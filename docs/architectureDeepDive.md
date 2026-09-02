# Architecture Deep Dive

## Architecture Diagram

```
┌─────────────┐      HTTPS      ┌──────────────┐      invokes      ┌──────────────────┐
│   Browser    │ ───────────────▶│ API Gateway  │───────────────────▶│  Lambda Functions  │
│ (index.html) │◀─────────────── │   (Prod)     │◀────────────────── │  (Python 3.12)     │
└─────────────┘      JSON        └──────────────┘                    └─────────┬─────────┘
                                                                                 │
                                                                    reads/writes │
                                                                                 ▼
                                                                       ┌──────────────────┐
                                                                       │    DynamoDB       │
                                                                       │ QuizQuestions      │
                                                                       │ QuizScores         │
                                                                       └──────────────────┘
                                                                                 ▲
                                                                                 │ one-time import
                                                                       ┌──────────────────┐
                                                                       │  Open Trivia DB    │
                                                                       │  (external API)    │
                                                                       └──────────────────┘
```

## Architecture Flow

### 1. User Interaction
A player opens the static HTML frontend (hosted on AWS Amplify or opened locally) and enters their name.

### 2. Request Processing
The frontend calls `GET /quiz`, which hits API Gateway and invokes the `GetQuizFunction` Lambda.

### 3. Question Retrieval
`GetQuizFunction` scans the `QuizQuestions` DynamoDB table, randomly samples 10 questions, strips out which answer is correct, and shuffles all answer options together before returning them — so the correct answer can't be inferred from the response shape.

### 4. Answer Grading
As the player answers each question, the frontend calls `POST /submit`. `SubmitAnswerFunction` looks up the real answer server-side and compares it — grading never happens in the browser, so it can't be bypassed by reading client-side code.

### 5. Response Generation
After all questions are answered, the frontend calls `POST /finish` with the round's total score. `FinishRoundFunction` compares it against the player's stored best in `QuizScores` and only overwrites it if the new score is higher.

## Cloud Services / Technology Stack

### Frontend
Static HTML/CSS/vanilla JavaScript, no build step. Hosted on AWS Amplify Hosting (manual deploy, no CI/CD pipeline needed for a static single-file app).

### Backend Infrastructure
- **AWS Lambda** (Python 3.12) — 5 functions, each single-purpose
- **Amazon API Gateway** — REST API, Lambda proxy integration, CORS enabled

### Data Storage
- **Amazon DynamoDB** — 2 tables, both on-demand (pay-per-request) billing:
  - `QuizQuestions` — partition key `question_id`
  - `QuizScores` — partition key `player_id`

### Additional Services
- **Open Trivia DB** (external, non-AWS) — source of trivia question data, called once by `ImportQuestionsFunction`

## Infrastructure as Code

This project uses **AWS SAM**, not CDK. SAM was chosen for its lower ceremony on a small, fixed-shape project — the entire infrastructure fits legibly in one `template.yaml` file using SAM's serverless-specific shorthand (`AWS::Serverless::Function`, `DynamoDBCrudPolicy`, etc.), without needing a general-purpose programming language to express it.

### SAM Template Structure
`template.yaml` declares, in order:
1. Global defaults shared by all functions (runtime, timeout, environment variables, CORS)
2. Two `AWS::DynamoDB::Table` resources
3. Five `AWS::Serverless::Function` resources, each with an `Events` block wiring it to an API Gateway route
4. An `Outputs` section exposing the deployed API's base URL

### Key SAM Constructs
- `DynamoDBCrudPolicy` — auto-generates least-privilege IAM permissions per function, scoped to the specific table it needs
- `Globals` — shared config (Python runtime, environment variables, CORS settings) applied across all functions without repeating it five times

### Deployment Automation
`sam build` packages each function's code; `sam deploy` turns the template into a CloudFormation stack, creating or updating every resource in one operation. Re-running `sam deploy` after any code or template change performs an incremental update — only changed resources are touched.

## Security Considerations

- **No authentication** on any endpoint — acceptable for a public demo project, but would need API keys or Cognito auth before handling real user data
- **Server-side grading** — the correct answer is never sent to the client until after a guess is submitted, preventing trivial cheating by inspecting network responses
- **IAM least privilege** — each Lambda function only has CRUD access to the specific DynamoDB table(s) it actually uses, not blanket account access

## Scalability

Every component here scales automatically and requires no capacity planning:
- Lambda scales horizontally per-request with no server provisioning
- DynamoDB on-demand mode scales read/write throughput automatically with traffic
- API Gateway handles concurrent connections without configuration

At personal-project traffic levels, this comfortably stays within AWS's free tier.

## Architectural Decisions

### Decision 1: Server-side grading over client-side
**Why:** A client-side-only quiz can be trivially cheated by reading the page's JavaScript or network responses for the correct answer. Moving grading to `submit_answer` means the correct answer is never exposed to the browser until after a guess is made.

### Decision 2: "Best score" leaderboard over cumulative score
**Why:** An earlier version added points to a player's score every time they replayed under the same name, meaning someone who played 10 rounds would always outrank a better player who played once. Switching to "only save if it beats your previous best" (via a dedicated `/finish` endpoint) makes the leaderboard reflect skill in a single round, not volume of play.

### Example: Randomized Question Sampling
`GetQuizFunction` scans the full question pool and uses `random.sample()` in the Lambda's Python code, rather than relying on DynamoDB's own scan ordering (which is not randomized and can return the same items consistently). This ensures each round feels different even if the same player replays multiple times.
