import os
import boto3
from config import Config


class S3Client:
    def __init__(
            self, 
            access_key: str, 
            secret_key: str,
            endpoint_url: str,
            bucket_name: str
        ):
        self.bucket_name = bucket_name
        self.session = boto3.session.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='ru-central1'
        )
        self.client = self.session.client(
            service_name='s3',
            endpoint_url=endpoint_url
        )

    def upload_file(
            self, 
            file_path: str, 
        ):
        self.client.upload_file(
            file_path, 
            self.bucket_name, 
            os.path.basename(file_path)
        )

def save_data_to_s3(access_key: str, secret_key: str):
    s3_client = S3Client(
        access_key=access_key,
        secret_key=secret_key,
        endpoint_url='https://storage.yandexcloud.net',
        bucket_name='cbr-press-release-classifier'
    )

    for root, _, files in os.walk("../data/"):
        for file in files:
            if file.endswith('.csv'):
                path_to_data = os.path.join(root, file)

                s3_client.upload_file(path_to_data)
