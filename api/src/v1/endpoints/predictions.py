from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, File, UploadFile

from api.src.core.app_container import AppContainer
from api.src.core.services.predictions_service import PredictionsService
from api.src.core.schemas.predictions import Prediction


router = APIRouter()


@router.on_event("startup")
@inject
def setup_model(service: PredictionsService = Depends(Provide[AppContainer.prediction_service])):
    # TODO YOUR CODE HERE
    ... # remove after implementing the code


@router.post("/", response_model=Prediction)
@inject
async def predict(
    image_file: UploadFile = File(), service: PredictionsService = Depends(Provide[AppContainer.prediction_service])
) -> Prediction:
    # TODO YOUR CODE HERE
    # Run test: pytest tests/v1/endpoints/test_predictions.py -k "test_predict_endpoint"
    ... # remove after implementing the code
