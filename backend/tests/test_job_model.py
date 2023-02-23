import pytest
from starlette import status


# @pytest.mark.asyncio
# async def test_create_job(company_client):
#
#     job = {"email": "test_user@test.com",
#            "title": "Test",
#            "description": "testpass",
#            "salary_from": 10,
#            "salary_to": 20,
#            }
#     resp = await company_client.post('jobs/', json=job)
#     assert resp.status_code == status.HTTP_200_OK
#     assert resp.json()["email"] == "test_user@test.com"
#     assert resp.json()["title"] == "Test"
#     assert resp.json()["description"] == True
#     assert resp.json()["salary_from"] == 10
#     assert resp.json()["salary_to"] == 20