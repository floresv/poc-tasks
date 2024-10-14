import os
from dotenv import load_dotenv
from aws_cdk import (
    App,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct

# Load environment variables from .env file
load_dotenv()

class TasksStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create DynamoDB Table
        table = dynamodb.Table(
            self, 'TasksTable',
            partition_key=dynamodb.Attribute(name='taskId', type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Lambda function factory to avoid repetition
        def create_lambda_handler(file: str) -> _lambda.Function:
            return _lambda.Function(
                self, f"{file}Handler",
                runtime=_lambda.Runtime.PYTHON_3_9,
                handler=f"{file}.handler",
                code=_lambda.Code.from_asset('lambda'),
                environment={
                    'TABLE_NAME': table.table_name
                }
            )

        # Create Lambda Functions for CRUD operations
        create_task = create_lambda_handler('create_task')
        get_task = create_lambda_handler('get_task')
        update_task = create_lambda_handler('update_task')
        delete_task = create_lambda_handler('delete_task')

        # Grant permissions to Lambda functions
        table.grant_read_write_data(create_task)
        table.grant_read_data(get_task)
        table.grant_read_write_data(update_task)
        table.grant_write_data(delete_task)

        # Create API Gateway
        api = apigateway.RestApi(self, 'TasksApi', rest_api_name='Tasks Service')

        # Define API resources and methods
        tasks = api.root.add_resource('tasks')
        tasks.add_method('POST', apigateway.LambdaIntegration(create_task))

        task = tasks.add_resource('{taskId}')
        task.add_method('GET', apigateway.LambdaIntegration(get_task))
        task.add_method('PUT', apigateway.LambdaIntegration(update_task))
        task.add_method('DELETE', apigateway.LambdaIntegration(delete_task))

app = App()
TasksStack(app, "TasksStack")
app.synth()
