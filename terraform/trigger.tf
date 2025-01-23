resource "aws_s3_bucket_notification" "gdpr_bucket_notification" {
  bucket = aws_s3_bucket.gdpr_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.gdpr_lambda_function.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

