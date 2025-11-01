import json
import os
import boto3
import uuid

table_1 = os.environ['AWS_DYNAMO_TABLE_NAME_1']
table_2 = os.environ['AWS_DYNAMO_TABLE_NAME_2']


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        version = body['version']
        language = body['language']
        title = body['title']
        description = body['description']
        code = body['code']
        output = body['output']
        email = body['email']

        dynamodb = boto3.client('dynamodb')

        id = str(uuid.uuid4())

        dynamodb.put_item(
            TableName=table_2,
            Item={
                "id": {"S":id},
                "email": {"S":email},
                "version": {"S":version},
                "language": {"S":language},
                "title": {"S":title},
                "description": {"S":description},
                "code": {"S":code},
                "output":{"S":output},
                "like": {"N":"2"},
                "deslike": {"N":"0"},
                "linkedin": {"S":""},
                "github": {"S":""},
                "x": {"S":""},
            }
        )

        
        return {
            'statusCode': 200,
            'body': json.dumps({
                "body": "success"
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Something went wrong')
        }
