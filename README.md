
# Lost and Found Matcher

## Project Overview

Lost and Found Matcher is a Python-based application that helps campus administrators identify possible matches between lost-item and found-item reports.

The system extracts item details, validates information, calculates match scores and generates reports.

## Features

- Reads lost and found reports from CSV files.
- Extracts item details from descriptions.
- Validates extracted information.
- Compares lost and found reports.
- Calculates matching scores.
- Explains why two reports match.
- Identifies possible double claims.
- Generates CSV and text output reports.
- Supports human review before returning items.

## Technologies Used

- Python
- CSV
- Regular Expressions
- Pandas (if used in the final implementation)
- LLM API (planned integration)

## Project Structure

Lost_and_Found_Matcher/
│
├── data/
│   ├── lost.csv
│   └── found.csv
│
├── outputs/
│   ├── matches.csv
│   ├── no_match.csv
│   ├── unclaimed.csv
│   └── summary.txt
│
├── main.py
├── matcher.py
├── validator.py
├── llm_extractor.py
├── test_matcher.py
├── test_red_team.py
├── system_prompt.txt
├── judgment_framework.md
├── cost_latency.md
└── README.md

## How to Run

### 1. Create a virtual environment

uv venv .venv

### 2. Activate the environment (Windows PowerShell)

.\.venv\Scripts\Activate.ps1

### 3. Install dependencies

uv pip install pandas python-dotenv requests

### 4. Run the application

python main.py

## Testing

Run the matching tests:

python test_matcher.py

Run the red-team tests:

python test_red_team.py

## Output Files

- matches.csv: Suggested matching pairs.
- no_match.csv: Lost reports without suggestions.
- unclaimed.csv: Found reports without suggestions.
- summary.txt: Overall processing summary.

## Human Verification

The application only suggests possible matches.

A campus administrator must verify ownership before returning any item.

## Current Development Status

The current prototype uses a temporary rule-based extraction method.

Real LLM API integration, API cost measurement and final evaluation are still pending.
