import pytest
from passlib.context import CryptContext
from httpx import AsyncClient
from beanie import PydanticObjectId

from models.user import User

# Same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def test_get_user(
    client: AsyncClient, test_user: User, superuser_token_headers
):
    response = await client.get(
        f"/users/{test_user.id}", headers=superuser_token_headers
    )

    assert response.status_code == 200
    assert response.json() == {
        "_id": test_user.id.__str__(),
        "first_name": test_user.first_name,
        "last_name": test_user.last_name,
        "avatar": test_user.avatar,
        "email": test_user.email,
        "is_active": bool(test_user.is_active),
        "is_super_user": test_user.is_super_user,
        "is_admin_user": test_user.is_admin_user,
    }


async def test_user_not_found(client: AsyncClient, superuser_token_headers):
    id = PydanticObjectId()

    response = await client.get(
        f"/users/{id}", headers=superuser_token_headers
    )

    assert response.status_code == 404


async def test_create_user(
    client: AsyncClient,
    test_password,
    test_adminuser: User,
    adminuser_token_headers,
):
    response = await client.post(
        "/users",
        json={
            "email": "newuser@gmail.com",
            "password": test_password,
        },
        headers=adminuser_token_headers,
    )

    assert response.status_code == 200

    assert response.json() == {
        "_id": response.json()["_id"],
        "first_name": None,
        "last_name": None,
        "avatar": None,
        "email": "newuser@gmail.com",
        "is_active": True,
        "is_admin_user": True,
        "is_super_user": False,
    }


async def test_edit_user(
    client: AsyncClient, test_superuser: User, superuser_token_headers
):
    user = {
        "first_name": None,
        "last_name": None,
        "avatar": None,
        "email": "usereditemail@email.com",
        "is_active": False,
        "is_admin_user": True,
        "is_super_user": True,
        "password": "new_password",
    }

    response = await client.put(
        f"/users/{test_superuser.id}",
        json=user,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200

    user["_id"] = test_superuser.id.__str__()

    user.pop("password")

    assert response.json() == user


async def test_edit_user_not_found(
    client: AsyncClient, superuser_token_headers
):
    id = PydanticObjectId()

    new_user = {
        "email": "usereditemail@email.com",
        "is_active": False,
        "is_super_user": False,
        "is_admin_user": False,
        "password": "new_password",
    }

    response = await client.put(
        f"/users/{id}", json=new_user, headers=superuser_token_headers
    )

    assert response.status_code == 404


async def test_delete_user(
    client: AsyncClient,
    test_user: User,
    test_superuser: User,
    superuser_token_headers,
):
    response = await client.delete(
        f"/users/{(test_user.id)}", headers=superuser_token_headers
    )

    response = await client.delete(
        f"/users/{(test_superuser.id)}", headers=superuser_token_headers
    )

    assert response.status_code == 200

    assert await User.find({}).to_list() == []


async def test_delete_user_not_found(
    client: AsyncClient, superuser_token_headers
):
    id = PydanticObjectId()

    response = await client.delete(
        f"/users/{id}", headers=superuser_token_headers
    )

    assert response.status_code == 404


async def test_users_lists(
    client: AsyncClient,
    test_user: User,
    test_superuser: User,
    superuser_token_headers,
):
    response = await client.get(
        "/users/get-all/", headers=superuser_token_headers
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "_id": test_user.id.__str__(),
            "first_name": test_user.first_name,
            "last_name": test_user.last_name,
            "avatar": test_user.avatar,
            "email": test_user.email,
            "is_active": test_user.is_active,
            "is_admin_user": test_user.is_admin_user,
            "is_super_user": test_user.is_super_user,
        },
        {
            "_id": test_superuser.id.__str__(),
            "first_name": test_superuser.first_name,
            "last_name": test_superuser.last_name,
            "avatar": test_superuser.avatar,
            "email": test_superuser.email,
            "is_active": test_superuser.is_active,
            "is_admin_user": test_superuser.is_admin_user,
            "is_super_user": test_superuser.is_super_user,
        },
    ]


async def test_authenticated_user_me(
    client: AsyncClient, test_user: User, user_token_headers
):
    response = await client.get("/users", headers=user_token_headers)

    assert response.status_code == 200

    assert response.json() == {
        "_id": test_user.id.__str__(),
        "first_name": test_user.first_name,
        "last_name": test_user.last_name,
        "avatar": test_user.avatar,
        "email": test_user.email,
        "is_active": test_user.is_active,
        "is_admin_user": test_user.is_admin_user,
        "is_super_user": test_user.is_super_user,
    }


async def test_unauthenticated_routes(client: AsyncClient):
    response = await client.get("/users")
    assert response.status_code == 401

    response = await client.get("/users/123")
    assert response.status_code == 401

    response = await client.put("/users/123")
    assert response.status_code == 401

    response = await client.delete("/users/123")
    assert response.status_code == 401


async def test_unauthorized_routes(client: AsyncClient, user_token_headers):
    response = await client.get("/users/get-all", headers=user_token_headers)
    assert response.status_code == 403

    response = await client.get("/users/123", headers=user_token_headers)
    assert response.status_code == 403
