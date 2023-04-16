import pytest
from starlette import status


async def test_create_user(client):
    user = {
        "email": "test_user@test.com",
        "password": "testpass",
        "confirmed_password": "testpass",
        "is_company": True,
        "is_active": True,
    }
    resp = await client.post("users/", json=user)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "test_user@test.com"
    assert resp.json()["is_company"] is True
    assert resp.json()["is_active"] is True


async def test_create_user_duplicate(client, create_user):
    user = {
        "email": "test@test.com",
        "password": "testpass",
        "confirmed_password": "testpass",
        "is_company": True,
        "is_active": True,
    }
    resp = await client.post("users/", json=user)
    assert resp.status_code == status.HTTP_409_CONFLICT
    assert resp.json()["detail"] == "This email is already registered"


async def test_update_user_duplicate(superuser_client, create_user, create_company):
    user = {"email": "test@test.com"}
    resp = await superuser_client.put(f"users/{create_company.id}", data=user)
    assert resp.status_code == status.HTTP_409_CONFLICT
    assert resp.json()["detail"] == "This email is already registered"


@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_detail",
    (
        (
            {
                "email": "test_user@test.com",
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
                "is_company": "false",
                "password": "password",
                "confirmed_password": "changed_password",
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["body", "confirmed_password"],
                        "msg": "Please enter the same value for password and confirmation password field",
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
                "is_company": "not_a_bool",
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["body", "is_company"],
                        "msg": "value could not be parsed to a boolean",
                        "type": "type_error.bool",
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
                "is_company": "false",
                "password": "password",
                "confirmed_password": "password",
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "field required",
                        "type": "value_error.missing"
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
    assert resp.json()["is_company"] is False
    assert resp.json()["is_active"] is True


async def test_get_user(create_user, superuser_client):
    resp = await superuser_client.get(f"/users/{create_user.id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "test@test.com"
    assert resp.json()["is_company"] is False
    assert resp.json()["is_active"] is True


async def test_user_access_to_another_user(authorized_client, create_superuser):
    resp = await authorized_client.get(f"/users/{create_superuser.id}")
    assert resp.status_code == status.HTTP_403_FORBIDDEN


async def test_user_update_of_another_user(authorized_client, create_superuser):
    resp = await authorized_client.put(f"/users/{create_superuser.id}", json={"name": "Hacker"})
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
    print(resp.json())
    assert resp.status_code == expected_status_code
    assert resp.json() == expected_detail


@pytest.mark.parametrize(
    "update_field, update_value",
    (
        ("email", "updated_test@test.com"),
        ("name", "Updated"),
        ("is_active", False),
        ("is_company", True)
    ),
)
async def test_update_user(create_user, superuser_client, update_field, update_value):
    resp = await superuser_client.put(f"/users/{create_user.id}", data={update_field: update_value})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()[update_field] == update_value


async def test_create_user_superuser(create_user, superuser_client):
    user = {
        "email": "test_user@test.com",
        "password": "testpass",
        "confirmed_password": "testpass",
    }
    resp = await superuser_client.post("users/", json=user)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "test_user@test.com"
    assert resp.json()["is_company"] is False
    assert resp.json()["is_active"] is True


async def test_delete_user(superuser_client):
    resp = await superuser_client.delete("/users/1")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {'message': True}
