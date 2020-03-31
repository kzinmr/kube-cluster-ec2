'''
Tests for flask app.
'''
import pytest

import app


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    client = app.app.test_client()
    yield client


def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"text":"Healthy"}
