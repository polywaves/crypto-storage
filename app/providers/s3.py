import boto3
from app.config import config


s3_session = boto3.Session(
  aws_access_key_id=config["S3_ACCESS_KEY"],
  aws_secret_access_key=config["S3_SECRET_KEY"]
)

s3 = s3_session.client("s3", endpoint_url=config["S3_URL"])