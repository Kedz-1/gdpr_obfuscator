import boto3
import io 
from botocore.exceptions import ClientError
import logging
import csv
from io import StringIO


logging.basicConfig(level=logging.INFO)

def obfuscation_tool(csv_content, pii_fields):

    if not pii_fields:
            raise ValueError ('No PII fields specified')
        

    csv_file = StringIO(csv_content)
    csv_reader = csv.DictReader(csv_file)

    obfuscated_data = []

    for values in csv_reader:
        for pii in pii_fields:
            if pii in values:
                values[pii] = '***'
            else:
                raise ValueError(f"'{pii}' not found in CSV data")

        obfuscated_data.append(values)
        
    convert_to_csv = StringIO(newline='')

    field_names = obfuscated_data[0].keys()

    csv_format = csv.DictWriter(convert_to_csv, fieldnames=field_names)

    csv_format.writeheader()

    csv_format.writerows(obfuscated_data)

    result = convert_to_csv.getvalue()

    result = result.replace('\r\n', '\n')

    logging.info(f'Successfully received the CSV content')

    return result