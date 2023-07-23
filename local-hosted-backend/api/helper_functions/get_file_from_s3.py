import boto3
import os 

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')


def download_file_from_s3(bucket_name: str, s3_file_key: str, local_file_path: str):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    s3.download_file(Bucket=bucket_name, Key=s3_file_key, Filename=local_file_path)

