resource "aws_s3_bucket" "gdpr_bucket" {
  bucket = "kedz-tf-test-bucket"

}

resource "aws_s3_object" "gdpr_key" {
  bucket = aws_s3_bucket.gdpr_bucket.id
  key    = "kedz-tf-test-key"
  source = "../data/csv_data_file.csv"

}