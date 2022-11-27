from pathlib import Path

import boto3
import mypy_boto3_s3.service_resource as s3_resources


class S3Downloader:
    def __init__(self, bucket_name: str):
        self._bucket: s3_resources.Bucket = boto3.resource("s3").Bucket(bucket_name)

    def download_directory(self, s3_location: str, local_destination: Path):
        """Download all the content from s3_location to local_destination."""
        for obj in self._bucket.objects.filter(Prefix=s3_location):
            if not obj.key.endswith("/"):
                obj_local_path = local_destination / obj.key.lstrip(s3_location).lstrip("/")
                obj_local_path.parent.mkdir(parents=True, exist_ok=True)
                self._bucket.download_file(obj.key, str(obj_local_path))
