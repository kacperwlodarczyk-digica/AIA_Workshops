from pathlib import Path

from mypy_boto3.s3 import S3ServiceResource


class S3Downloader:
    def __init__(self, s3_resource: S3ServiceResource, bucket_name: str):
        self._bucket = s3_resource.Bucket(bucket_name)

    def download_directory_content(self, s3_location: str, local_destination: Path) -> None:
        """Download all the content from s3_location to local_destination."""
        # TODO YOUR CODE HERE
        # Run test: pytest tests/managers/test_s3_downloader.py -k "test_download_directory_method"
        ... # remove after implementing the code
