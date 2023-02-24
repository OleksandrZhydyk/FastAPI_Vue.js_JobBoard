import pytest
from starlette import status


async def test_create_job(company_client):

    job = {'email': 'test_job@test.com',
           'title': 'TestJob',
           'description': 'testpass',
           'salary_from': 10,
           'salary_to': 20,
           }
    resp = await company_client.post('jobs/', json=job)
    assert resp.status_code == status.HTTP_200_OK
    response_data = resp.json()
    assert response_data['email'] == 'test_job@test.com'
    assert response_data['title'] == 'TestJob'
    assert response_data['description'] == 'testpass'
    assert response_data['salary_from'] == 10
    assert response_data['salary_to'] == 20


async def test_get_all_jobs(authorized_client, create_job):
    resp = await authorized_client.get('jobs/')
    assert resp.status_code == status.HTTP_200_OK
    response_data = resp.json()
    assert response_data['total'] == 1
    assert response_data['items'][0]['email'] == 'test_job@test.com'

@pytest.mark.parametrize(
    'update_field, update_value',
    (
        ('email', 'updated_test_user@test.com'),
        ('title', 'updated_title'),
    ),
)
async def test_update_job(company_client, create_job, update_field, update_value):

    resp = await company_client.put(f'jobs/{create_job.id}', json={update_field: update_value})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()[update_field] == update_value


async def test_delete_job(company_client, create_job):
    resp = await company_client.delete(f'jobs/{create_job.id}')
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() is True


async def test_get_detail_job(company_client, create_job):
    resp = await company_client.get(f'jobs/{create_job.id}')
    assert resp.status_code == status.HTTP_200_OK
    response_data = resp.json()
    assert response_data['salary_from'] == 10
    assert response_data['category'] == "Miscellaneous"
    assert response_data['user']['id'] == 1


async def test_apply_to_job(authorized_client, create_job):
    resp = await authorized_client.post(f'jobs/{create_job.id}/apply')
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() is True

async def test_get_appliers_to_job(company_client, apply_to_job, create_job):
    resp = await company_client.get(f'jobs/{create_job.id}/apply')
    assert resp.status_code == status.HTTP_200_OK
    response_data = resp.json()
    assert response_data['email'] == 'test_job@test.com'
    assert response_data['category'] == 'Miscellaneous'
    assert response_data['appliers'][0]['email'] == 'test@test.com'
