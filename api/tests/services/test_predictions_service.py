from pathlib import Path

from api.src.core.schemas.predictions import Prediction
from api.src.core.services.predictions_service import PredictionsService

from api.tests.ml.test_classifier_model import HEALTHLY_IMAGE_NAME


def test_predict_method(predictions_service: PredictionsService, assets_path: Path):
    predictions_service.setup_model()
    with open(assets_path / HEALTHLY_IMAGE_NAME, mode="rb") as f:
        image_content = f.read()
    prediction = predictions_service.predict(image_content=image_content)
    assert isinstance(prediction, Prediction)
    assert prediction.label.lower() == "healthy"


def test_setup_model(predictions_service: PredictionsService):
    assert not predictions_service._model.ready
    predictions_service.setup_model()
    assert predictions_service._model.ready
