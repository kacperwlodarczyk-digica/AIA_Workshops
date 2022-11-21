from pathlib import Path

from api.src.core.schemas.predictions import Prediction
from api.src.core.ml_models.classifier import ClassifierModel


class PredictionService:
    def __init__(self, classifier_model: ClassifierModel) -> None:
        self._classifier = classifier_model

    def predict(self, image_content: bytes) -> Prediction:
        return self._classifier(image_content)

    def load_model(self) -> bool:
        model_path = Path("/home/kwlodarczyk/Documents/ai_academy/workshop/data/model_k_kren_final.h5")
        class_names_path = Path("/home/kwlodarczyk/Documents/ai_academy/workshop/data/class_names.json")
        self._classifier.load(model_path, class_names_path)
        return self._classifier.ready

    def unload_model(self) -> bool:
        self._classifier.unload()
        return self._classifier.ready
