from src.obfuscator import obfuscation_tool
from src.s3_utils import read_s3
from src.s3_utils import write_s3


def obfuscated_data(input_data, region="eu-west-2"):

    '''
    Processes a CSV file saved in S3, obfuscates the content stored within the object and then writes it back to the S3 file path with a new key.

    Args:
        input_data (dict):
            A dictionary containing:
                - "file_to_obfuscate" (str) - The file path of the CSV to be obfuscated 

                - "pii_fields" (list) - A list of field names to be obfuscated
        

        region (str) - Specifies the region where the S3 bucket is located. Defaults to eu-west-2.
    
    Returns:
        The obfuscated content as a string

    '''
    # Extract Pii fields and parse file path to get bucket and key
    file_path = input_data["file_to_obfuscate"]
    pii = input_data["pii_fields"]

    paths = file_path[5:].split("/", 1)

    s3_bucket = paths[0]
    s3_key = paths[1]

    # Retrieve content from specified S3 bucket
    content = read_s3(file_path, region)

    # Obfuscate specified PII fields
    obfuscated_content = obfuscation_tool(content, pii)

    # Upload obfuscated data to a new file with '-masked.csv' suffix
    new_key = s3_key.replace(".csv", "-masked.csv")
    write_s3(s3_bucket, new_key, obfuscated_content)

    return obfuscated_content


# print(obfuscated_data({
# "file_to_obfuscate": "s3://masking-test-bucket/masking-test-object",
# "pii_fields": ["name"]
# }))

# print(
#     obfuscated_data(
#         {
#             "file_to_obfuscate": "s3://final-obfuscation-bucket/final-obfuscation-key.csv",
#             "pii_fields": ["name"],
#         }
#     )
# )


print(obfuscated_data({
    "file_to_obfuscate": "s3://kedz-test-large-bucket/kedz-test-large-key.csv",
    "pii_fields": ["name"]
}))