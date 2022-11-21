from dependency_injector import containers
from dependency_injector.providers import Singleton

from aia_api.src.core.services.predictions import PredictionService
from aia_api.src.core.ml_models.classifier import ClassifierModel
from aia_api.src.core.settings import load_settings


class AppContainer(containers.DeclarativeContainer):
    """APP Container with all the providers"""

    # WiringConfiguration provides a way to inject container providers into the functions and methods
    # As we're using providers in endpoints package (via FastAPI Depends()), we need to add this package to the configuration
    # Then, we can inject our providers to the endpoints (using @inject decorator)
    wiring_config = containers.WiringConfiguration(packages=["api.src.v1.endpoints"])

    settings = load_settings()

    # Model
    classifier_model: Singleton[ClassifierModel] = Singleton(ClassifierModel, device=settings.DEVICE)
    # Services
    prediction_service: Singleton[PredictionService] = Singleton(PredictionService, classifier_model=classifier_model)
