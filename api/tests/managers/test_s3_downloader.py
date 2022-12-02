import tempfile
from pathlib import Path

import boto3
from mypy_boto3.s3 import S3Client

from api.src.core.managers.s3_downloader import S3Downloader
from api.src.core.settings import AppSettings


def test_download_directory_method(test_settings: AppSettings, s3_downloader: S3Downloader):
    s3_client_mock: S3Client = boto3.client("s3")
    s3_file_location = f"{_S3_DIRECTORY_NAME}/{_S3_FILE_NAME}"
    s3_client_mock.create_bucket(
        Bucket=test_settings.BUCKET_NAME, CreateBucketConfiguration={"LocationConstraint": test_settings.REGION}
    )
    s3_client_mock.put_object(Bucket=test_settings.BUCKET_NAME, Key=s3_file_location, Body=_FILE_CONTENT_MOCK)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        s3_downloader.download_directory_content(_S3_DIRECTORY_NAME, tmp_dir_path)
        file_path = tmp_dir_path / _S3_FILE_NAME

        assert file_path.exists()
        with open(file_path, "r") as f:
            file_content = f.read()
            assert file_content == _FILE_CONTENT_MOCK


_S3_DIRECTORY_NAME = "test"
_S3_FILE_NAME = "test_file.txt"
_FILE_CONTENT_MOCK = "test file content"
