import boto3
import json
import os
from boto3.dynamodb.conditions import Key

# Assuming you have a function defined for updating the task
def handler(event, context):
    table_name = os.environ['TABLE_NAME']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    body = json.loads(event['body'])  # Parse the JSON body
    new_status = body['status']  # Access the 'status' field
    new_title = body['title']
    new_description = body['description']

    # Extract taskId and the new status from the event
    task_id = event['pathParameters']['taskId']

    # Define the update expression
    update_expression = "SET #s = :new_status"
    expression_attribute_names = {
        "#s": "status"  # Use #s as a placeholder for the reserved word
    }
    expression_attribute_values = {
        ":new_status": new_status
    }

    try:
        # Perform the update
        table.update_item(
            Key={'taskId': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {
            'statusCode': 200,
            'body': f'Task {task_id} updated successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
