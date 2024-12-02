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
def test_read_file_obfuscates_for_one_field(file_path, csv_example):

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint":"eu-west-2"})

    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_example)

    file_path = {

"file_to_obfuscate": "s3://test-bucket/test-object",

"pii_fields": ["name"]

}

    result = s3_read_file(file_path)

    assert result == 'name,email\n***,john.doe@example.com\n'


@mock_aws
def test_read_file_obfuscates_for_multiple_fields(file_path, csv_example):

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint":"eu-west-2"})

    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_example)

    result = s3_read_file(file_path)

    assert result == 'name,email\n***,***\n'


@mock_aws
def test_read_file_error_for_non_existent_field(csv_example):

    s3_client = boto3.client("s3", region_name="eu-west-2")

    s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint":"eu-west-2"})

    s3_client.put_object(Bucket="test-bucket", Key="test-object", Body=csv_example)

    file_path['friend'] = 'Kedz'

    with pytest.raises(ClientError, match='Object not found'):
        result = s3_read_file(file_path)


@mock_aws
def test_read_file_error_for_no_pii_fields(csv_example):

    file_path = {

"file_to_obfuscate": "s3://test-bucket/test-object",

"pii_fields": [""]

}

    with pytest.raises(ClientError, match='Specified key does not exists'):
        s3_read_file(file_path)



# @pytest.mark.parametrize(
#     "csv_multiple_examples, expected_output", [
#         (
#             'name,email\njohn Doe,john.doe@example.com\n',

#             'name,email\n***, ***\n'
        
#         ),
#         (
#             'name,email\njane Doe,jane.doe@example.com\n',

#             'name,email\n***, ***\n'

#         ),
#         (
#             'name,email,age\nalbert Alphonso,albert.alphonso@example.com,35\n',

#             'name,email\n***, ***,35\n'

#         ),
#         (
#             'student_id,name,course,graduation_date,email_address\n1111,john Smith, Software,2024-03-31,j.smith@email.com\n',

#             'student_id,name,course,graduation_date,email_address\n1111,***,Software,2024-03-31,***\n'

#         )
#     ]
# )

# @mock_aws
# def test_csv_files_is_obfuscated(conn, csv_multiple_examples, expected_output):

#     conn.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

#     conn.put_object(Bucket="test-bucket", Key="test-object", Body=csv_multiple_examples)

#     input1 = conn.get_object(Bucket="test-bucket", Key="test-object")["Body"].read().decode()

    
#     result = obfuscation_tool(input1)

#     assert result == expected_output
