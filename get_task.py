import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    task_id = event['pathParameters']['taskId']

    response = table.get_item(Key={'taskId': task_id})
    item = response.get('Item')

    if not item:
        return {'statusCode': 404, 'body': json.dumps({'error': 'Task not found'})}

    return {'statusCode': 200, 'body': json.dumps(item)}
