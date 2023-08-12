provider "aws" {
  region                      = "us-east-2"
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

locals {
  region         = "us-east-2"
  bucket_name    = "chat-with-docs-ui-bucket"
  storage_bucket = "chat-with-docs-storage-bucket"
}
