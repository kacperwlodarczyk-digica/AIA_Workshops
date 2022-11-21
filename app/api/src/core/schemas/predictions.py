from pydantic import BaseModel


class Prediction(BaseModel):
    label: str
    score: float
