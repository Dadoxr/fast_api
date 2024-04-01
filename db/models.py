from enum import Enum
import uuid
from sqlalchemy import UUID, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Role(str, Enum):
    """
    Class collect type of roles
    """

    CLIENT = "client"
    ADMIN = "admin"


class Service(str, Enum):
    """
    Class collect all services
    """

    AUTH = "auth"
    SCHEDULER = "scheduler"
    GRAPHICS = "graphics"


class User(Base):
    """
    Class collect all users

    - username
    - email
    - password
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

    roles = relationship("UserRole", back_populates="users")


class UserRole(Base):
    """
    Class collect roles of users

    - user_id
    - role
    - service

    """

    __tablename__ = "user_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role = Column(String)
    service = Column(String)

    users = relationship("User", back_populates="roles")
