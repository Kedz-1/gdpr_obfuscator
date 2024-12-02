from src.obfuscator import s3_read_file
import pytest
import boto3
import moto
from moto import mock_aws
from botocore.exceptions import ClientError


@pytest.fixture
def s3_client():
    return boto3.client("s3", region_name="eu-west-2")

@pytest.fixture
def csv_example():
    return 'name,email\njohn Doe,john.doe@example.com\n'

@pytest.fixture
def file_path():
    return {

"file_to_obfuscate": "s3://test-bucket/test-object",

"pii_fields": ["name", "email_address"]

}


@mock_aws
def test_read_file_valid_s3_path(file_path, csv_example):

    s3_client = boto3.client("s3", region_name ="eu-west-2")

    s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_example)

    result = s3_read_file(file_path)

    assert result == csv_example


@mock_aws
def test_read_file_raises_exception_for_invalid_s3():
    
    file_path = {

"file_to_obfuscate": "test-bucket/test-object",

"pii_fields": ["name", "email_address"]

}

    with pytest.raises(ValueError, match='The file path must start with \'s3://\'.'):
        s3_read_file(file_path)


@mock_aws
def test_read_file_raises_exception_for_no_object():

    file_path = {

"file_to_obfuscate": "s3://test-bucket",

"pii_fields": ["name", "email_address"]

}

    with pytest.raises(ValueError, match='Path must contain a bucket and an object.'):
        s3_read_file(file_path)


@mock_aws
def test_read_file_no_object_found(file_path):

    s3_client = boto3.client('s3', region_name='eu-west-2')

    s3_client.create_bucket(Bucket='test-bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})

    with pytest.raises(ClientError, match="The specified key does not exist"):
        s3_read_file(file_path)


@mock_aws
def test_read_file_no_path():

    with pytest.raises(ValueError, match="The file path must start with 's3://'. "):
        s3_read_file({
            'file_to_obfuscate' : '',
            
            'pii_fields' : ['name', 'email']
        })


@mock_aws
def test_read_file_has_a_non_existent_bucket():

    file_path = {

"file_to_obfuscate": "s3://non-existent-bucket/test-object",

"pii_fields": ["name", "email_address"]

}

    with pytest.raises(ClientError, match = 'The specified bucket does not exist'):
        s3_read_file(file_path)
