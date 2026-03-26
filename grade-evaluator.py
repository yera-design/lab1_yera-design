#!/usr/bin/python3
import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process: ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })

        if not assignments:
            print("Ooops the CSV file has no data.")
            sys.exit(1)

        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    print("\n--- Processing Grades ---")

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
            print(f"Error: Invalid score {score} for '{assignment}'.")
            sys.exit(1)

        # Weight accumulation
        total_weight += weight
        if group == 'formative':
            formative_weight += weight
        elif group == 'summative':
            summative_weight += weight
        else:
            print(f"Error: Unknown group '{record['group']}' for assignment '{assignment}'")
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
        print(f"Error: Total weight sum = {total_weight}, expected 100.")
        sys.exit(1)
    if formative_weight != 60:
        print(f"Error: Formative total weight = {formative_weight}, expected 60.")
        sys.exit(1)
    if summative_weight != 40:
        print(f"Error: Summative total weight = {summative_weight}, expected 40.")
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
