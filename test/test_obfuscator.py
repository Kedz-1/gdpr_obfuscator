from src.obfuscator import obfuscation_tool
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
def pii_fields():
    return ["name", "email"]


@mock_aws
def test_read_file_obfuscates_for_one_field(csv_example):

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint":"eu-west-2"})

    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_example)

    result = obfuscation_tool(csv_example, ["name"])

    assert result.decode('utf-8') == 'name,email\n***,john.doe@example.com\n'


@mock_aws
def test_read_file_obfuscates_for_multiple_fields(pii_fields, csv_example):

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint":"eu-west-2"})

    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_example)

    result = obfuscation_tool(csv_example, pii_fields)

    assert result.decode('utf-8') == 'name,email\n***,***\n'


# @mock_aws
# def test_read_file_error_for_non_existent_field(csv_example, pii_fields):

#     s3_client = boto3.client("s3", region_name="eu-west-2")

#     s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint":"eu-west-2"})

#     s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_example)

#     pii_fields.append('friend')
    
#     with pytest.raises(ValueError, match="'friend' not found in CSV data"):
#         obfuscation_tool(csv_example, pii_fields)


@mock_aws
def test_read_file_error_for_no_pii_fields(csv_example):

    s3_client = boto3.client("s3", region_name = "eu-west-2")

    s3_client.create_bucket(Bucket='test-bucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})

    s3_client.put_object(Bucket='test-bucket', Key='test-object', Body=csv_example)


    with pytest.raises(ValueError, match='No PII fields specified'):
        obfuscation_tool(csv_example, [])



@pytest.mark.parametrize(
    "csv_multiple_examples, expected_output", [
        (
            'name,email\njohn Doe,john.doe@example.com\n',

            'name,email\n***,***\n'
        
        ),
        (
            'name,email\njane Doe,jane.doe@example.com\n',

            'name,email\n***,***\n'

        ),
        (
            'name,email,age\nalbert Alphonso,albert.alphonso@example.com,35\n',

            'name,email,age\n***,***,35\n'

        ),
        (
            'student_id,name,course,graduation_date,email\n1111,john Smith, Software,2024-03-31,j.smith@email.com\n',

            'student_id,name,course,graduation_date,email\n1111,***, Software,2024-03-31,***\n'

        )
    ]
)

@mock_aws
def test_read_files_obfuscates_parametrize_fields( csv_multiple_examples, expected_output, csv_example, pii_fields):

    s3_client = boto3.client("s3", region_name = "eu-west-2")

    s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_multiple_examples)

    input1 = s3_client.get_object(Bucket="test-bucket", Key="test-object")["Body"].read().decode()

    
    result = obfuscation_tool(input1, pii_fields)

    assert result.decode('utf-8') == expected_output
