from fastapi import HTTPException, status
from beanie import PydanticObjectId

import auth.security as security

import models.user as models


async def get_user(id: PydanticObjectId):
    db_user = await models.User.find_one(models.User.id == id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return db_user


async def get_user_by_email(email: str):
    return await models.User.find_one(models.User.email == email)


async def create_user(user: models.UserCreate):
    db_user = await get_user_by_email(user.email)

    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    hashed_password = security.get_password_hash(user.password)

    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_super_user=user.is_super_user,
        hashed_password=hashed_password,
    )

    await db_user.save()

    return db_user


async def edit_user(id: PydanticObjectId, edit: models.UserEdit):
    db_user = await get_user(id)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    new_user_dict = edit.dict(exclude_unset=True)

    if "password" in new_user_dict:
        new_user_dict["hashed_password"] = security.get_password_hash(
            new_user_dict["password"]
        )
        del new_user_dict["password"]

    for key, value in new_user_dict.items():
        setattr(db_user, key, value)

    await db_user.save()
    return db_user


async def delete_user(id: PydanticObjectId):
    user = await get_user(id)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    await user.delete()

    return True


async def get_users(limit: int = 100):
    return await models.User.find({}).limit(limit).to_list()
