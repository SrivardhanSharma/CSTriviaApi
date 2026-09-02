# User Guide

## Prerequisites
Nothing to install — just a web browser.

## Introduction
CS Trivia Quiz is a browser-based computer science trivia game. Answer 10 randomly selected questions per round, get instant feedback on each answer, and see how your best score compares to other players on the leaderboard.

### Key Features
- Fresh, randomized question sets each round
- Instant correct/incorrect feedback with the right answer shown
- A leaderboard tracking every player's personal best score
- Light and dark mode (modern theme)

## Getting Started

### Step 1: Access the Application
Open the app's URL in any modern web browser (or open the HTML file directly if running locally).

### Step 2: Enter Your Name
Type a name into the input field on the start screen. This is how you'll appear on the leaderboard.

### Step 3: Start the Quiz
Click "Start quiz" / "Begin quiz." Ten questions will be pulled at random from the question bank.

### Step 4: Answer Each Question
Click an answer choice. You'll immediately see whether it was correct, along with the right answer if you got it wrong. Click "Next question" to continue.

### Step 5: View Results
After the 10th question, you'll see your final score. If it's higher than your previous best under that name, it's saved to the leaderboard automatically.

## Common Use Cases

### Use Case 1: Quick solo practice
Play a round by yourself to test your CS knowledge — no account or setup required.

### Use Case 2: Competing with friends
Share the app's link with friends and see who can top the leaderboard — everyone playing under a unique name gets their own tracked best score.

## Tips and Best Practices
- Use a consistent name each time you play if you want your score to accumulate toward a single leaderboard entry
- Replaying only updates the leaderboard if you beat your own previous best score

## Frequently Asked Questions (FAQ)

### Q: Do I need to create an account?
No — just type a name each time you play.

### Q: Why didn't my score show up on the leaderboard?
Only your best-ever score under a given name is saved. If your latest round was lower than a previous round, the leaderboard keeps your higher score.

### Q: Can I play the same questions again?
Questions are pulled randomly from a pool of 40 each round, so repeats are possible but the full 10-question set is unlikely to repeat exactly.

### Q: Is my data private?
Only your chosen name and score are stored — no personal information is collected.

## Troubleshooting

### Issue: The leaderboard says "Couldn't load leaderboard"
This usually means the app can't reach the backend API. Check your internet connection, or if you're the developer, confirm the backend is deployed and the `API_BASE` URL in the HTML file is correct.

### Issue: Questions won't load / "No questions in the bank yet"
The question database may not have been seeded yet. A developer needs to run the `/import` endpoint once after deployment.

### Issue: My score seems too high or too low
The leaderboard shows your best single round (out of 10), not a cumulative total across multiple rounds.

## Getting Help
This is a personal project without a formal support channel — reach out to the developer directly via the contact info in the main [README](../README.md#author).

## Next Steps
Try to beat your own best score, or challenge a friend to top the leaderboard.
