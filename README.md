# Lost and Found Matcher

## 1. Project Overview

Lost and Found Matcher is a Python-based application that helps campus administrators identify possible matches between lost-item and found-item reports.

The application uses a local AI model to extract item details, validates the extracted information, compares reports, calculates match scores and generates output files.

It assists administrators in finding possible matches, but human verification is required before returning any item.

## 2. Features

- Reads lost and found reports from CSV files.
- Uses AI to extract item details from descriptions.
- Validates extracted information against original reports.
- Compares every lost report with found reports.
- Calculates matching scores.
- Explains why reports match.
- Rejects conflicting item details.
- Identifies possible duplicate claims.
- Generates CSV and text output reports.
- Includes matching and red-team tests.
- Supports human verification before returning items.

## 3. Technologies Used

- Python
- Qwen 2.5 (0.5B)
- Ollama
- CSV
- Regular Expressions
- Requests
- Pandas (where used in the implementation)

## 4. Project Structure

```text
lost and found matcher/
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
├── test_redteam.py
├── system_prompt.txt
├── judgment_framework.md
├── cost_latency_note.md
├── ai_decision_journal.md
├── reflection.md
├── README.md
└── .gitignore
```

## 5. Requirements

- Python
- Ollama
- Qwen 2.5 (0.5B) model

## 6. Installation and Setup

### Step 1: Create a virtual environment

```powershell
uv venv .venv
```

### Step 2: Activate the environment

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
uv pip install pandas python-dotenv requests
```

### Step 4: Set up Ollama

Install Ollama and download the model:

```powershell
ollama pull qwen2.5:0.5b
```

Make sure Ollama is running before starting the application.

## 7. How to Run

Run the main application:

```powershell
python main.py
```

The application processes the lost and found reports and generates the output files in the outputs folder.

## 8. Testing

Run the matching tests:

```powershell
python test_matcher.py
```

Run the red-team tests:

```powershell
python test_redteam.py
```

The red-team tests check vague claims, brand guessing and malicious instructions.

## 9. Output Files

| File | Description |
|---|---|
| matches.csv | Suggested matching pairs with scores and reasons |
| no_match.csv | Lost reports without suggested matches |
| unclaimed.csv | Found reports without suggested matches |
| summary.txt | Overall processing summary |

## 10. Matching Rules

- Same item category is required.
- Reports more than 30 days apart are rejected.
- Different known colours are rejected.
- Different known brands are rejected.
- Same colour gives 2 points.
- Same brand gives 2 points.
- Same place gives 1 point.
- A score of 3 or more is classified as Likely.
- A score of 1 or 2 is classified as Possible.
- Items categorized as other are not automatically matched.

## 11. Human Verification

The application only suggests possible matches.

A campus administrator must verify the claimant and check ownership before returning an item. The AI system never makes the final ownership decision.

## 12. Current Development Status

The working prototype uses Qwen 2.5 (0.5B) through Ollama for local AI extraction.

The application successfully processed 10 lost reports and 10 found reports in the demonstration dataset and generated 9 suggested matches.

Matching tests and three red-team scenarios have also been prepared and tested.

## 13. Conclusion

This project demonstrates how AI and Python can help campus administrators manage lost and found reports more efficiently while keeping human verification as an essential part of the process.
