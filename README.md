GRADE EVALUATOR & ARCHIVER

This project contains two scripts for managing student grades:

1.Grade-evaluator.py – Reads a CSV file with assignment data, validates weights and scores, computes final grade and GPA, determines pass/fail status, and suggests which formative assignments are eligible for resubmission.

2.Organizer.sh – Archives the current grades.csv file by moving it to an archive/ folder with a timestamp, creates a fresh empty grades.csv, and logs the action.

I.REQUIREMENTS

1.Python 3 (for the evaluator)

2.Unix‑like shell (Linux, macOS, or Git Bash on Windows) to run the Bash script.

No external Python libraries are needed – only the standard csv, os, and sys modules.

II.PURPOSE FOR EACH SCRIPT
            
1.PYTHON SCRIPT – grade-evaluator.py

Purpose

1.Reads a CSV file with the columns:

assignment – name of the assignment

group – formative or summative

score – student’s grade (0–100)

weight – weight of the assignment (percentage of the total grade)

It then:

2.Validates that all scores are between 0 and 100.

3.Checks that the sum of all weights equals 100, formative weights sum to 60, and summative weights sum to 40.

4.Computes the final grade (out of 100) and GPA (out of 5.0).

5.Calculates the average score in the formative and summative groups.

6.Determines pass/fail: a student passes only if both group averages are ≥ 50%.

7.Suggests which formative assignment(s) to resubmit: those that scored < 50% and have the highest weight among failed formatives.

How to run

-> Open a terminal in the project folder.

-> Run the script:

python grade-evaluator.py or /.grade-evaluator.py

When prompted, enter the name of the CSV file (e.g., grades.csv).
The script will process the file and print the results.

2.BASH SCRIPT - organizer.sh

Purpose

1.Automates the archival of grades.csv after you finish evaluating a batch of grades.
It does the following:

2.Creates an archive directory if it doesn’t exist.

3.Generates a timestamp (e.g., 20250326-153042).

4.Renames the existing grades.csv to grades_timestamp.csv and moves it into archive/.

5.Creates a new empty grades.csv in the current directory, ready for the next batch.

6.Appends a log entry to organizer.log (e.g., 20250326-153042: Archived grades.csv -> archive/grades_20250326-153042.csv).

How to run

-> Make the script executable (Linux/macOS/WSL):

chmod +x organizer.sh
(On Windows with Git Bash you can skip this and just use bash organizer.sh.)

->Run it:

./organizer.sh
Or:

bash
bash organizer.sh
The script will archive the current grades.csv and leave a fresh empty one behind.

NOTES

If grades.csv does not exist, the script logs a warning and does nothing else.

The log file organizer.log accumulates entries over time.

III.WORKFLOW EXAMPLE

1.Prepare a valid CSV file named grades.csv with the required columns.

2.Run the Python evaluator to see the student’s grade report.

3.Run the Bash archiver to move the used CSV to the archive and reset the environment for the next student.

4.Repeat steps for the next student and so on.

IV.ERROR HANDLING

1.Missing CSV file – Python script exits with an error.

2.Empty CSV file (or only headers) – Python script exits with an error.

3.Invalid scores or weights – Python script exits with a descriptive message.

4.No grades.csv when archiving – Bash script logs a warning but continues.


