import gc
from typing import Optional
import json

import tensorflow as tf

from aia_api.src.core.schemas.predictions import Prediction
from aia_api.src.core.models.files import ClassifierModelFiles


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

    def preprocess(self, image_content: bytes):
        height, width, n_channels = self._input_shape[-3:]
        image_tf: tf.Tensor = tf.image.decode_image(image_content, channels=n_channels, expand_animations=False)
        image_tf = tf.image.resize(image_tf, (height, width))
        image_tf /= 255
        image_tf = tf.expand_dims(image_tf, axis=0)
        return image_tf

    def predict(self, image: tf.Tensor):
        if not self.ready:
            raise RuntimeError("Model not loaded!")
        output: tf.Tensor = self._classifier_model(image, training=False)
        return output

    def postprocess(self, image: tf.Tensor, output: tf.Tensor):
        output_softmax = tf.nn.softmax(output).numpy()
        class_index: int = output_softmax.argmax(-1)[0]
        label = self._map_index_to_label(class_index)
        score: float = output_softmax.max(-1)[0]
        return Prediction(label=label, score=score)

    def load(self):
        if not self.ready:
            self._classifier_model = tf.keras.models.load_model(self.files.model_file_path, compile=False)
            self._classifier_model.trainable = False
            self._input_shape = self._classifier_model.layers[0].input_shape
            with open(self.files.class_names_file_path, "r") as f:
                self._indexes_to_labels = json.load(f)

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
