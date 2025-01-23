from src.obfuscator import obfuscation_tool
from src.s3_read import read_s3
from src.s3_write import write_s3
from src.main import obfuscated_data
import boto3
from botocore.exceptions import ClientError
import logging
import json

logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):

    try:

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        # pii_fields = event['pii_fields']

        if key.endswith('masked.csv'):
            logging.info('file already obfuscated')
            return {
                'statusCode': 200,
                'body': 'File already obfuscated'
            }
            
        pii_fields = ['name', 'email']  
        file_path = f's3://{bucket}/{key}'

        lambda_obfuscated_data = {
            "file_to_obfuscate":file_path,
            "pii_fields":pii_fields
            }
        
        result = obfuscated_data(lambda_obfuscated_data)
        logging.info('Successfully obfuscated the data')
        return {
            'statusCode': 200,
            'body': json.dumps(result)
            }
    
    except ClientError as e:
        logging.error(f'Client error occured {e}')
        return {
            'statusCode': 500,
            'body': f'Failed to obfuscate content: {e}'
        }


'''
{
  "file_to_obfuscate": "s3://kedz-tf-test-bucket/sample.csv",
  "pii_fields": ["name", "email"]
}
'''