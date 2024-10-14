# Tasks API with AWS CDK

Serverless REST API using AWS CDK
Perform CRUD operations with a DynamoDB table.

## Prerequisites

- [Docker](https://www.docker.com/)
- [AWS CLI](https://aws.amazon.com/cli/)
- [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-python.html) (optional if using Docker)
- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/)

## Project Structure

The project consists of the following main components:

- **DynamoDB Table**: `TasksTable` to store task data.
- **Lambda Functions**: Functions to handle CRUD operations.
- **API Gateway**: Exposes the Lambda functions as a REST API.

## Setting Up Environment Variables

Create a `.env` file in the root of your project directory with the following content:

```plaintext
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=us-east-2  # Change to your desired region
```


## Building and Running the Docker Container

- Build the Docker image:
docker build -t cdk-app .

- Run the Docker container with environment variables:
docker run -it --env-file .env cdk-app

- Bootstrapping the CDK Environment
cdk bootstrap aws://<YOUR_AWS_ACCOUNT_ID>/<YOUR_AWS_REGION>

- Deploying the Stack
cdk deploy

- Delete Stack
cdk delete


## Example API Calls

- Create a Task:
curl -X POST -H "Content-Type: application/json" -d '{"taskId": "1", "status": "New"}' <API_ENDPOINT>/tasks
- Get a Task:
curl -X GET <API_ENDPOINT>/tasks/1
- Update a Task:
curl -X PUT -H "Content-Type: application/json" -d '{"status": "In Progress"}' <API_ENDPOINT>/tasks/1
- Delete a Task:
curl -X DELETE <API_ENDPOINT>/tasks/1