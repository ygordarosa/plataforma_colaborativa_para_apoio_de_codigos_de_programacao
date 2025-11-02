import json
import boto3
import os

TABLE_NAME = os.environ["table"]
def lambda_handler(event, context):
    
    try:
        dynamodb = boto3.client('dynamodb')

        response = dynamodb.scan(
            TableName=TABLE_NAME
        )
        items = response["Items"]

        snippets = []
        for item in items:
            snippets.append({
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
            })
        
        snippets.sort(key=lambda s: s["like"], reverse=True)
        top_3 = snippets[:3]

        return {
            'statusCode': 200,
            'body': json.dumps(top_3, ensure_ascii=False)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        }
