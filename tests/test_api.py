import json
from datetime import datetime
from decimal import Decimal

import pytest as pytest
from fastapi.testclient import TestClient
from starlette import status

from app.main import app
from app.models import NamkhaData, Fraction, Gender, Location, Method, CalculationStatus, CalculationData


@pytest.fixture
def client():
    return TestClient(app)


def test_status(client):
    response = client.get('/status')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_tz(client):
    response = client.get('/tz', params=dict(lat=-23.5475, lon=-46.63611, date='2023-02-15T00:00:00'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'tz': 'America/Sao_Paulo', 'offset': -3}

    response = client.get('/tz', params=dict(lat=-23.5475, lon=-46.63611, date='2018-02-15T00:00:00'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'tz': 'America/Sao_Paulo', 'offset': -2}


def test_calculate(client):
    namkha_data = NamkhaData(fraction=Fraction.year,
                             name='John Doe',
                             gender=Gender.male,
                             datetime=datetime.now(),
                             location=Location(lat=Decimal('-23.5475'), lon=Decimal('-46.63611')),
                             method=Method.rinpoche,)
    response = client.post('/calculate', content=namkha_data.__json__())
    assert response.status_code == status.HTTP_201_CREATED
    calc = CalculationData(**json.loads(response.content))
    assert calc.id
    assert calc.created
    assert calc.status == CalculationStatus.new
    assert calc.result is None
    assert calc.finished is None

    response = client.get(f'/calculate/{calc.id}')
    assert response.status_code == status.HTTP_200_OK
    calc_ = CalculationData(**json.loads(response.content))
    assert calc_.id == calc.id
    assert calc_.created == calc.created
    assert calc_.status == calc.status
    assert calc_.result == calc.result
    assert calc_.finished == calc.finished
