resource "aws_iam_role" "gdpr_lambda_role" {
  name = "gdpr_lambda_permissions"


  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Sid    = "AllowLambdaAssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  tags = {
    project = "GDPR Obfuscator"
  }
}

resource "aws_iam_policy" "gdpr_lambda_policy" {
  name        = "gdpr_lambda_policies"
  description = "Allows for lambda to read/write to s3 and log to CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow",
        Resource = "arn:aws:s3:::kedz-tf-test-bucket/*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"

        ]
        Effect = "Allow",
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
  tags = {
    Project = "GDPR Obfuscator"
    Function = "Lambda s3 access"
  }
}

resource "aws_iam_role_policy_attachment" "gdpr_lambda_policy_attachment" {
  role       = aws_iam_role.gdpr_lambda_role.name
  policy_arn = aws_iam_policy.gdpr_lambda_policy.arn
}