import boto3
from botocore.exceptions import ClientError
import logging


def write_s3(bucket, key, content, region="eu-west-2"):
    '''
    This function uploads content to a specified S3 bucket and key. 

    Args:
        bucket (str) - The name of the S3 bucket where the content will be stored.

        key (str) - The key in the bucket where the content will be uploaded.

        content (str) - The data to upload to the S3 object.

        region (str) - Specifies the region where the S3 bucket is located. Defaults to eu-west-2.
    
    Raises:
        ValueError - If the bucket is empty or inavlid.

        ClientError - If an error occurs whilst trying to upload data to the S3.

    Logs:
        - A success message if the content is successfully written to the S3 object.

        - An error message if the upload fails.

    '''
    s3_client = boto3.client("s3", region_name=region)

    # check that the bucket name is provided
    if not bucket:
        raise ValueError("The specified bucket does not exist")

    if not key:
        raise ValueError("The specified key does not exist")
    try:
        # Uploads content to the specified bucket and key
        s3_client.put_object(Bucket=bucket, Key=key, Body=content)
        logging.info(f"Successfully wrote obfuscated data to {key} in {bucket}")

    except ClientError as e:
        # Log and re-raise error if the operation fails
        logging.error(f"Failed to write obfuscated data to S3: {e}")
        raise