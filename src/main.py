from src.obfuscator import obfuscate_tool
from src.s3_utils import read_s3
from src.s3_utils import write_s3


def obfuscated_data(input_data, region='eu-west-2'):

    file_path = input_data["file_to_obfuscate"]
    pii = input_data["pii_fields"]

    paths = file_path[5:].split('/', 1)

    s3_bucket = paths[0]
    s3_key = paths[1]

    content = read_s3(file_path, region)
    obfuscated_content = obfuscate_tool(content, pii)
    write_s3(s3_bucket, s3_key, obfuscated_content)

    return obfuscated_content

print(obfuscated_data({
"file_to_obfuscate": "s3://masking-test-bucket/masking-test-object",
"pii_fields": ["email"]
}))

