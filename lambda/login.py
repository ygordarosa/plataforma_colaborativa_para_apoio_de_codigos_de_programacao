import json
import os
import boto3

table = os.environ["AWS_DYNAMO_TABLE_NAME"]

def lambda_handler(event, context):
    
    body = json.loads(event.get("body", "{}"))
    
    email = body.get("email")
    password = body.get("password")

    
    dynamodb = boto3.client("dynamodb")

    #verifica se o registro existe
    response = dynamodb.get_item(
        TableName=table,
        Key={
            "email": {"S":email}
        }
    )
    if "Item" in response:
        user_found = response["Item"]["password"]["S"] == password
    else:
        user_found = False
    
    if not user_found:
        return {
            "statusCode": 401,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Credenciais inválidas"})
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "email": email,
            "name": response["Item"]["name"]["S"]})
    }



