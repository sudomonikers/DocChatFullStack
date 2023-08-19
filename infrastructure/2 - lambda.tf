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

resource "aws_ecr_repository" "lambda_ecr_repo" {
  name = "lambda-docker-repo"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_lambda_function" "chat_with_docs_rest_api_function" {
  function_name = "chat-with-docs-rest-api"
  image_uri = "${aws_ecr_repository.lambda_ecr_repo.repository_url}:latest"
  package_type = "Image"
  role = aws_iam_role.chat_with_docs_rest_api.arn
  depends_on = [aws_ecr_repository.lambda_ecr_repo]
  tracing_config {
    mode = "Active"
  }
  environment {
    variables = {
      # Environment variables, if needed
    }
  }
}

resource "aws_cloudwatch_log_group" "chat_with_docs" {
  name = "/aws/lambda/${aws_lambda_function.chat_with_docs_rest_api_function.function_name}"

  retention_in_days = 14
}
