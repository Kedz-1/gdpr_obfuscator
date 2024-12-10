import boto3
import io 
from botocore.exceptions import ClientError
import logging
import csv
from io import StringIO

logging.basicConfig(level=logging.INFO)

def read_s3(file_path, region="eu-west-2"):

    s3_client = boto3.client("s3", region_name = region)

    if not file_path.startswith('s3://'):
        raise ValueError('The file path must start with \'s3://\'. ')
    
    paths = file_path[5:].split('/', 1)

    if len(paths) != 2:
        raise ValueError('Path must contain a bucket and an object.')
    
    s3_bucket = paths[0]
    s3_object = paths[1]

    try:
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_object)
        content = response["Body"].read().decode()
        logging.info(f'Successfully received the content stored in {s3_object} - {content}')
        return content
    
    except ClientError as e:
        logging.error(f'An error ({e}) has occured whilst trying to access {s3_object}\'s content.')
        raise

# print(read_s3('s3://kedz-test-bucket/test-object'))

def write_s3(bucket, key, content, region='eu-west-2'):

    s3_client = boto3.client('s3', region_name=region)

    try:
        s3_client.put_object(Bucket=bucket, Key=key, Body=content)
        logging.info(f'Successfully wrote obfuscated data to {key} in {bucket}')
    
    except ClientError as e:
        logging.error(f'Failed to write obfuscated data to S3: {e}')
        raise


'''
In the first instance, it is only necessary to be able to process CSV data.

The tool will be invoked by sending a JSON string containing:
•the S3 location of the required CSV file for obfuscation

•the names of the fields that are required to be obfuscated

    {
"file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
"pii_fields": ["name", "email_address"]
}
'''


# def make_bucket(bucket_name, region="eu-west-2"):
    
#     s3_client = boto3.client("s3", region_name=region)

#     try:
#         response = s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint":region})

#         print(f'{bucket_name} created successfully.')
#         return response

    
#     except Exception as e:
#         print(f'An error has occured while creating the bucket: {e}.')
#         raise

# make_bucket("thisisgoingtobemytestbucket11111")


# def put_object(bucket_name, object_name, content, region="eu-west-2"):

#     s3_client = boto3.client("s3", region_name=region)

#     try:
#         response = s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=content)

#         print(f'{object_name} created successfully.')
#         return response
    
#     except Exception as e:
#         print(f'An error has occured whilst creating an object: {e}.')
#         raise

# put_object('thisisgoingtobemytestbucket', 'thisismytestprefix/thisismytestobject', 'hi')


# def get_object(bucket_name, object_name, region='eu-west-2' ):

#     s3_client = boto3.client("s3", region_name=region)

#     try:
#         response = s3_client.get_object(Bucket=bucket_name, Key=object_name)["Body"].read().decode()

#         print(f'Successfully collected {object_name}\'s content.')
#         print(response)
#         return response
        
#     except Exception as e:
#         print(f'There has been an error trying to collect the content of {bucket_name}.')
#         raise


# get_object('thisisgoingtobemytestbucket', 'thisismytestprefix/thisismytestobject')