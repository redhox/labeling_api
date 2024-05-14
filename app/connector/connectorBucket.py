import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv
load_dotenv()

config = Config(
    signature_version= os.getenv("SIGNATURE_VERSION"),
)
s3 = boto3.client(
    's3',
    endpoint_url=os.getenv("ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME"),  # Par exemple, 'us-east-1'
    config=config,
)
class MinioBucketManager:
    def __init__(self):
        self.bucket_name = os.getenv("BUCKET_NAME")

    def upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket"""
        if object_name is None:
            object_name = file_name
        # Upload the file
        s3.upload_file(file_name, self.bucket_name, object_name)

    def list_objects(self):
        """List all objects in the bucket"""
        response = s3.list_objects(Bucket=self.bucket_name)
        for content in response.get('Contents', []):
            print(content['Key'])

