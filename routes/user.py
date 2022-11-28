from typing import List
from fastapi import APIRouter, Body, Depends, Response

from beanie import PydanticObjectId

import database.user as db
import models.user as models

import auth.jwt as auth

r = APIRouter(
    tags=["User Routes"],
    prefix="/users",
    dependencies=[Depends(auth.get_active_user)],
)


@r.get("/me", response_model=models.UserOut)
async def user_me(current_user=Depends(auth.get_active_user)):
    """
    Get current user from JWT
    """
    return current_user


@r.get("/get/{id}", response_model=models.UserOut)
async def get_user(
    id: PydanticObjectId, admin=Depends(auth.get_current_active_admin)
):
    """
    Get a user by ID

    Args:
       - `id`: The MongoDB id of the user
    """
    return await db.get_user(id)


@r.post("", response_model=models.UserOut)
async def create_user(
    create: models.UserCreate = Body(),
    admin=Depends(auth.get_current_active_admin),
):
    """
    Create a new user in the database

    Args:
       - `user`: Create a new user
    """
    user = await db.create_user(create)

    return user


@r.put("/{id}", response_model=models.UserOut)
async def edit_user(id: PydanticObjectId, edit: models.UserEdit):
    """
    Edit a user in the database

    Args:
       - `id`: The MongoDB id of the user

       - `user`: The edited user
    """
    user = await db.edit_user(id, edit)

    return user


@r.delete("/{id}", response_model=bool)
async def delete_user(id: PydanticObjectId):
    """
    Delete a user in the database

    Args:
       - `id`: The MongoDB id of the user
    """
    user = await db.delete_user(id)

    return user


@r.get("", response_model=List[models.UserOut])
async def get_all_users(
    response: Response, superuser=Depends(auth.get_current_active_superuser)
):
    """
    Get all users

    Args:
       - `limit`: List size limit
    """
    users = await db.get_users()

    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(users)}"

    return users
