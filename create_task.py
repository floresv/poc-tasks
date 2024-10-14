import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    body = json.loads(event['body'])
    item = {
        'taskId': body['taskId'],
        'title': body['title'],
        'description': body['description'],
        'status': body['status']
    }

    table.put_item(Item=item)

    return {
        'statusCode': 201,
        'body': json.dumps(item)
    }
