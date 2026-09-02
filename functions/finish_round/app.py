import os
import json
import decimal
import boto3

dynamodb = boto3.resource("dynamodb")
scores_table = dynamodb.Table(os.environ["SCORES_TABLE"])


def _decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        player_id = body.get("player_id")
        score = body.get("score")
        total = body.get("total")

        if player_id is None or score is None or total is None:
            return _response(400, {"error": "player_id, score, and total are required"})

        existing = scores_table.get_item(Key={"player_id": player_id}).get("Item")
        previous_best = existing["score"] if existing else 0

        is_new_best = score > previous_best
        if is_new_best:
            scores_table.put_item(Item={
                "player_id": player_id,
                "score": score,
                "total": total,
            })

        return _response(200, {
            "best_score": max(score, previous_best),
            "is_new_best": is_new_best,
        })

    except Exception as e:
        return _response(500, {"error": str(e)})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body, default=_decimal_default),
    }
