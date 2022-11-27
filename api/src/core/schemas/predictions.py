from __future__ import annotations

from pydantic import BaseModel, confloat


SCORE_TYPE = confloat(ge=0, le=1)


class Prediction(BaseModel):
    label: str
    score: SCORE_TYPE
