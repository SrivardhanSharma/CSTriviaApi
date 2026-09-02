# Deployment Guide

## Table of Contents
- [Requirements](#requirements)
- [Pre-Deployment](#pre-deployment)
- [Deployment](#deployment)
- [Post-Deployment Verification](#post-deployment-verification)
- [Troubleshooting](#troubleshooting)
- [Cleanup](#cleanup)

## Requirements

### Accounts
- An AWS account (the free tier covers this entire project)

### CLI Tools
- AWS CLI
- AWS SAM CLI

### Access Permissions
- An IAM user or role with permissions to create Lambda functions, API Gateway APIs, DynamoDB tables, and IAM roles (an `AdministratorAccess` policy is the simplest path for a personal project; a scoped-down policy is more appropriate for production use)

### Software Dependencies
- Python 3.12 (matches the Lambda runtime used in `template.yaml`)

## Pre-Deployment

### AWS Account Setup
1. Create an AWS account if you don't already have one
2. (Recommended) Set a billing budget alert: Billing Console → Budgets → Create budget → set a low threshold (e.g. $1) with an email alert

### CLI Tools Installation
This project was deployed using **AWS CloudShell** (browser-based terminal, pre-authenticated, no local credential setup needed) — see the AWS Console's top navigation bar for the CloudShell icon.

If deploying from a local machine instead:
1. Install the AWS CLI, then run `aws configure` with an IAM user's access key
2. Install the AWS SAM CLI

### Environment Configuration
No environment variables need to be set manually — `template.yaml` defines the `QUESTIONS_TABLE` and `SCORES_TABLE` environment variables for each Lambda function automatically at deploy time.

## Deployment

### Backend Deployment
From the project root:

```bash
sam build
sam deploy --guided
```

During the guided deploy, you'll be prompted for:
- **Stack Name** — e.g. `quiz-api`
- **AWS Region** — e.g. `us-east-1`
- **Confirm changes before deploy** — `y`
- **Allow SAM CLI IAM role creation** — `y`
- **Function has no authentication, is this okay?** (asked once per function) — `y` (this is a public demo API with no auth)
- **Save arguments to configuration file** — `y` (lets future deploys just use `sam deploy`)

After deployment finishes, note the `ApiUrl` value printed in the **Outputs** section — this is your API's base URL.

Once deployed, seed the question database:
```bash
curl -X POST {your-api-url}/import
```

### Frontend Deployment
1. Open `webapp/index-modern.html` and update the `API_BASE` constant near the top of the `<script>` block with your deployed `ApiUrl`
2. To host it publicly on **AWS Amplify**:
   - Rename the file to `index.html`
   - Zip it
   - AWS Console → Amplify → New app → deploy without a Git provider → upload the zip
   - Amplify provides a public URL once deployed

## Post-Deployment Verification

### Verify Backend Deployment
```bash
curl {your-api-url}/quiz?limit=5
```
Should return a JSON object with a `questions` array.

### Verify Frontend Deployment
Open the deployed Amplify URL (or the local HTML file) in a browser, play through a full round, and confirm the leaderboard updates.

## Troubleshooting

### Common Issues

#### Issue: Browser shows CORS errors in the console (`Access-Control-Allow-Origin`)
The `Globals.Api.Cors` block in `template.yaml` handles preflight requests, but each Lambda function must also include the `Access-Control-Allow-Origin` header in its actual response — this project's functions already do, but if you add a new endpoint, make sure to include it there too.

#### Issue: `Object of type Decimal is not JSON serializable`
DynamoDB returns numeric values as Python `Decimal` objects, which `json.dumps()` can't serialize by default. Any Lambda function returning a number read from DynamoDB needs a custom `default=` handler passed to `json.dumps()` (see `finish_round/app.py` for the pattern used here).

#### Issue: CDK Bootstrap Error
Not applicable — this project uses SAM, not CDK, so no bootstrap step is required.

#### Issue: Permission Denied
Usually means the IAM user/role running `sam deploy` lacks permission to create one of the resources in the template. Confirm the IAM user has sufficient permissions (see [Access Permissions](#access-permissions)).

## Cleanup

To tear down every resource this project created (Lambda functions, API Gateway, DynamoDB tables) and stop any possibility of ongoing cost:

```bash
sam delete
```

To remove the Amplify-hosted frontend: AWS Console → Amplify → select the app → Actions → Delete app.

## Next Steps

See [modificationGuide.md](modificationGuide.md) for how to add new features, and [userGuide.md](userGuide.md) for how to actually play the quiz once it's deployed.
