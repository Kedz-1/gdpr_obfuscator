resource "aws_lambda_function" "gdpr_lambda_function" {

  filename      = "../lambda_function.zip"
  function_name = "gdpr_obfuscation_lambda_function"
  role          = aws_iam_role.gdpr_lambda_role.arn
  
  handler       = "handler.lambda_handler"
  runtime = "python3.11"
  timeout = 60
}