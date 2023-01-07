import pytest


@pytest.mark.asyncio
async def test_create_user(async_client):

    user = {"email": "test@test.com",
            "name": "Test",
            "password": "testpass",
            "confirmed_password": "testpass",
            "is_company": True,
            "is_active": True
            }
    resp = await async_client.post('users/', json=user)
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@test.com"
    assert resp.json()["name"] == "Test"
    assert resp.json()["is_company"] == True
    assert resp.json()["is_active"] == True


@pytest.mark.asyncio
async def test_async_get_jobs(async_client):
    resp = await async_client.get('/jobs/')
    assert resp.status_code == 404
    assert resp.json()["detail"] == "There are no objects"





# @pytest.mark.asyncio
# async def test_create_user(test_db) -> None:
#     user = {
#         "email": "test6@test.com",
#         "name": "Test",
#         "password": "testpass",
#         "confirmed_password": "testpass",
#         "is_company": True,
#         "is_active": True
#     }

    # token = create_access_token({'sub': user['email']})
    # response = await AsyncClient(app=app, base_url="http://localhost:8000",).post(app.url_path_for("create_user"), json=user, headers={"Authorization": f"Bearer {token}",
    #                                                                                                                                    "Content-Type": "application/json"})
    # assert response.status_code == 200
    # assert response.json()["email"] == "test6@test.com"

    # try:
    #     user = await create_user(user)
    #     assert False, 'already registered'
    # except sqlalchemy.exc.IntegrityError:
    #     pass

# def test_ordinary():
#     user = {
#             "email": "test6@test.com",
#             "name": "Test",
#             "password": "testpass",
#             "confirmed_password": "testpass",
#             "is_company": True,
#             "is_active": True
#         }
#     with TestClient(app) as client:
#         # token = create_access_token({'sub': user['email']})
#         response = client.get("/jobs")
#         # response = client.get("/users", json=user)
#
#     assert response.status_code == 404
#     assert response.json()["detail"] == "There are no objects"


    # headers = {"Authorization": f"Bearer {token}"}