from httpx import AsyncClient
import pytest
import auth.security


# Same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio


def verify_password_mock(first: str, second: str):
    return True


async def test_login(client: AsyncClient, test_user, monkeypatch):
    # Patch verify_password to skip password hashing (improves speed)
    monkeypatch.setattr(auth.security, "verify_password", verify_password_mock)

    response = await client.post(
        "auth/token",
        data={"username": test_user.email, "password": "nottheactualpass"},
    )

    assert response.status_code == 200


async def test_signup(client: AsyncClient, monkeypatch):
    def get_password_hash_mock(first: str):
        return True

    # Patch get_password_hash to skip password hashing (improves speed)
    monkeypatch.setattr(
        auth.security, "get_password_hash", get_password_hash_mock
    )

    response = await client.post(
        "auth/signup",
        data={"username": "some@email.com", "password": "randompassword"},
    )

    assert response.status_code == 200


async def test_resignup(client: AsyncClient, test_user, monkeypatch):
    # Patch verify_password to skip password hashing (improves speed)
    monkeypatch.setattr(auth.security, "verify_password", verify_password_mock)

    response = await client.post(
        "auth/signup",
        data={
            "username": test_user.email,
            "password": "password_hashing_is_skipped_via_monkey_patch",
        },
    )
    assert response.status_code == 409


async def test_wrong_password(
    client: AsyncClient, test_user, test_password, monkeypatch
):
    # Patch verify_password to skip password hashing (improves speed)
    def verify_password_failed_mock(first: str, second: str):
        return False

    monkeypatch.setattr(
        auth.security, "verify_password", verify_password_failed_mock
    )

    response = await client.post(
        "auth/token", data={"username": test_user.email, "password": "wrong"}
    )

    assert response.status_code == 401


async def test_wrong_login(client: AsyncClient, test_user, test_password):
    response = await client.post(
        "auth/token", data={"username": "fakeuser", "password": test_password}
    )

    assert response.status_code == 401
