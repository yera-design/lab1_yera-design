## GRADE EVALUATOR & ARCHIVER

This project contains two scripts for managing student grades:

- grade-evaluator.py – Reads a CSV file with assignment data, validates weights and scores, computes final grade and GPA, determines pass/fail status, and suggests which formative assignments are eligible for resubmission.

- organizer.sh – Archives the current grades.csv file by moving it to an archive/ folder with a timestamp, creates a fresh empty grades.csv, and logs the action.

## I. REQUIREMENTS

- Python 3 (for the evaluator)
- Unix‑like shell (Linux, macOS, or Git Bash on Windows) to run the Bash script
- No external Python libraries are needed – only the standard csv, os, and sys modules

## II. PURPOSE FOR EACH SCRIPT

1. PYTHON SCRIPT – grade-evaluator.py

Purpose:
- Reads a CSV file with the columns:
- assignment – name of the assignment
- group – formative or summative
- score – student’s grade (0–100)
- weight – weight of the assignment (percentage of the total grade)

Features:
- Validates that all required columns exist
- Normalizes input (trims spaces, lowercases group names)
- Checks for empty fields and invalid numbers
- Validates that all scores are between 0 and 100
- Validates that weights sum correctly (total = 100, formative = 60, summative = 40)
- Provides clear error messages with line numbers for easier debugging
- Computes final grade (out of 100) and GPA (out of 5.0)
- Calculates average scores in formative and summative groups
- Determines pass/fail: a student passes only if both group averages are ≥ 50%
- Suggests which formative assignment(s) to resubmit: those that scored < 50% and have the highest weight among failed formatives
How to run:
python grade-evaluator.py
 or
./grade-evaluator.py


When prompted, enter the name of the CSV file (e.g., grades.csv). The script will process the file and print the results.

2. BASH SCRIPT – organizer.sh

Purpose:
- Automates the archival of grades.csv after evaluating a batch of grades.
Features:
- Creates an archive directory if it doesn’t exist
- Generates a timestamp (e.g., 20250326-153042)
- Renames the existing grades.csv to grades_timestamp.csv and moves it into archive/
- Creates a new empty grades.csv in the current directory
- Appends a log entry to organizer.log with [INFO], [WARN], or [ERROR] tags
- Handles errors gracefully (e.g., failed mv, touch, or mkdir)
- Logs warnings if grades.csv does not exist

How to run:
chmod +x organizer.sh   # make executable (Linux/macOS/WSL)
./organizer.sh
or
bash organizer.sh

## III. WORKFLOW EXAMPLE
- Prepare a valid CSV file named grades.csv with the required columns.
- Run the Python evaluator to see the student’s grade report.
- Run the Bash archiver to move the used CSV to the archive and reset the environment for the next student.
- Repeat steps for the next student and so on.

## IV. ERROR HANDLING

Python Script (grade-evaluator.py)

- Missing CSV file → exits with error
- Empty CSV file (or only headers) → exits with error
- Missing columns → exits with descriptive error
- Empty fields → exits with descriptive error (line number shown)
- Invalid numbers → exits with descriptive error (line number shown)
- Scores out of range (0–100) → exits with descriptive error (line number shown)
- Incorrect weights → exits with descriptive error (expected totals shown)

Bash Script (organizer.sh)
-  Archive directory creation failure → logs [ERROR] and exits
-  File move failure → logs [ERROR] and exits
-  New file creation failure → logs [ERROR] and exits
- ⚠️Missing grades.csv → logs [WARN] but continues








