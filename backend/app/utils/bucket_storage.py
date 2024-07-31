from fastapi import File
import boto3
import os
from io import BytesIO
import uuid

# GET
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get(
    'AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# Defines the AWS S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME
)

async def upload_audio_s3(file, audio_data) -> str:
    try:
        # Generate a random filename using UUID
        file_extension = file.filename.split('.')[-1]
        random_filename = f"{uuid.uuid4()}.{file_extension}"

        # Upload the file to S3
        s3_client.upload_fileobj(BytesIO(audio_data), AWS_STORAGE_BUCKET_NAME, random_filename)

        return  f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{random_filename}"
    except Exception as e:
            return {"error from aws": str(e)}