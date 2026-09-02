import os
import json
import decimal
import boto3

dynamodb = boto3.resource("dynamodb")
questions_table = dynamodb.Table(os.environ["QUESTIONS_TABLE"])


def _decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        question_id = body.get("question_id")
        answer = body.get("answer")

        if not all([question_id, answer]):
            return _response(400, {"error": "question_id and answer are required"})

        question = questions_table.get_item(Key={"question_id": question_id}).get("Item")
        if not question:
            return _response(404, {"error": "Question not found"})

        is_correct = answer.strip().lower() == question["correct_answer"].strip().lower()

        return _response(200, {
            "correct": is_correct,
            "correct_answer": question["correct_answer"],
        })

    except Exception as e:
        return _response(500, {"error": str(e)})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body, default=_decimal_default),
    }
