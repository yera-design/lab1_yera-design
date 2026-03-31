#!/usr/bin/python3
import csv
import sys
import os

REQUIRED_COLUMNS = {'assignment', 'group', 'score', 'weight'}

def load_csv_data():
    filename = input("Enter the name of the CSV file to process: ").strip()

    if not os.path.exists(filename):
        print(f" Ooops the file '{filename}' was not found,First make sure that {filename} exists!")
        sys.exit(1)

    assignments = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Validate required columns
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing:
                print(f"Ooops Missing required columns: {', '.join(missing)}")
                sys.exit(1)

            for line_num, row in enumerate(reader, start=2):  # start=2 (header is line 1)
                try:
                    assignment = row['assignment'].strip()
                    group = row['group'].strip().lower()
                    score_str = row['score'].strip()
                    weight_str = row['weight'].strip()

                    # Empty field check
                    if not assignment or not group or not score_str or not weight_str:
                        print(f" Ooops Empty field detected at line {line_num}.")
                        sys.exit(1)

                    # Convert to float safely
                    score = float(score_str)
                    weight = float(weight_str)

                    assignments.append({
                        'assignment': assignment,
                        'group': group,
                        'score': score,
                        'weight': weight
                    })

                except ValueError as ve:
                    print(f" Ooops Invalid number at line {line_num}: {ve}")
                    sys.exit(1)

        if not assignments:
            print("Ooops The CSV file has no data rows.")
            sys.exit(1)

        return assignments

    except Exception as e:
        print(f"Ooops Unexpected error while reading file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    print("\n=== Processing Grades ===")

    # Initialize accumulators
    total_weight = 0.0
    formative_weight = 0.0
    summative_weight = 0.0
    total_weighted_grade = 0.0
    formative_weighted_grade = 0.0
    summative_weighted_grade = 0.0
    failed_formative = []  # to store (assignment, weight, score)

    # Process each record
    for record in data:
        assignment = record['assignment']
        group = record['group'].lower()
        score = record['score']
        weight = record['weight']

        # Score validation
        if score < 0 or score > 100:
            print(f"Ooops at line {record['line_num']}:  "
            f"Score '{score}' for '{assignment}' is out of range." 
            "valid scores must be between 0 and 100.")
            sys.exit(1)

        # Weight accumulation
        total_weight += weight
        if group == 'formative':
            formative_weight += weight
        elif group == 'summative':
            summative_weight += weight
        else:
    print(f"Ooops at line {record['line_num']}: "
          f"Unknown group '{record['group']}' for assignment '{assignment}'. "
          "Valid groups are 'formative' or 'summative'.")
    sys.exit(1)

	
        # Weighted contribution
        weighted_contrib = (score * weight) / 100
        total_weighted_grade += weighted_contrib
        if group == 'formative':
            formative_weighted_grade += weighted_contrib
        elif group == 'summative':
            summative_weighted_grade += weighted_contrib

        # Collect failed formative assignments (score < 50)
        if group == 'formative' and score < 50:
            failed_formative.append((assignment, weight, score))

    # Weight validation after processing all records
if total_weight != 100:
    print(f"Ooops Total weight is {total_weight}, but expected 100. "
          "Please check your CSV weights.")
    sys.exit(1)

if formative_weight != 60:
    print(f"Ooops Formative total weight is {formative_weight}, but expected 60. "
          "Ensure formative assignments add up correctly.")
    sys.exit(1)

if summative_weight != 40:
    print(f"Ooops Summative total weight is {summative_weight}, but expected 40. "
          "Ensure summative assignments add up correctly.")
    sys.exit(1)

    # Final calculations
    final_grade = total_weighted_grade
    gpa = (final_grade / 100) * 5

    # Average percentages per category (weighted sum / total weight * 100)
    formative_average = (formative_weighted_grade / formative_weight) * 100 if formative_weight > 0 else 0
    summative_average = (summative_weighted_grade / summative_weight) * 100 if summative_weight > 0 else 0

    # Pass/Fail decision
    passed = (formative_average >= 50) and (summative_average >= 50)
    status = "PASSED" if passed else "FAILED"

    # Output results
    print(f"Formative average: {formative_average:.2f}%")
    print(f"Summative average: {summative_average:.2f}%")
    print(f"Final Grade: {final_grade:.2f} / 100")
    print(f"GPA: {gpa:.2f} / 5.0")
    print(f"Result: {status}")

    # Resubmission logic for failed formative assignments

    if len(failed_formative) > 0:
    # 1. Find the highest weight among failed formative assignments
        highest_weight = 0
        for item in failed_formative:
            assignment_name = item[0]
            weight = item[1]
            score = item[2]
            if weight > highest_weight:
                highest_weight = weight

    # 2. Collect all assignments that have that highest weight
        eligible_assignments = []
        for item in failed_formative:
            assignment_name = item[0]
            weight = item[1]
            score = item[2]
            if weight == highest_weight:
                eligible_assignments.append(assignment_name)

    # 3. Print the result
        if len(eligible_assignments) == 1:
            print(f"Assignment to resubmit: {eligible_assignments[0]}")
        else:
        # join the list into a string with commas
            assignments_str = ', '.join(eligible_assignments)
            print(f"Assignments to resubmit: {assignments_str}")

    else:
        print("No resubmission needed.")
     
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
