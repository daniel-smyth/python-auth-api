from typing import Optional
from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


class User(Document):
    """A user document as it is stored in a MongoDB database"""

    email: Indexed(EmailStr, unique=True)
    first_name: str = None
    last_name: str = None
    avatar: str = None
    is_active: bool = True
    is_admin_user: bool = True
    is_super_user: bool = True
    hashed_password: str


class UserBase(BaseModel):
    email: str
    first_name: str = None
    last_name: str = None
    avatar: str = None
    is_active: bool = True
    is_admin_user: bool = False
    is_super_user: bool = False


class UserCreate(UserBase):
    password: str


class UserEdit(UserBase):
    password: Optional[str] = None


class UserOut(UserBase):
    id: PydanticObjectId = Field(..., alias="_id")
    """The objects MongoDB ID"""
