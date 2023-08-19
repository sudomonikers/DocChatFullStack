#!/bin/bash
#prompt user for which backend they want to use

#if they choose backend OP, prompt user for pinecone key and region, as well as the name of the bucket they want to create
BACKEND_DIRECTORY="./backend-OP"
LAMBDA_BUCKET_NAME="chat-with-docs-lambda-s3-artifact"
FUNCTION_NAME="chat-with-docs-rest-api"
VERSION=$(date +%Y%m%d%H%M%S)
AWS_REGION="us-east-2"
AWS_ACCOUNT_ID=145880140878



#first we need to create the resources the rest of the infrastructure depends on
cd ./infrastructure
terraform init
terraform apply -target=aws_ecr_repository.lambda_ecr_repo -auto-approve



#now push things to those created resources
cd ../${BACKEND_DIRECTORY}
open --background -a Docker
DOCKER_STATUS=$(docker info &>/dev/null; echo $?) # Check if Docker is running and ready
while [ "$DOCKER_STATUS" -ne 0 ]; do # Wait until Docker is up and running
    echo "Waiting for Docker to start..."
    sleep 2
    DOCKER_STATUS=$(docker info &>/dev/null; echo $?)
done
echo "Docker is up and running!"
ECRrepositoryUri=$(aws ecr describe-repositories --repository-names lambda-docker-repo --query 'repositories[0].repositoryUri' --output text)
docker build --platform linux/amd64 -t docker-image:$VERSION .
docker tag docker-image:$VERSION $ECRrepositoryUri:latest
docker push $ECRrepositoryUri:latest
docker rmi docker-image:$VERSION
docker rmi $ECRrepositoryUri:latest
osascript -e 'quit app "Docker"'
aws lambda update-function-code --function-name $FUNCTION_NAME --image-uri $ECRrepositoryUri:latest

#apply the terraform infrastructure
cd ../infrastructure
terraform init
terraform apply -auto-approve
cd ../
