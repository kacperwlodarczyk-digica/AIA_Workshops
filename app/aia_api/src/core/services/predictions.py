from aia_api.src.core.models.classifier import ClassifierModel
from aia_api.src.core.managers.s3_downloader import S3Downloader


class PredictionsService:
    def __init__(self, model: ClassifierModel, s3_downloader: S3Downloader, model_s3_location: str):
        self._model = model
        self._s3_downloader = s3_downloader
        self._model_s3_location = model_s3_location

    def predict(self, image_content: bytes):
        return self._model(image_content)

    def setup_model(self):
        self._download_model_files()
        if not self._check_model_files_exists():
            raise FileNotFoundError(
                f"Model files under `{self._model.files.root_dir_path}` directory does not exists!"
            )
        self._model.load()

    def _download_model_files(self):
        if not self._check_model_files_exists():
            self._model.files.root_dir_path.mkdir(parents=True, exist_ok=True)
            self._s3_downloader.download_directory(self._model_s3_location, self._model.files.root_dir_path)

    def _check_model_files_exists(self) -> bool:
        return self._model.files.class_names_file_path.exists() and self._model.files.model_file_path.exists()
