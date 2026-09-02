import os
import json
import random
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["QUESTIONS_TABLE"])


def lambda_handler(event, context):
    try:
        params = (event.get("queryStringParameters") or {})
        limit = int(params.get("limit", 10))

        # Scan the full pool, then randomly sample so each round is different
        result = table.scan()
        items = result.get("Items", [])
        sample_size = min(limit, len(items))
        items = random.sample(items, sample_size) if items else []

        # Build a shuffled "options" list (correct + incorrect answers combined)
        # so the client can render real multiple choice, without revealing
        # which option is correct. The actual check happens in /submit.
        for item in items:
            correct = item.pop("correct_answer", None)
            incorrect = item.pop("incorrect_answers", [])
            options = incorrect + ([correct] if correct else [])
            random.shuffle(options)
            item["options"] = options

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"questions": items}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)}),
        }
