from pathlib import Path
import logging

from mypy_boto3.s3 import S3ServiceResource


logger = logging.getLogger(__file__)


class S3Downloader:
    def __init__(self, s3_resource: S3ServiceResource, bucket_name: str):
        self._bucket = s3_resource.Bucket(bucket_name)

    def download_directory_content(self, s3_location: str, local_destination: Path):
        """Download all the content from s3_location to local_destination."""
        for obj in self._bucket.objects.filter(Prefix=s3_location):
            if not obj.key.endswith("/"):
                obj_local_path = local_destination / obj.key.lstrip(s3_location).lstrip("/")
                obj_local_path.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"Downloading file {obj.key} from S3 to {obj_local_path}.")
                self._bucket.download_file(obj.key, str(obj_local_path))
