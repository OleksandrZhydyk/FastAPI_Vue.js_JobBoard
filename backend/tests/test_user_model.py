import httpx
import pytest
from starlette import status


async def test_create_user(client):
    user = {
        "email": "test_user@test.com",
        "name": "Test",
        "password": "testpass",
        "confirmed_password": "testpass",
        "is_company": True,
        "is_active": True,
    }
    resp = await client.post("users/", json=user)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "test_user@test.com"
    assert resp.json()["name"] == "Test"
    assert resp.json()["is_company"] is True
    assert resp.json()["is_active"] is True


async def test_create_user_duplicate(client, create_user):
    user = {
        "email": "test@test.com",
        "name": "Test",
        "password": "testpass",
        "confirmed_password": "testpass",
        "is_company": True,
        "is_active": True,
    }
    resp = await client.post("users/", json=user)
    assert resp.status_code == status.HTTP_409_CONFLICT
    assert resp.json()["detail"] == "This email is already registered"


@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_detail",
    (
        (
            {
                "email": "test_user@test.com",
                "name": "Test",
                "is_company": "false",
                "password": "123",
                "confirmed_password": "123",
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["body", "password"],
                        "msg": "ensure this value has at least 8 characters",
                        "type": "value_error.any_str.min_length",
                        "ctx": {"limit_value": 8},
                    }
                ]
            },
        ),
        (
            {
                "email": "test_user@test.com",
                "name": "Test",
                "is_company": "false",
                "password": "password",
                "confirmed_password": "changed_password",
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["body", "confirmed_password"],
                        "msg": "Please enter the same value for password and confirmed password field",
                        "type": "value_error",
                    }
                ]
            },
        ),
        (
            {
                "email": "test_user@test.com",
                "password": "password",
                "confirmed_password": "password",
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["body", "is_company"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            {
                "email": "not_email",
                "name": "Test",
                "is_company": "false",
                "password": "password",
                "confirmed_password": "password",
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    }
                ]
            },
        ),
        (
            {
                "email": "test_user@test.com",
                "name": "",
                "is_company": "false",
                "password": "password",
                "confirmed_password": "password",
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["body", "name"],
                        "msg": "ensure this value has at least 2 characters",
                        "type": "value_error.any_str.min_length",
                        "ctx": {"limit_value": 2},
                    }
                ]
            },
        ),
    ),
)
async def test_create_user_fail(
    client, user_data, expected_status_code, expected_detail
):
    resp = await client.post("users/", json=user_data)
    assert resp.status_code == expected_status_code
    assert resp.json() == expected_detail


async def test_get_me(authorized_client):
    resp = await authorized_client.get(
        "/users/me",
    )
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "test@test.com"
    assert resp.json()["name"] == "Test"
    assert resp.json()["is_company"] is False
    assert resp.json()["is_active"] is True


async def test_get_user(create_user, superuser_client):
    resp = await superuser_client.get("/users/1")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "test@test.com"
    assert resp.json()["name"] == "Test"
    assert resp.json()["is_company"] is False
    assert resp.json()["is_active"] is True


async def test_user_access_to_another_user(authorized_client, create_superuser):
    resp = await authorized_client.get("/users/2")
    assert resp.status_code == status.HTTP_403_FORBIDDEN


async def test_user_update_of_another_user(authorized_client, create_superuser):
    resp = await authorized_client.put("/users/2", json={"name": "Hacker"})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "update_field, update_value",
    (
        ("email", "updated_test@test.com"),
        ("name", "Updated"),
    ),
)
async def test_update_me(authorized_client, update_field, update_value):
    resp = await authorized_client.put("/users/me", data={update_field: update_value})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()[update_field] == update_value
    assert resp.json()["is_company"] is False


@pytest.mark.parametrize(
    "updated_user_data, expected_status_code, expected_detail",
    (
        (
            {"name": "123"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {"detail": "Name should contains only letters"},
        ),
        (
            {"name": "a"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "ctx": {"limit_value": 2},
                        "loc": ["name"],
                        "msg": "ensure this value has at least 2 characters",
                        "type": "value_error.any_str.min_length",
                    }
                ]
            },
        ),
        (
            {"email": "123"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    }
                ]
            },
        ),
        (
            {"email": "not_email"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    }
                ]
            },
        ),
    ),
)
async def test_update_me_fail(
    authorized_client, updated_user_data, expected_status_code, expected_detail
):
    resp = await authorized_client.put("/users/me", data=updated_user_data)
    assert resp.status_code == expected_status_code
    assert resp.json() == expected_detail

@pytest.mark.parametrize(
    "update_field, update_value",
    (
        ("email", "updated_test@test.com"),
        ("name", "Updated"),
    ),
)
async def test_update_user(create_user, superuser_client, update_field, update_value):
    resp = await superuser_client.put("/users/1", data={update_field: update_value})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()[update_field] == update_value
    assert resp.json()["is_company"] is False


async def test_delete_user(superuser_client):
    resp = await superuser_client.delete("/users/1")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {'message': True}
