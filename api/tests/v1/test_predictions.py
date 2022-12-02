from unittest import mock
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette import status

from api.src.core.schemas.predictions import Prediction
from api.src.core.services.predictions_service import PredictionsService
from api.tests.ml.test_classifier_model import HEALTHY_IMAGE_NAME


def test_predict(app: FastAPI, client: TestClient, assets_path: Path):
    with open(assets_path / HEALTHY_IMAGE_NAME, "rb") as f:
        response = client.post(
            app.url_path_for("predict"), files={"image_file": (HEALTHY_IMAGE_NAME, f, "image/jpeg")}
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["label"].lower() == "healthy"


def test_dummy_predict_with_override(app: FastAPI, client: TestClient, assets_path: Path):
    prediction_service_mock = mock.Mock(spec=PredictionsService)
    test_label = "TEST_LABEL"
    test_score = 0.91
    prediction_service_mock.predict.return_value = Prediction(label=test_label, score=test_score)

    # More: https://python-dependency-injector.ets-labs.org/examples/fastapi.html?highlight=fastapi#tests
    with app.container.prediction_service.override(prediction_service_mock):
        with open(assets_path / HEALTHY_IMAGE_NAME, "rb") as f:
            response = client.post(
                app.url_path_for("predict"), files={"image_file": (HEALTHY_IMAGE_NAME, f, "image/jpeg")}
            )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["label"] == test_label
    assert response.json()["score"] == test_score
