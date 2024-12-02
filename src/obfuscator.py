import boto3
import io 
from botocore.exceptions import ClientError
import logging
import csv
from io import StringIO


logging.basicConfig(level=logging.INFO)

def s3_read_file(input_data, region="eu-west-2"):

    s3_client = boto3.client("s3", region_name = region)

    file_path = input_data['file_to_obfuscate'] 
    pii_fields = input_data['pii_fields']


    if not file_path.startswith('s3://'):
        raise ValueError('The file path must start with \'s3://\'. ')
    
    paths = file_path[5:].split('/', 1)
    #print(paths)
    
    if len(paths) != 2:
        raise ValueError('Path must contain a bucket and an object.')
    
    s3_bucket = paths[0]
    s3_object = paths[1]

    try:
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_object)["Body"].read().decode()


        csv_file = StringIO(response)
        csv_reader = csv.DictReader(csv_file)

        for pii in csv_reader:
            if pii['name']:
                pii['name'] = '***'
            #print(pii)
            print(csv_reader)


        logging.info(f'Successfully received the content stored in {s3_object} - {response}')
        return response
    
    except ClientError as e:
        logging.error(f'An error has occured whilst trying to access {s3_object}\'s content in {s3_bucket}.')
        raise

print(s3_read_file({
"file_to_obfuscate": "s3://masking-test-bucket/masking-test-object",
"pii_fields": ["name", "email_address"]
}))

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

data = {
"file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
"pii_fields": ["name", "email_address"]
}

file_path = data["file_to_obfuscate"]
pii_fields = data["pii_fields"]

#print(file_path)
#print(pii_fields)

paths = file_path[5:].split('/', 1)

# print(paths)