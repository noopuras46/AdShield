# AdShield

A lightweight web application that analyzes advertisements and identifies suspicious or potentially misleading content.

## About

AdShield is designed to help distinguish legitimate advertisements from suspicious or potentially deceptive ones.
Instead of blocking advertising as a whole, the project focuses on identifying warning signs that may indicate scam or misleading content.

## Features

- Analyze advertisement text for suspicious patterns
- Calculate a risk score for the advertisement
- Classify advertisements by risk level
- Identify words or phrases that contribute to the risk
- Display the factors that influenced the result
- Provide an explanation for the detected risk
- Simple web interface for quick analysis

## Tech Stack

- Python
- Flask
- HTML
- CSS
- JavaScript

## How It Works

1. Enter or submit an advertisement for analysis.
2. AdShield examines the content for suspicious patterns.
3. A risk score is generated based on the detected signals.
4. The advertisement is classified according to its risk level.
5. AdShield explains the factors that contributed to the result.

## How to Run

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Run the Flask application.
5. Open the local URL shown in the terminal.

```bash
pip install -r requirements.txt
python app.py