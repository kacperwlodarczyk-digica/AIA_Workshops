from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_healthcheck(app: FastAPI, client: TestClient):
    response = client.get(app.url_path_for("healthcheck"))
    assert response.status_code == 200
    assert response.json() == "OK"
