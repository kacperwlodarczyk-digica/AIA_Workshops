from api.src.core.ml.classifier_model import ClassifierModel
from api.src.core.managers.s3_downloader import S3Downloader


class PredictionsService:
    def __init__(self, model: ClassifierModel, s3_downloader: S3Downloader, model_s3_location: str):
        self._model = model
        self._s3_downloader = s3_downloader
        self._model_s3_location = model_s3_location

    def predict(self, image_content: bytes):
        # TODO YOUR CODE HERE
        # Run test: pytest tests/services/test_predictions_service.py -k "test_predict_method"
        ... # remove after implementing the code

    def setup_model(self):
        # TODO YOUR CODE HERE
        # Run test: pytest tests/services/test_predictions_service.py -k "test_setup_model_method"
        ... # remove after implementing the code

    def _download_model_files(self):
        if not self._check_model_files_exists():
            self._model.files.root_dir_path.mkdir(parents=True, exist_ok=True)
            self._s3_downloader.download_directory_content(self._model_s3_location, self._model.files.root_dir_path)

    def _check_model_files_exists(self) -> bool:
        return self._model.files.class_names_file_path.exists() and self._model.files.model_file_path.exists()
