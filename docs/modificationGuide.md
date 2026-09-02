# Project Modification Guide

## Introduction
This guide covers how to extend or customize the CS Trivia Quiz API — adding new endpoints, changing the question source, modifying the frontend theme, and more.

## Table of Contents
- [Project Structure Overview](#project-structure-overview)
- [Frontend Modifications](#frontend-modifications)
- [Backend Modifications](#backend-modifications)
- [Adding New Features](#adding-new-features)
- [Database Modifications](#database-modifications)
- [Best Practices](#best-practices)
- [Testing Your Changes](#testing-your-changes)

## Project Structure Overview
See the [README](../README.md#project-structure) for the full folder layout. In short: `template.yaml` defines infrastructure, `functions/` holds one folder per Lambda, `webapp/` holds the static frontend files.

## Frontend Modifications

### Changing the UI Theme
Both `webapp/index-worksheet.html` and `webapp/index-modern.html` define their entire look using CSS custom properties (variables) at the top of the `<style>` block — e.g. `--accent`, `--bg`, `--card`. Change these values to retheme the app without touching layout markup.

The modern theme also supports light/dark mode via a `[data-theme="dark"]` CSS selector overriding the same variable names — add a new theme by duplicating that block with different values.

### Adding New Pages
This is a single-page app with three view states (`setupCard`/`setupView`, `quizCard`/`quizView`, `doneCard`/`doneView`) toggled via `style.display`. To add a new "page," add a new `<div>` with a unique ID and toggle its visibility the same way.

### Modifying Components
Answer choices are rendered dynamically in JavaScript (`renderQuestion()` function) from the `options` array returned by `GET /quiz` — modify the `choicesEl.innerHTML` template string there to change how each choice renders.

## Backend Modifications

### Adding New Lambda Functions
1. Create a new folder under `functions/` with an `app.py` containing a `lambda_handler(event, context)` function
2. Add a corresponding `AWS::Serverless::Function` resource to `template.yaml`, following the pattern of existing functions
3. Run `sam build && sam deploy`

### Modifying the SAM Template
`template.yaml` is the single source of truth for all infrastructure. Common changes:
- Adjust `Globals.Function.Timeout` to change the timeout for all functions at once
- Add a new `Policies` entry under a function to grant it access to additional AWS resources

### Adding New API Endpoints
Add an `Events` block to a function's definition in `template.yaml`:
```yaml
Events:
  Api:
    Type: Api
    Properties:
      Path: /your-new-path
      Method: get
```

## Adding New Features

### Feature: Timed Questions
To add a per-question timer: track elapsed time client-side in `webapp/index-modern.html`, and optionally pass it to `POST /submit` so `submit_answer/app.py` can factor speed into scoring.

### Feature: Multiple Categories
Open Trivia DB supports many categories beyond "Science: Computers" (category ID 18). To support category selection: modify `import_questions/app.py` to accept a category parameter, store `category` as part of each question item (already done), and add a category filter to `get_quiz/app.py`'s scan/sample logic.

## Database Modifications

### Adding New Tables
Add a new `AWS::DynamoDB::Table` resource to `template.yaml`, then reference its name via a new environment variable in `Globals.Function.Environment.Variables`, following the existing pattern for `QUESTIONS_TABLE` and `SCORES_TABLE`.

### Modifying Schema
DynamoDB is schemaless beyond its declared key attributes — you can add new fields to items (e.g., a `difficulty_multiplier` on scores) without a migration. Just update the relevant Lambda function(s) to read/write the new field.

## Best Practices

- Keep each Lambda function single-purpose — it makes IAM permissions easier to scope narrowly and keeps cold-start times low
- Always add the `Access-Control-Allow-Origin` header to new Lambda responses if they'll be called from a browser
- Use `json.dumps(body, default=_decimal_default)` for any response containing a number read from DynamoDB

## Testing Your Changes

### Local Testing
Test individual endpoints directly with `curl` against your deployed API before wiring up frontend changes:
```bash
curl -X POST {api-url}/your-endpoint -H "Content-Type: application/json" -d '{"key": "value"}'
```

### Deployment Testing
After any `template.yaml` or function code change:
```bash
sam build
sam deploy
```
Then re-run the `curl` checks in [deploymentGuide.md](deploymentGuide.md#post-deployment-verification).

## Conclusion
The project is intentionally small and single-purpose, which makes most modifications additive — you can usually add a new Lambda function and API route without touching existing ones.
