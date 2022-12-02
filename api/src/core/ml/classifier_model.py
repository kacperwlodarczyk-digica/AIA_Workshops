from typing import Optional

import tensorflow as tf

from api.src.core.schemas.predictions import Prediction
from api.src.core.ml.classifier_files import ClassifierModelFiles


class ClassifierModel:
    def __init__(self, files: ClassifierModelFiles):
        self.files = files
        # Initialize on load
        self._classifier_model: Optional[tf.keras.models.Sequential] = None
        self._input_shape: Optional[tuple[None, int, int, int]] = None
        self._indexes_to_labels: Optional[dict[str, str]] = None

    def __call__(self, image_content: bytes):
        image = self.preprocess(image_content)
        output = self.predict(image)
        prediction = self.postprocess(image, output)
        return prediction

    def preprocess(self, image_content: bytes) -> tf.Tensor:
        # TODO YOUR CODE HERE
        # Run test: pytest tests/ml/test_classifier_model.py -k "test_preprocess_method"
        ... # remove after implementing the code

    def predict(self, image: tf.Tensor) -> tf.Tensor:
        # TODO YOUR CODE HERE
        # Run test: pytest tests/ml/test_classifier_model.py -k "test_predict_method"
        ... # remove after implementing the code

    def postprocess(self, image: tf.Tensor, output: tf.Tensor) -> Prediction:
        # TODO YOUR CODE HERE
        # Run test: pytest tests/ml/test_classifier_model.py -k "test_postprocess_method"
        ... # remove after implementing the code

    def load(self):
        # TODO YOUR CODE HERE
        # Run test: pytest tests/ml/test_classifier_model.py -k "test_load_method"
        ... # remove after implementing the code

    @property
    def ready(self):
        return (
            self._classifier_model is not None
            and self._indexes_to_labels is not None
            and self._input_shape is not None
        )

    def _map_index_to_label(self, index: int):
        label_raw: str = self._indexes_to_labels[str(index)]
        return label_raw.replace("_", " ").capitalize()
