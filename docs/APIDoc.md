# CS Trivia Quiz API — APIs

## Overview

A REST API backing a trivia quiz app. Handles importing questions from an external source, serving randomized rounds, grading answers, and tracking a leaderboard.

## Base URL

```
https://{api-id}.execute-api.{region}.amazonaws.com/Prod
```


## Authentication

None. All endpoints are public with no API key or auth token required, since this is a personal project. See [Security Considerations](architectureDeepDive.md#security-considerations) for the tradeoffs of this decision.

### Headers Required

```
Content-Type: application/json
```
(required for `POST` requests only)

## 1) Question Endpoints

#### POST /import — Pull a fresh batch of questions from Open Trivia DB into the database

**Request body:** none

**Response:**
```json
{ "imported": 40 }
```

#### GET /quiz — Fetch a randomized set of questions for a round

**Query parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `limit` | integer | 10 | Number of questions to return |

**Response:**
```json
{
  "questions": [
    {
      "question_id": "a1b2c3d4-...",
      "question": "What does CPU stand for?",
      "category": "Science: Computers",
      "difficulty": "easy",
      "options": [
        "Central Processing Unit",
        "Computer Personal Unit",
        "Central Program Utility",
        "Central Processor Undertaking"
      ]
    }
  ]
}
```


## 2) Gameplay Endpoints

#### POST /submit — Grade a single answer

**Request body:**
```json
{
  "question_id": "a1b2c3d4-...",
  "answer": "Central Processing Unit"
}
```

**Response:**
```json
{
  "correct": true,
  "correct_answer": "Central Processing Unit"
}
```

#### POST /finish — Save a completed round's score if it's a new personal best

**Request body:**
```json
{
  "player_id": "sri",
  "score": 8,
  "total": 10
}
```

**Response:**
```json
{
  "best_score": 8,
  "is_new_best": true
}
```

## 3) Leaderboard Endpoints

#### GET /leaderboard — Get the top scores across all players

**Response:**
```json
{
  "leaderboard": [
    { "player_id": "sri", "score": 8, "total": 10 }
  ]
}
```

## Response Format

### Success Response
All successful responses return HTTP 200 with a JSON body as shown above.

### Error Response
```json
{ "error": "description of what went wrong" }
```

## Error Codes

| Status | Meaning |
|---|---|
| 400 | Missing required field(s) in the request body |
| 404 | Question ID not found (`/submit` only) |
| 500 | Unhandled server error — check CloudWatch logs for the relevant Lambda function |

## Rate Limiting

None configured. API Gateway's default account-level throttling applies (10,000 requests/second burst, shared across the account).

## SDK / Client Examples

### JavaScript/TypeScript
```javascript
const res = await fetch(`${API_BASE}/quiz?limit=10`);
const data = await res.json();
```

### Python
```python
import requests
res = requests.get(f"{API_BASE}/quiz", params={"limit": 10})
data = res.json()
```

### cURL
```bash
curl -X POST https://your-api-url/Prod/submit \
  -H "Content-Type: application/json" \
  -d '{"question_id": "abc123", "answer": "Central Processing Unit"}'
```

## Changelog

- Removed cumulative per-answer scoring in favor of a `/finish` endpoint that only saves a new personal best
- Added CORS headers to all Lambda responses to support browser-based frontend calls
- Fixed a `Decimal`-to-JSON serialization bug in score-returning endpoints


