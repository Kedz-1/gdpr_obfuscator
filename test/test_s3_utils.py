#from src.s3_utils import retrieve_s3_file
from src.s3_utils import s3_read_file
import pytest
import boto3
import moto
from moto import mock_aws
import io
import uuid


@pytest.fixture
def s3_client():
    return boto3.client("s3", region_name="eu-west-2")

@pytest.fixture
def csv_example():
    return 'name,email\njohn Doe,john.doe@example.com\n'

@pytest.fixture
def file_path():
    return 's3://test-bucket/test-object'


@mock_aws
def test_read_file(s3_client, csv_example):

    
    s3_client.create_bucket(Bucket="test-bucket12112121212", CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

    s3_client.put_object(Bucket="test-bucket12112121212", Key="test-object", Body=csv_example)

    result = s3_client.get_object(Bucket="test-bucket12112121212", Key="test-object")

    #print(result)
    assert result["Body"].read().decode() == csv_example
    

# @mock_aws
# def test_read_file_valid_s3_path(s3_client, file_path, csv_example):

#     s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

#     s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_example)

#     result = s3_read_file(file_path)

#     assert result == csv_example



    