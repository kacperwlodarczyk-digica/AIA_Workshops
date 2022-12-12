import pytest
from pydantic.error_wrappers import ValidationError

from api.src.core.schemas.predictions import Prediction


def test_prediction_score_value_validator():
    with pytest.raises(ValidationError) as e:
        Prediction(label="test", score=10)
