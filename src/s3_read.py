import boto3
from botocore.exceptions import ClientError
import logging

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
            f"Successfully received the content stored in {s3_key}."
        )
        return content

    except ClientError as e:
        # Log an error message if there's an issue accessing the S3
        logging.error(
            f"An error ({e}) has occured whilst trying to access {s3_key}'s content."
        )
        raise