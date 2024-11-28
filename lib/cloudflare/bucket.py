from django.core.cache import cache

import boto3
from botocore.client import Config
from botocore.errorfactory import ClientError
from dataplane import s3_download, s3_upload

from apps.system.core.classes import SingletonMeta
from utils.env import get_env_var

DEFAULT_BUCKET = get_env_var("CLOUDFLARE_R2_BUCKET")

class R2CloudflareHandler(metaclass=SingletonMeta):
    def __init__(self):
        access_key = get_env_var("CLOUDFLARE_R2_BUCKET_ACCESS_KEY")
        secret_access_key = get_env_var("CLOUDFLARE_R2_BUCKET_SECRET_ACCESS_KEY")
        url = get_env_var("CLOUDFLARE_R2_BUCKET_URL")

        self.client = boto3.client(
            "s3",
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )

    def upload(self, file, path, bucket=DEFAULT_BUCKET):
        upload = s3_upload(
            Bucket=bucket,
            S3Client=self.client,
            TargetFilePath=path,
            UploadObject=file.read(),
            UploadMethod="Object",
        )
        return upload

    def download(self, path):
        cache_image = cache.get(path)
        if cache_image:
            return cache_image

        try:
            response = s3_download(
                Bucket=get_env_var("CLOUDFLARE_R2_BUCKET"),
                S3Client=self.client,
                S3FilePath=path,
                DownloadMethod="Object",
            )
        except ClientError:
            return None

        cache.set(path, response["content"], 60 * 60 * 24)

        return response["content"]

    def delete(self, path):
        self.client.delete_object(Bucket=get_env_var("CLOUDFLARE_R2_BUCKET"), Key=path)
        if cache.has_key(path):
            cache.delete(path)
