provider "aws" {
  region     = "us-east-2"
}

module "bucket-1" {
  source = "./modules/s3"
  s3-bucket-name = "chat-with-docs-bucket"
}
