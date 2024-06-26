from typing import Annotated, Union

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from db.dals import UserDAL
from db.models import User
from db.database import get_db
from services.hashing import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def _get_user_by_email_for_auth(email: str, db: AsyncSession):
    async with db.begin():
        user_dal = UserDAL(db=db)
        return await user_dal.get_user(email=email)


async def authenticate_user(
    email: str, password: str, db: AsyncSession
) -> Union[User, None]:
    
    user = await _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        return
    if not Hasher.verify(password, user.password):
        return
    return user


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        raise credentials_exception
    return user
