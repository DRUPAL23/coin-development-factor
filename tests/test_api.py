from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


def test_health() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_validation_endpoint() -> None:
    response = client.get('/v1/validate')
    assert response.status_code == 200
    assert response.json()['valid'] is True
    assert response.json()['errors'] == []


def test_contract_endpoint_returns_source() -> None:
    response = client.get('/v1/contracts/example')
    assert response.status_code == 200
    assert response.json()['contract_name'] == 'ExampleCoin'
    assert 'contract ExampleCoin' in response.json()['source']
