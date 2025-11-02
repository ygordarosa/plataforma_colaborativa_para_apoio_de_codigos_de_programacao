import json
import boto3
import os
import uuid


TABLE_NAME_1 = os.environ['TABLE_NAME_1']
TABLE_NAME_2 = os.environ['TABLE_NAME_2']

def lambda_handler(event, context):
    try:
        dynamodb = boto3.client('dynamodb')

        if event['requestContext']["http"]["method"] == "GET":
            snippet_id = event.get("queryStringParameters", {}).get("id")
            if snippet_id:
                response = dynamodb.get_item(
                    TableName=TABLE_NAME_1,
                    Key={
                        'id': {'S': snippet_id}
                    }
                )
                item = response.get('Item')
                if item:
                    snippet = {
                        "id": item["id"]["S"],
                        "email": item["email"]["S"],
                        "version": item["version"]["S"],
                        "language": item["language"]["S"],
                        "title": item["title"]["S"],
                        "description": item["description"]["S"],
                        "code": item["code"]["S"],
                        "output":item["output"]["S"],
                        "like": int(item["like"]["N"]),
                        "deslike": int(item["deslike"]["N"]),
                        "linkedin": item["linkedin"]["S"],
                        "github": item["github"]["S"],
                        "x": item["x"]["S"],
                    }

                    comments_resp = dynamodb.scan(
                        TableName=TABLE_NAME_2,
                        FilterExpression="snippet_id = :sid",
                        ExpressionAttributeValues={":sid": {"S": snippet_id}}
                    )

                    comments = []
                    for c in comments_resp.get("Items", []):
                        comments.append({
                            "snippet_id": c["snippet_id"]["S"],
                            "user_email": c["user_email"]["S"],
                            "user_name": c["user_name"]["S"],
                            "comment": c["comment"]["S"]
                        })
                    return {
                        'statusCode': 200,
                        'body': json.dumps({
                            "snippet": snippet,
                            "comments": comments
                        }, ensure_ascii=False)
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps('Snippet not found')
                    }
        elif event['requestContext']["http"]["method"] == "POST":
            body = json.loads(event['body'])
            snippet_id = body.get("snippet_id")
            user_email = body.get("user_email")
            user_name = body.get("user_name")
            comment = body.get("comment")

            id = str(uuid.uuid4())
            dynamodb.put_item(
                TableName=TABLE_NAME_2,
                Item={
                    "id": {"S": id},
                    "snippet_id": {"S": snippet_id},
                    "user_email": {"S": user_email},
                    "user_name": {"S": user_name},
                    "comment": {"S": comment}
                }
            )
            return {
            'statusCode': 200,
            'body': json.dumps({
                "body": "success"
            })
            }
            

        print("chegou aqui")
        return {
            'statusCode': 401,
            'body': json.dumps("algo deu errado")
        }


    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        }
