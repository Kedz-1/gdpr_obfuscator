import boto3
import io
from botocore.exceptions import ClientError
import logging
import csv
from io import StringIO

logging.basicConfig(level=logging.INFO)

def read_s3(file_path, region="eu-west-2"):

    '''
    This function reads content from an object stored within an S3 object located at the given file. The content returned is a UTF-8 decoded string.sucessfuly

    Args:
        file_path (str) - Takes an S3 file path including a bucket and key.

        region (str) - Specifies the region where the S3 bucket is located. Defaults to eu-west-2.
    
    Returns:
        The content stored in the S3 as a string.
    
    Raises:
        ValueError:
            - If the file path is not a valid S3 URI
            - If the file path does not contain a bucket/key

        ClientError:
            - If the S3 object can't be accessed
    
    Logs:
        - Logs a success message if the object content is successfully retrieved.
        - Logs an error message if there is an issue retrieving the S3 object.
        
    Examples:
        >>> file_path = 's3://test-bucket/test-key'
        >>> read_s3(file_path)
        'This is the content stored in the S3 object.'

        >>> file_path = 'invalid-path'
        >>> read_s3(file_path)
        ValueError: The file path must start with 's3://'.
    '''

    s3_client = boto3.client("s3", region_name=region)

    # Validate that the file path 
    if not file_path.startswith("s3://"):
        raise ValueError("The file path must start with 's3://'. ")

    # Extract the bucket and key from the file path
    paths = file_path[5:].split("/", 1)

    # Checks that both the bucket and key are present
    if len(paths) != 2:
        raise ValueError("Path must contain a bucket and an object.")

    s3_bucket = paths[0]
    s3_key = paths[1]

    try:
        # Attempt to retrieve the object
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)

        # Read the object content and decode it into a string
        content = response["Body"].read().decode()

        #Logs a success message on retrieving the content
        logging.info(
            f"Successfully received the content stored in {s3_key} - {content}"
        )
        return content

    except ClientError as e:
        # Log an error message if there's an issue accessing the S3
        logging.error(
            f"An error ({e}) has occured whilst trying to access {s3_key}'s content."
        )
        raise

# print(read_s3('s3://kedz-test-bucket/test-object'))


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


# print(write_s3('s3://kedz-test-bucket/kedz-test-object', 'hi'))



# def create_bucket(bucket, region='eu-west-2'):
#     s3_client = boto3.client('s3', region_name=region)

#     try:
#         s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': region})
#         logging.info('Successfully created bucket')
#         return True

#     except ClientError as e:
#         logging.error('Failed to upload large bucket')

# create_bucket('kedz-test-large-bucket')

def write_to_s3(bucket, key, content):
    s3_client = boto3.client('s3', region_name='eu-west-2')

    try:
        s3_client.put_object(Bucket=bucket, Key=key, Body= content)
        logging.info('Successfully put object')
        return True
    except ClientError as e:
        logging.error('Failed to upload large key')

write_to_s3('kedz-test-large-bucket', 'kedz-test-large-key.csv', ("name,email\njohn Doe,john.doe@example.com\n") * 33333)
