from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette import status

from api.tests.ml.test_classifier_model import HEALTHLY_IMAGE_NAME


def test_predict(app: FastAPI, client: TestClient, assets_path: Path):
    with open(assets_path / HEALTHLY_IMAGE_NAME, "rb") as f:
        response = client.post(
            app.url_path_for("predict"), files={"image_file": (HEALTHLY_IMAGE_NAME, f, "image/jpeg")}
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["label"].lower() == "healthy"
