import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_full_user_journey():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        reg = await client.post('/auth/register', json={'email': 'e2e@depoz.io', 'password': 'Strong123!!'})
        assert reg.status_code == 200
        token = reg.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}

        step1 = await client.post('/brandcraft/step1', headers=headers, json={'brand_name': 'Depozio', 'activity_description': 'software finance'})
        assert step1.status_code == 200
        pid = step1.json()['project_id']

        assert (await client.post(f'/brandcraft/step2/{pid}', headers=headers, json={'territory': 'EU'})).status_code == 200
        suggest = await client.get(f'/brandcraft/step3/suggest/{pid}', headers=headers)
        assert suggest.status_code == 200
        assert (await client.post(f'/brandcraft/step3/{pid}', headers=headers, json={'nice_classes': suggest.json()['suggested']})).status_code == 200

        search = await client.post('/brandcraft/step4/search', headers=headers, json={'project_id': pid})
        assert search.status_code == 200
        results = await client.get(f'/brandcraft/step5/results/{pid}', headers=headers)
        assert results.status_code == 200
        assert len(results.json()['results']) > 0

        pdf = await client.get(f'/brandcraft/step6/report/{pid}', headers=headers)
        assert pdf.status_code == 200
        assert pdf.headers['content-type'] == 'application/pdf'
