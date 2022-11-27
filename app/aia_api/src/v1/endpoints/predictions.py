from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, File, UploadFile

from aia_api.src.core.app_container import AppContainer
from aia_api.src.core.services.predictions import PredictionsService
from aia_api.src.core.schemas.predictions import Prediction

router = APIRouter()


@router.post("/", response_model=Prediction)
@inject
async def classify_image(
    image_file: UploadFile = File(), service: PredictionsService = Depends(Provide[AppContainer.prediction_service])
) -> list[Prediction]:
    image_content = await image_file.read()
    return service.predict(image_content)


@router.on_event("startup")
@inject
def setup_model(service: PredictionsService = Depends(Provide[AppContainer.prediction_service])):
    service.setup_model()
