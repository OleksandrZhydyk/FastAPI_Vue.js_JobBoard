import pytest
from starlette import status


async def test_create_user(client):

    user = {"email": "test_user@test.com",
            "name": "Test",
            "password": "testpass",
            "confirmed_password": "testpass",
            "is_company": True,
            "is_active": True
            }
    resp = await client.post('users/', json=user)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "test_user@test.com"
    assert resp.json()["name"] == "Test"
    assert resp.json()["is_company"] is True
    assert resp.json()["is_active"] is True


async def test_get_me(authorized_client):
    resp = await authorized_client.get('/users/me', )
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "test@test.com"
    assert resp.json()["name"] == "Test"
    assert resp.json()["is_company"] is False
    assert resp.json()["is_active"] is True


async def test_get_user(create_user, superuser_client):
    resp = await superuser_client.get('/users/1')
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "test@test.com"
    assert resp.json()["name"] == "Test"
    assert resp.json()["is_company"] is False
    assert resp.json()["is_active"] is True


async def test_user_access_to_another_user(authorized_client, create_superuser):
    resp = await authorized_client.get('/users/2')
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_user_update_of_another_user(authorized_client, create_superuser):
    resp = await authorized_client.put('/users/2', json={"name": "Hacker"})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "update_field, update_value",
    (
        ("email", "updated_test@test.com"),
        ("name", "Updated"),
    ),
)
async def test_update_me(authorized_client, update_field, update_value):
    resp = await authorized_client.put('/users/me', json={update_field: update_value})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()[update_field] == update_value
    assert resp.json()['is_company'] is False


@pytest.mark.parametrize(
    "update_field, update_value",
    (
        ("email", "updated_test@test.com"),
        ("name", "Updated"),
    ),
)
async def test_update_user(create_user, superuser_client, update_field, update_value):
    resp = await superuser_client.put('/users/1', json={update_field: update_value})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()[update_field] == update_value
    assert resp.json()['is_company'] is False


async def test_delete_user(superuser_client):
    resp = await superuser_client.delete('/users/1')
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() is True
