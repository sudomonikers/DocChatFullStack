provider "aws" {
  region                      = "us-east-2"
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

locals {
  region             = "us-east-2"
  bucket_name        = "chat-with-docs-ui-bucket"
  storage_bucket     = "chat-with-docs-storage-bucket"
  lambda_s3_artifact = "chat-with-docs-lambda-s3-artifact"
  stack_name         = "backend-OP" #change this to whichever directory you are using, OP or local hosted
}
