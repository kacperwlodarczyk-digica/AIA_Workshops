from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, File, UploadFile

from api.src.core.app_container import AppContainer
from api.src.core.services.predictions import PredictionService
from api.src.core.schemas.predictions import Prediction

router = APIRouter()


@router.post("/", response_model=Prediction)
@inject
async def classify_image(
    image_file: UploadFile = File(), service: PredictionService = Depends(Provide[AppContainer.prediction_service])
) -> Prediction:
    image_content = await image_file.read()
    return service.predict(image_content)


@router.on_event("startup")
@inject
def load_model(service: PredictionService = Depends(Provide[AppContainer.prediction_service])) -> bool:
    return service.load_model()