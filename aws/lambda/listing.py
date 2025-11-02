import json
import boto3
import os


TABLE_NAME = os.environ['TABLE_NAME']

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
        if event['requestContext']["http"]["method"] == "POST":
            body = json.loads(event['body'])
            if 'search' in body:
                search = body["search"].lower()
                texts = []
                for snippet in snippets:
                    combined_text = f"{snippet['title'].lower()}. {snippet['description'].lower()}. {snippet['code'].lower()}"
                    texts.append(combined_text)
                
               

                # Combina resultados com os metadados
                results = []
                for snippet in snippets:
                    combined_text = f"{snippet['title'].lower()} {snippet['description'].lower()} {snippet['code'].lower()}".lower()
                    score = combined_text.count(search)
                    results.append({
                        "id": snippet["id"],
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "code": snippet["code"],
                        "like": snippet["like"],
                        "version": snippet["version"],
                        "language": snippet["language"],
                        "output":snippet["output"],
                        "deslike": snippet["deslike"],
                        "linkedin": snippet["linkedin"],
                        "github": snippet["github"],
                        "x": snippet["x"],
                        "score": float(score)
                    })

                # Ordena pelos mais relevantes
                results.sort(key=lambda x: x["score"], reverse=True)
                return {
                    'statusCode': 200,
                    'body': json.dumps(results, ensure_ascii=False)
                }
            elif body["filter_language"]:
                filtered_snippets = []
                for snippet in snippets:
                    if snippet["language"] == body["filter_language"]:
                        filtered_snippets.append(snippet)
                return {
                    'statusCode': 200,
                    'body': json.dumps(filtered_snippets, ensure_ascii=False)
                }


        print("chegou aqui")
        return {
            'statusCode': 200,
            'body': json.dumps(snippets, ensure_ascii=False)
        }


    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        }
