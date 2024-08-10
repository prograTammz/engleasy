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

async def upload_audio_s3(audio_data: BytesIO) -> str:
    try:
        audio_data.seek(0)
        # Generate a random filename using UUID
        file_name = f"{uuid.uuid4()}.mp3"

        # Upload the file to S3
        s3_client.put_object(Body=audio_data, Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_name,  ContentType='audio/mpeg')

        return  f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
    except Exception as e:
            return {"error from aws": str(e)}