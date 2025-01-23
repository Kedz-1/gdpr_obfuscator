resource "aws_lambda_permission" "allow_excecution_from_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.gdpr_lambda_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.gdpr_bucket.arn

}