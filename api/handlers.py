from typing import Annotated
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import User, UserCreate, UserShow, UserRoleCreate, UserRoleShow
from db.dals import UserDAL
from db.database import get_db
from db.models import UserRole
from services.hashing import Hasher
from api.actions.auth import get_current_user_from_token


users_router = APIRouter()


@users_router.post("/")
async def create_user(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UserShow:
    user_dal = UserDAL(db=db)
    try:
        user = await user_dal.create_user(
            email=body.email, hashed_password=Hasher.get_hash(body.password)
        )
        return UserShow(id=user.id, email=user.email, username=user.username)

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with {body.email} already exists",
        )


@users_router.delete("/")
async def delete_user(
    body: User,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> dict[str, str]:
    user_dal = UserDAL(db=db)
    await user_dal.delete_user(email=body.email)
    return {"message": f"user {body.email} has been deleted if existed"}


@users_router.get("/")
async def get_all_users(
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> list[UserShow]:

    user_dal = UserDAL(db=db)

    offset = (page - 1) * size
    users = await user_dal.get_all_users(offset=offset, limit=size)
    return [
        UserShow(id=user.id, username=user.username, email=user.email) for user in users
    ]


@users_router.post("/role/")
async def add_user_role(
    body: UserRoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UserRoleShow | dict[str, str]:
    user_dal = UserDAL(db=db)
    user = await user_dal.get_user(email=body.email)
    if user:
        service_is_exists = await user_dal.check_service_for_user_is_exists(
            user_id=user.id, service=body.service
        )
        if not service_is_exists:
            role = await user_dal.add_user_role(
                user_id=user.id, role=body.role, service=body.service
            )
            return UserRoleShow(
                id=role.id,
                user_id=user.id,
                username=user.username,
                email=user.email,
                role=role.role,
                service=role.service,
            )

        return {
            "message": f"Service {body.service} with user {body.email} exists. Change method to patch"
        }
    return {"message": f"User with {body.email} does not exists"}


@users_router.patch("/role/")
async def update_user_role(
    body: UserRoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UserRoleShow | dict[str, str]:
    user_dal = UserDAL(db=db)
    user = await user_dal.get_user(email=body.email)
    if user:
        service_is_exists = await user_dal.check_service_for_user_is_exists(
            user_id=user.id, service=body.service
        )
        if service_is_exists:
            role: UserRole = await user_dal.update_user_role(
                user_id=user.id, role=body.role, service=body.service
            )
            return UserRoleShow(
                id=role.id,
                user_id=user.id,
                username=user.username,
                email=user.email,
                role=role.role,
                service=role.service,
            )
        return {
            "message": f"Service {body.service} with user {body.email} exists. Change method to post"
        }
    return {"message": f"User with {body.email} does not exists"}
