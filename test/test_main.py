from src.main import obfuscated_data
import pytest
import moto
from moto import mock_aws
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import sys


@pytest.fixture
def example_input():
    return {
        "file_to_obfuscate": "s3://test-bucket/test-object",
        "pii_fields": ["name", "email"],
    }


@pytest.fixture
def csv_content():
    return "name,email\njohn Doe,john.doe@example.com\n"


@mock_aws
def test_obfuscated_function_writes_to_s3(example_input, csv_content):

    s3_client = boto3.client("s3", region_name="eu-west-2")
    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_content)

    response = obfuscated_data(example_input)

    result = s3_client.get_object(Bucket="test-bucket", Key="test-object")

    assert result["Body"].read().decode() == "name,email\n***,***\n"


@mock_aws
def test_obfuscated_function_does_not_affect_other_fields(csv_content):

    s3_client = boto3.client("s3", region_name="eu-west-2")
    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_content)

    response = obfuscated_data({
        "file_to_obfuscate": "s3://test-bucket/test-object",
        "pii_fields": ["email"],
    })

    result = s3_client.get_object(Bucket="test-bucket", Key="test-object")

    assert result["Body"].read().decode() == "name,email\njohn Doe,***\n"


@mock_aws
def test_obfuscated_function_no_pii_fields(csv_content):

    s3_client = boto3.client("s3", region_name="eu-west-2")
    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_content)

    example_input = {
        "file_to_obfuscate": "s3://test-bucket/test-object",
        "pii_fields": [],
    }

    with pytest.raises(ValueError, match="No PII fields specified"):
        obfuscated_data(example_input)


@mock_aws
def test_obfuscated_function_invalid_s3_path(example_input):

    example_input = {
        "file_to_obfuscate": "test-bucket/test-object",
        "pii_fields": ["name", "email"],
    }

    with pytest.raises(ValueError, match="The file path must start with 's3://'."):
        obfuscated_data(example_input)


@mock_aws
def test_obfuscated_function_raises_error_on_empty_file(example_input):

    s3_client = boto3.client("s3", region_name="eu-west-2")
    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body="")

    with pytest.raises(
        ValueError, match="The file is empty or contains no data to process"
    ):
        obfuscated_data(example_input)



@mock_aws
def test_obfuscate_function_can_handle_files_up_to_1mb(example_input):
    
    content = ("name,email\njohn Doe,john.doe@example.com\n") *33333

    s3_client = boto3.client('s3', region_name='eu-west-2')
    s3_client.create_bucket(Bucket='test-bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})

    s3_client.put_object(Bucket='test-bucket', Key='test-object', Body=content)

    response = s3_client.head_object(Bucket='test-bucket', Key='test-object')
    size = response['ContentLength']

    start_time = datetime.now()
    result = obfuscated_data(example_input)
    end_time = datetime.now()
    execution_time = end_time - start_time
    
    assert size >= 1000000
    assert execution_time.total_seconds() < 60
    assert '***' in result




















# @mock_aws
# def test_obfuscate_function_works_with_large_files():


# @mock_aws
# def test_obfuscate_function_():


# @mock_aws
# def test_obfuscated_function_has_file_without_pii_fields(csv_content):

#     s3_client = boto3.client('s3', region_name='eu-west-2')
#     s3_client.create_bucket(Bucket='test-bucket', CreateBucketConfiguration={'LocationConstraint' : 'eu-west-2'})
#     s3_client.put_object(Bucket='test-bucket', Key='test-object', Body=csv_content)

#     example_input = {
# "file_to_obfuscate": "s3://test-bucket/test-object",
# "pii_fields": ['friend', 'enemy']
# }

#     with pytest.raises(ValueError, match="'friend' not found in CSV data"):

#         obfuscated_data(example_input)
