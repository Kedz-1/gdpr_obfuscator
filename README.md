# GDPR Obfuscator

## Overview
The GDPR Obfuscator is a Python library module developed to anonymize Personally Identifiable Information (PII) in CSV files. Designed for AWS environments, the tool ensures GDPR compliance by obfuscating sensitive data fields. It processes files directly from and to S3 buckets using `boto3`.

## Features
- **CSV Support**: Obfuscates specified fields in CSV files, ensuring data privacy.
- **AWS S3 Integration**: Reads and writes files directly from and to S3 buckets.
- **Customizable Fields**: Allows users to define specified PII fields for obfuscation.
- **Performance Optimized**: Processes CSV files up to 1MB in size within one minute.
- **Secure**: Uses IAM roles for authentication and avoids embedding credentials.
- **Extensible**: Future plans include support for JSON and Parquet file formats.

## How It Works
1. **Input**: A JSON string specifying the S3 file location and PII fields to obfuscate.
2. **Processing**: The tool reads the file, obfuscates sensitive fields, and generates an obfuscated byte-stream.
3. **Output**: The obfuscated file is uploaded directly back to the S3 bucket as a new key ending in '-masked.csv'.

### Input Example
```json
{
  "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
  "pii_fields": ["name", "email_address"]
}
```

### Output Example
Original CSV:
```csv
name,email
john Doe, john.do@example.com
```

Obfuscated CSV:
```csv
name,email
***,***
```
## Usage

### Prerequisites
- Python 3.11.1 or higher
- AWS credentials configured for `boto3`
- Access to an AWS S3 bucket

### Installation
Clone the repository and set up the environment:
```bash
git clone <https://github.com/Kedz-1/data_project.git>
cd data_project
make create-environment # Creates a virtual environment
source venv/bin/activate # Activates the virtual environment
make requirements # Installs project dependencies
```

### Programmatic Usage
```python
from data_project.main import obfuscated_data

input_data = {
    "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
    "pii_fields": ["name", "email_address"]
}

# Reads the content from the file path, obfuscates the specified PII fields and uploads back to the S3 bucket
obfuscated_data(input_data)
```

### Testing
Run unit tests and check coverage:
```bash
make scan-unit-test
```

## Known Limitations
- Currently only supports CSV files.
- Requires external handling to save the obfuscated output.
- Does not validate CSV formatting, assumes valid input
