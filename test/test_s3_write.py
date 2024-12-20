from src.s3_utils import write_s3
import pytest
import boto3
import moto
from moto import mock_aws
from botocore.exceptions import ClientError
import logging


@mock_aws
def test_write_to_s3_inputs_data_to_s3():

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    write_s3("test-bucket", "test-object", "hi")

    response = s3_client.get_object(Bucket="test-bucket", Key="test-object")

    result = response["Body"].read().decode()

    assert result == "hi"


@mock_aws
def test_write_to_s3_error_for_incorrect_bucket():

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    with pytest.raises(ClientError, match="The specified bucket does not exist"):
        write_s3("non-existent-bucket", "test-object", "hi")


@mock_aws
def test_write_to_s3_value_error_for_no_bucket():

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    with pytest.raises(ValueError, match="The specified bucket does not exist"):
        write_s3("", "test-object", "hi")


@mock_aws
def test_write_to_s3_error_for_incorrect_key():

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    
    with pytest.raises(ValueError, match="The specified key does not exist"):
        write_s3("test-bucket", "", "hi")


@mock_aws
def test_write_to_s3_empty_body():

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    write_s3("test-bucket", "test-object", "")

    response = s3_client.get_object(Bucket="test-bucket", Key="test-object")

    assert response["Body"].read().decode() == ""


@mock_aws
def test_write_s3_logs_on_success(caplog):

    caplog.set_level(logging.INFO)

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    write_s3("test-bucket", "test-object", "hi")

    assert (
        "Successfully wrote obfuscated data to test-object in test-bucket"
        in caplog.text
    )


@mock_aws
def test_write_s3_logs_on_fail(caplog):

    caplog.set_level(logging.ERROR)

    with pytest.raises(ClientError):
        write_s3("non-existent-object", "test-bucket", "hi")

    assert "Failed to write obfuscated data to S3" in caplog.text


@mock_aws
def test_write_s3_works_with_large_files():

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    large_content = "a" * (100 * 100 * 100)

    write_s3("test-bucket", "test-object", large_content)

    response = s3_client.get_object(Bucket="test-bucket", Key="test-object")

    assert response["Body"].read().decode() == large_content
