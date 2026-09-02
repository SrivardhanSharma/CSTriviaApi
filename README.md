# CS Trivia Quiz API

A serverless full stack trivia quiz application built on AWS. Questions are pulled from a live trivia source, served through a REST API, and graded server side, with a leaderboard that tracks each player's personal best.

Built as a hands-on project to learn serverless backend development — Lambda, API Gateway, and DynamoDB — end to end, from infrastructure to a deployed, working frontend.

## Features

- Randomized 10 question rounds randomly pulled from 40 computer science trivia questions
- Server side answer validation
- Leaderboard that only updates on a new personal best per player
- Two frontend themes 
- Fully serverless backend 

## Tech Stack

**Backend:** Python, AWS Lambda, Amazon API Gateway, Amazon DynamoDB, AWS SAM
**Frontend:** HTML, CSS, vanilla JavaScript
**External data:** [Open Trivia DB](https://opentdb.com) API
**Hosting:** AWS Amplify 

## Project Structure

```
quiz-api/
├── template.yaml              # AWS SAM infrastructure definition
├── requirements.txt
├── functions/
│   ├── import_questions/      # Pulls questions from Open Trivia DB into DynamoDB
│   ├── get_quiz/               # Returns a randomized set of questions
│   ├── submit_answer/          # Grades a single answer server-side
│   ├── finish_round/           # Saves a player's score if it's a new best
│   └── leaderboard/             # Returns the top scores
├── webapp/
│   ├── index-worksheet.html    # "Graded worksheet" themed frontend
│   └── index-modern.html       # Modern SaaS themed frontend (light/dark mode)
└── docs/
    ├── APIDoc.md
    ├── architectureDeepDive.md
    ├── deploymentGuide.md
    ├── modificationGuide.md
    └── userGuide.md
```

## Quick Start

See [docs/deploymentGuide.md](docs/deploymentGuide.md) for full setup instructions. In short:

```bash
sam build
sam deploy --guided
```

Then open `webapp/index-modern.html` in a browser (after updating the `API_BASE` constant with your deployed API URL).

## Documentation

- [User Guide](docs/userGuide.md) — how to use the app
- [API Documentation](docs/APIDoc.md) — endpoint reference
- [Architecture Deep Dive](docs/architectureDeepDive.md) — how it's built
- [Deployment Guide](docs/deploymentGuide.md) — how to deploy your own copy
- [Modification Guide](docs/modificationGuide.md) — how to extend it

## Author

Srivardhan Sharma — [GitHub](https://github.com/SrivardhanSharma) · [LinkedIn](https://www.linkedin.com/in/srivardhan-sharma-933591203/)
# CSTriviaApi
