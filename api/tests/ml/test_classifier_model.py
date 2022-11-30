from pathlib import Path

import tensorflow as tf
import numpy as np

from api.src.core.ml.classifier_model import ClassifierModel
from api.src.core.schemas.predictions import Prediction


def test_load_method(classifier_model: ClassifierModel):
    assert not classifier_model.ready
    classifier_model.load()
    assert classifier_model.ready


def test_preprocess_method(classifier_model: ClassifierModel, assets_path: Path):
    classifier_model.load()
    with open(assets_path / HEALTHLY_IMAGE_NAME, mode="rb") as f:
        image_content = f.read()
    image_tf = classifier_model.preprocess(image_content)
    assert isinstance(image_tf, tf.Tensor)

    image_np = image_tf.numpy()
    expected_image_preprocessed_np = np.load(assets_path / _HEALTHLY_IMAGE_PREPROCESSED_NAME)

    assert image_np.shape == expected_image_preprocessed_np.shape
    assert np.allclose(image_np, expected_image_preprocessed_np, atol=0.005)


def test_predict_method(classifier_model: ClassifierModel, assets_path: Path):
    classifier_model.load()
    image_preprocessed_np = np.load(assets_path / _HEALTHLY_IMAGE_PREPROCESSED_NAME)
    image_preprocessed_tf: tf.Tensor = tf.convert_to_tensor(image_preprocessed_np)
    output = classifier_model.predict(image_preprocessed_tf)

    assert isinstance(output, tf.Tensor)
    output_softmax = tf.nn.softmax(output).numpy()
    class_index: int = output_softmax.argmax(-1)[0]
    class_label = classifier_model._indexes_to_labels[str(class_index)]
    assert class_label == "healthy"


def test_map_index_to_label(classifier_model: ClassifierModel):
    classifier_model.load()
    assert classifier_model._map_index_to_label(1) == "Frog eye leaf spot"


def test_postprocess_method(classifier_model: ClassifierModel, assets_path: Path):
    classifier_model.load()
    image_preprocessed_np = np.load(assets_path / _HEALTHLY_IMAGE_PREPROCESSED_NAME)
    image_preprocessed_tf: tf.Tensor = tf.convert_to_tensor(image_preprocessed_np)
    output = classifier_model.predict(image_preprocessed_tf)
    prediction = classifier_model.postprocess(image_preprocessed_tf, output)
    assert isinstance(prediction, Prediction)
    assert prediction.label.lower() == "healthy"


HEALTHLY_IMAGE_NAME = "healthy.jpg"
_HEALTHLY_IMAGE_PREPROCESSED_NAME = "healthy_preprocessed.npy"
