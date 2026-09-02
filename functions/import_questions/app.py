import os
import json
import uuid
import html
import boto3
import urllib.request

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["QUESTIONS_TABLE"])


OPEN_TRIVIA_URL = "https://opentdb.com/api.php?amount=40&category=18&type=multiple"


def lambda_handler(event, context):
    try:
        with urllib.request.urlopen(OPEN_TRIVIA_URL) as response:
            data = json.loads(response.read().decode())

        results = data.get("results", [])
        if not results:
            return _response(502, {"error": "No questions returned from Open Trivia DB"})

        imported = 0
        with table.batch_writer() as batch:
            for item in results:
                question_id = str(uuid.uuid4())
                correct_answer = html.unescape(item["correct_answer"])
                incorrect_answers = [html.unescape(a) for a in item["incorrect_answers"]]

                batch.put_item(Item={
                    "question_id": question_id,
                    "question": html.unescape(item["question"]),
                    "correct_answer": correct_answer,
                    "incorrect_answers": incorrect_answers,
                    "difficulty": item.get("difficulty", "unknown"),
                    "category": html.unescape(item.get("category", "General")),
                })
                imported += 1

        return _response(200, {"imported": imported})

    except Exception as e:
        return _response(500, {"error": str(e)})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body),
    }
