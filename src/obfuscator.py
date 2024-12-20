import boto3
import io
from botocore.exceptions import ClientError
import logging
import csv
from io import StringIO


logging.basicConfig(level=logging.INFO) 

def obfuscation_tool(csv_content, pii_fields):

    '''
    Obfuscates sensitive data found within the CSV data.

    Replaces the values of specified fields in the CSV data with '***' to protect sensitive information.

    Args:
        csv_content (str) - The content of the CSV data as a string.

        pii_fields (list) - A list of field names to obfuscate. Fields must match the column headers in the CSV data.

    Returns:
        The obfuscated data as a UTF-8 encoded byte stream 
    
    Raises:
        ValueError: If no pii fields are specified.

        ValueError: If the CSV file is empty.

    Examples:
        >>> csv_content = "name,email\nJohn,john@example.com\n"
        >>> pii_fields = ["name", "email"]
        >>> obfuscation_tool(csv_content, pii_fields)
        b'name,email\n***,***\n'


    '''

    # Raises a value error if no PII/CSV fields are specified
    if not pii_fields:
        raise ValueError("No PII fields specified")

    if len(csv_content) == 0:
        raise ValueError("The file is empty or contains no data to process")

    # Reads the CSV content into a dictionary
    csv_file = StringIO(csv_content)
    csv_reader = csv.DictReader(csv_file)

    obfuscated_data = []

    # Iterates over the content in the CSV data and the specified pii fields to then replace the value of the chosen fields with '***'
    for values in csv_reader:
        for pii in pii_fields:
            if pii in values:
                values[pii] = "***"
        obfuscated_data.append(values)

    # Converts obfuscated data back to CSV format
    convert_to_csv = StringIO(newline="")

    field_names = obfuscated_data[0].keys()

    csv_format = csv.DictWriter(convert_to_csv, fieldnames=field_names)

    csv_format.writeheader()
    csv_format.writerows(obfuscated_data)

    # Get CSV as a string and replace'\r\n' with '\n' for consistency
    result = convert_to_csv.getvalue()
    result = result.replace("\r\n", "\n")

    # Convert the result to utf-8 encoded byte stream
    byte_stream = result.encode("utf-8")

    logging.info(f"Successfully received the CSV content")

    return byte_stream
