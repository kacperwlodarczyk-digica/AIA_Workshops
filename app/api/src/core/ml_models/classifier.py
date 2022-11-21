import gc
from pathlib import Path
from typing import Literal, Union
import json

import tensorflow as tf
from tensorflow_addons.metrics import F1Score

from api.src.core.schemas.predictions import Prediction
from api.src.core.common.exceptions import ModelUninitializedException


class ClassifierModel:
    def __init__(self, device: Literal["cpu", "gpu"] = "cpu") -> None:
        self._device = device
        # Initialize on load
        self._classifier_model: tf.keras.models.Sequential = None
        self._input_shape: tuple[None, int, int, int] = None
        self._indexes_to_labels: dict[str, str] = None

    def __call__(self, image_content: bytes) -> Prediction:
        image = self.preprocess(image_content)
        output = self.predict(image)
        prediction = self.postprocess(image, output)
        return prediction

    def preprocess(self, image_content: bytes, crop_to_aspect_ratio: bool = False) -> tf.Tensor:
        height, width, n_channels = self._input_shape[-3:]
        image_tf: tf.Tensor = tf.image.decode_image(image_content, channels=n_channels, expand_animations=False)
        if crop_to_aspect_ratio:
            image_tf = tf.keras.preprocessing.image.smart_resize(image_tf, (height, width))
        else:
            image_tf = tf.image.resize(image_tf, (height, width))
        image_tf = tf.expand_dims(image_tf, axis=0)
        return image_tf

    def predict(self, image: tf.Tensor) -> tf.Tensor:
        if not self.ready:
            raise ModelUninitializedException
        output: tf.Tensor = self._classifier_model(image, training=False)
        return output

    def postprocess(self, image: tf.Tensor, output: tf.Tensor) -> Prediction:
        output_softmax = tf.nn.softmax(output).numpy()
        class_index: int = output_softmax.argmax(-1)[0]
        label = self._map_index_to_label(class_index)
        score: float = output_softmax.max(-1)[0]
        return Prediction(label=label, score=score)

    def load(self, model_archive_path: Union[str, Path], class_names_path: Union[str, Path]) -> None:
        if not self.ready:
            # TODO: We don't support GPU
            # with tf.device(f"/{self._device}:0"):
            self._classifier_model = tf.keras.models.load_model(model_archive_path)
            self._classifier_model.trainable = False
            self._input_shape = self._classifier_model.layers[0].input_shape
            with open(class_names_path, "r") as f:
                self._indexes_to_labels = json.load(f)

    def unload(self) -> None:
        if self.ready:
            self._classifier_model = None
            self._input_shape = None
            self._indexes_to_labels = None
            tf.keras.backend.clear_session()
            gc.collect()

    @property
    def ready(self) -> bool:
        return (
            self._classifier_model is not None
            and self._indexes_to_labels is not None
            and self._input_shape is not None
        )

    def _map_index_to_label(self, index: int) -> str:
        label_raw = self._indexes_to_labels[str(index)]
        return label_raw.replace("_", " ").capitalize()
