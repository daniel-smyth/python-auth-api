import pytest
from typing import AsyncGenerator, Dict
from httpx import AsyncClient


import main
import config
import auth.security
import utils.mongo

from models.user import User


settings = config.get_settings()


def get_password_hash() -> str:
    """
    Password hashing can be expensive so a mock will be much faster
    """
    return "securepasswordsecrethash"


def verify_password_mock(first: str, second: str):
    """
    Replaces real function in auth.security with monkeypatch. See
    superuser_token_headers, adminuser_token_headers, user_token_headers
    """
    return True


@pytest.fixture
def test_password() -> str:
    return "securepassword"


@pytest.fixture
async def test_superuser() -> User:
    """
    Make a test super user in the database
    """
    user = User(
        email="fakesuperuser@email.com",
        hashed_password=get_password_hash(),
        is_super_user=True,
        is_admin_user=True,
    )

    await user.save()

    return user


@pytest.fixture
async def superuser_token_headers(
    client: AsyncClient,
    test_superuser: User,
    test_password,
    monkeypatch,
) -> Dict[str, str]:
    """
    monkeypatch: A MonkeyPatch is a piece of Python code which extends or
    modifies other code at runtime (typically at startup). This monkeypatch
    replaces the verify_password with testing verify_password_mock
    """
    monkeypatch.setattr(auth.security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_superuser.email,
        "password": test_password,
    }

    response = await client.post("auth/token", data=login_data)

    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    return headers


@pytest.fixture
async def test_adminuser() -> User:
    """
    Make a test admin user in the database
    """
    user = User(
        email="fakeadminuser@email.com",
        hashed_password=get_password_hash(),
        is_admin_user=True,
        is_super_user=False,
    )
    await user.save()
    return user


@pytest.fixture
async def adminuser_token_headers(
    client: AsyncClient,
    test_adminuser: User,
    test_password,
    monkeypatch,
) -> Dict[str, str]:
    """
    monkeypatch: A MonkeyPatch is a piece of Python code which extends or
    modifies other code at runtime (typically at startup). This monkeypatch
    replaces the verify_password with testing verify_password_mock
    """
    monkeypatch.setattr(auth.security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_adminuser.email,
        "password": test_password,
    }

    response = await client.post("auth/token", data=login_data)

    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    return headers


@pytest.fixture
async def test_user() -> User:
    """
    Make a test admin user in the database
    """
    user = User(
        email="fakeuser@email.com",
        hashed_password=get_password_hash(),
        is_admin_user=False,
        is_super_user=False,
    )

    await user.save()

    return user


@pytest.fixture
async def user_token_headers(
    client: AsyncClient,
    test_user: User,
    test_password,
    monkeypatch,
) -> Dict[str, str]:
    """
    monkeypatch: A MonkeyPatch is a piece of Python code which extends or
    modifies other code at runtime (typically at startup). This monkeypatch
    replaces the verify_password with testing verify_password_mock
    """
    monkeypatch.setattr(auth.security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_user.email,
        "password": test_password,
    }

    response = await client.post("auth/token", data=login_data)

    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    return headers


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop")
    ]
)
def anyio_backend(request):
    """
    For asyncronous requests
    """
    return request.param


@pytest.fixture
async def client() -> AsyncGenerator:
    """
    Connect to MongoDB and yield AsyncClient until testing is complete. Tear
    down database on end of tests
    """
    db_name = "pytest"

    async with AsyncClient(
        app=main.app, base_url="http://testserver"
    ) as client:
        await utils.mongo.manager.connect(
            db_url=settings.DB_URL, db_name=db_name
        )
        await utils.mongo.manager.init_beanie(db_name)

        yield client

        await utils.mongo.manager.async_client.drop_database(db_name)
        utils.mongo.manager.async_client.close()
