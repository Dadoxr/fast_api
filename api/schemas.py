import uuid
from pydantic import BaseModel, EmailStr

from db.models import Role, Service


class User(BaseModel):
    email: EmailStr


class UserCreate(User):
    password: str


class UserShow(User):
    id: uuid.UUID
    username: str

    class Config:
        from_attributes = True


class UserRoleCreate(User):
    role: Role
    service: Service


class UserRoleShow(User):
    id: uuid.UUID
    user_id: uuid.UUID
    username: str
    role: Role
    service: Service

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str