from typing import Iterator
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from moto import mock_s3
import pytest
import boto3
from mypy_boto3.s3 import S3ServiceResource

from api.src.main import app as _app
from api.src.core.managers.s3_downloader import S3Downloader
from api.src.core.settings import load_settings, AppSettings
from api.src.core.ml.classifier_model import ClassifierModel
from api.src.core.ml.classifier_files import ClassifierModelFiles
from api.src.core.services.predictions_service import PredictionsService


@pytest.fixture
def app() -> Iterator[FastAPI]:
    yield _app


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as c:
        yield c


def pytest_sessionstart(session: pytest.Session):
    # Get healthcheck to run FastAPI `startup` events,
    # like downloading ML models
    with TestClient(_app) as client:
        client.get(_app.url_path_for("healthcheck"))


@pytest.fixture(scope="session")
def assets_path() -> Path:
    return Path(__file__).parent / "assets"


@pytest.fixture(scope="session")
def test_settings():
    return load_settings()


@pytest.fixture(scope="session")
def classifier_model_files(test_settings: AppSettings):
    return ClassifierModelFiles(
        root_dir_path=test_settings.DATA_LOCAL_DIR,
        model_file_name=test_settings.MODEL_FILE_NAME,
        class_names_file_name=test_settings.CLASS_NAMES_FILE_NAME,
    )


@pytest.fixture(scope="function")
def classifier_model(classifier_model_files: ClassifierModelFiles):
    return ClassifierModel(files=classifier_model_files)


@pytest.fixture(scope="function")
def s3_downloader(test_settings: AppSettings) -> Iterator[S3Downloader]:
    with mock_s3():
        s3_resource_mock: S3ServiceResource = boto3.resource("s3")
        yield S3Downloader(s3_resource_mock, test_settings.BUCKET_NAME)


@pytest.fixture(scope="function")
def predictions_service(classifier_model: ClassifierModel, s3_downloader: S3Downloader, test_settings: AppSettings):
    return PredictionsService(
        model=classifier_model, s3_downloader=s3_downloader, model_s3_location=test_settings.MODEL_DATA_LOCATION_S3
    )
