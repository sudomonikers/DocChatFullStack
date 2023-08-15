
resource "aws_s3_bucket" "lambda_bucket" {
  bucket        = local.lambda_s3_artifact
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_role" "chat_with_docs_rest_api" {
  name = "chat-with-docs-rest-api-policy"

  assume_role_policy = <<POLICY
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    POLICY
}

resource "aws_iam_role_policy_attachment" "chat_with_docs_rest_api_policy" {
  role       = aws_iam_role.chat_with_docs_rest_api.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "chat_with_docs_rest_api_function" {
  function_name = "chat-with-docs-rest-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_chat_with_docs.key

  runtime = "python3.11"
  handler = "api.main.handler"

  source_code_hash = data.archive_file.lambda_chat_with_docs.output_base64sha256

  role = aws_iam_role.chat_with_docs_rest_api.arn
}

resource "aws_cloudwatch_log_group" "chat_with_docs" {
  name = "/aws/lambda/${aws_lambda_function.chat_with_docs_rest_api_function.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_chat_with_docs" {
  type = "zip"

  source_dir  = "../${path.module}/${local.stack_name}"
  output_path = "../${path.module}/lambda.zip"
}

resource "aws_s3_object" "lambda_chat_with_docs" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "lambda.zip"
  source = data.archive_file.lambda_chat_with_docs.output_path

  etag = filemd5(data.archive_file.lambda_chat_with_docs.output_path)
}
