from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, File, UploadFile

from api.src.core.app_container import AppContainer
from api.src.core.services.predictions_service import PredictionsService
from api.src.core.schemas.predictions import Prediction


router = APIRouter()


@router.on_event("startup")
@inject
def setup_model(service: PredictionsService = Depends(Provide[AppContainer.prediction_service])):
    service.setup_model()


@router.post("/", response_model=Prediction)
@inject
async def predict(
    image_file: UploadFile = File(), service: PredictionsService = Depends(Provide[AppContainer.prediction_service])
) -> Prediction:
    image_content = await image_file.read()
    return service.predict(image_content)

