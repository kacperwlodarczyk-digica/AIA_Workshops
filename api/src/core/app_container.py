import boto3
from botocore.config import Config
from dependency_injector import containers
from dependency_injector.providers import Singleton, Resource

from api.src.core.services.predictions_service import PredictionsService
from api.src.core.managers.s3_downloader import S3Downloader
from api.src.core.ml.classifier_model import ClassifierModel
from api.src.core.ml.classifier_files import ClassifierModelFiles
from api.src.core.settings import load_settings


class AppContainer(containers.DeclarativeContainer):
    """APP Container with all the resources"""

    # WiringConfiguration provides a way to inject container providers into the functions and methods
    # As we're using providers in endpoints package (via FastAPI Depends()), we need to add this package to the configuration
    # Then, we can inject our providers to the endpoints (using @inject decorator)
    wiring_config = containers.WiringConfiguration(packages=["api.src.v1.endpoints"])

    settings = load_settings()

    # AWS
    session = Resource(boto3.session.Session, region_name=settings.REGION)
    s3_downloader = Singleton(
        S3Downloader,
        s3_resource=session.provided.resource.call(service_name="s3", config=Config(signature_version="s3v4")),
        bucket_name=settings.BUCKET_NAME,
    )

    # Models
    classifier_files: Singleton[ClassifierModelFiles] = Singleton(
        ClassifierModelFiles,
        root_dir_path=settings.DATA_LOCAL_DIR,
        model_file_name=settings.MODEL_FILE_NAME,
        class_names_file_name=settings.CLASS_NAMES_FILE_NAME,
    )
    classifier_model: Singleton[ClassifierModel] = Singleton(ClassifierModel, files=classifier_files)

    # Services
    prediction_service: Singleton[PredictionsService] = Singleton(
        PredictionsService,
        model=classifier_model,
        s3_downloader=s3_downloader,
        model_s3_location=settings.MODEL_DATA_LOCATION_S3,
    )
