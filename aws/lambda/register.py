import json
import os
import boto3

table = os.environ["AWS_DYNAMO_TABLE_NAME"]

def lambda_handler(event, context):
    event = json.loads(event.get("body", "{}"))
    email = event.get("email")
    password = event.get("password")
    name = event.get("name")

    dynamodb = boto3.client("dynamodb")

    #verifica se o registro nao existe
    response = dynamodb.get_item(
        TableName=table,
        Key={
            "email": {"S":email}
        }
    )

    if "Item" in response:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Email ja cadastrado"
            })
        }
    
    dynamodb.put_item(
        TableName=table,
        Item={
            "email": {"S":email},
            "name": {"S":name},
            "password": {"S":password}
        }
    )
    
    return  {
        "statusCode": 200,
        "body":json.dumps({
            "email": email,
            "name": name
        })
    }

