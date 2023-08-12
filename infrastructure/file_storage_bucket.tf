module "storage_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.14.1"
  bucket  = local.storage_bucket
}
