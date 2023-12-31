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

#kubernetes
aws eks --region $(terraform output -raw region) update-kubeconfig --name $(terraform output -raw cluster_name)
helm repo add qdrant https://qdrant.to/helm
helm install qdrant-release qdrant/qdrant
helm install qdrant-database qdrant/qdrant --set "service.type=LoadBalancer"
#curl request to create a collection in qdrant db
curl --location --request POST 'http://ae6b7a69dec704390bcccc683d8d927a-555827074.us-east-2.elb.amazonaws.com:6333/collections/documents?content-type=application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
  "vectors": {
    "size": 384,
    "distance": "Cosine"
  }
}'
curl --location --request POST 'http://ae6b7a69dec704390bcccc683d8d927a-555827074.us-east-2.elb.amazonaws.com:6333/collections/titles?content-type=application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
  "vectors": {
    "size": 384,
    "distance": "Cosine"
  }
}'


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


#apply the terraform infrastructure
cd ../infrastructure
terraform init
terraform apply -auto-approve
cd ../

aws lambda update-function-code --function-name $FUNCTION_NAME --image-uri $ECRrepositoryUri:latest --output text
