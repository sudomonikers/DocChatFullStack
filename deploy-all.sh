

#deploy ui
aws s3 sync ./ui/build s3://{BUCKET_NAME} --delete
aws cloudfront create-invalidation --distribution-id {DISTRIBUTION_ID}--paths \"/*\"
