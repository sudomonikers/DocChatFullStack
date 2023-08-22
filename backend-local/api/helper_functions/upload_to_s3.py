import boto3
import os 

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')


def upload_file_to_aws(local_file: str, bucket: str, s3_file: str):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    s3.upload_file(local_file, bucket, s3_file)

if __name__ == "__main__":
    #example usage
    upload_file_to_aws("test.pdf", "example-bucket", "test.pdf")