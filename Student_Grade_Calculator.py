# Student Grade Calculator - Advanced Version
# Calculates grades, GPA, CGPA and semester comparison

import json
import os

DATA_FILE = "student_records.json"

# Load saved records
def load_records():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save records
def save_records(records):
    with open(DATA_FILE, "w") as file:
        json.dump(records, file)

# Get letter grade
def get_grade(score):
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

# Convert score to grade point
def get_grade_point(score):
    if score >= 90:
        return 4.0
    elif score >= 80:
        return 3.7
    elif score >= 70:
        return 3.3
    elif score >= 60:
        return 3.0
    elif score >= 50:
        return 2.0
    else:
        return 0.0

# Calculate GPA for one semester
def calculate_gpa(marks):
    grade_points = [get_grade_point(mark) for mark in marks]
    return sum(grade_points) / len(grade_points)

# Calculate CGPA from all semesters
def calculate_cgpa(records, name):
    semesters = records.get(name, [])
    if not semesters:
        return 0.0
    all_points = []
    for semester in semesters:
        for mark in semester["marks"]:
            all_points.append(get_grade_point(mark))
    return sum(all_points) / len(all_points)

# Show single semester result
def show_result(name, semester, subjects, marks):
    average = sum(marks) / len(marks)
    gpa = calculate_gpa(marks)
    print(f"\n--- Semester {semester} Result ---")
    print(f"Student Name : {name}")
    print(f"{'Subject':<15} {'Marks':<8} {'Grade':<8} {'Points'}")
    print("-" * 45)
    for i in range(len(subjects)):
        grade = get_grade(marks[i])
        points = get_grade_point(marks[i])
        print(f"{subjects[i]:<15} {marks[i]:<8} {grade:<8} {points}")
    print("-" * 45)
    print(f"Average      : {average:.2f}")
    print(f"GPA          : {gpa:.2f}")
    if average >= 50:
        print("Status       : Passed ✓")
    else:
        print("Status       : Failed ✗")

# Show full academic record with CGPA
def show_full_record(records, name):
    semesters = records.get(name, [])
    if not semesters:
        print("No record found.")
        return
    print(f"\n=== Full Academic Record: {name} ===")
    print(f"{'Semester':<12} {'Average':<12} {'GPA':<10} {'Status'}")
    print("-" * 45)
    for sem in semesters:
        average = sum(sem["marks"]) / len(sem["marks"])
        gpa = calculate_gpa(sem["marks"])
        status = "Passed" if average >= 50 else "Failed"
        print(f"{sem['semester']:<12} {average:<12.2f} {gpa:<10.2f} {status}")
    cgpa = calculate_cgpa(records, name)
    print("-" * 45)
    print(f"CGPA         : {cgpa:.2f}")
    if cgpa >= 3.5:
        print("Standing     : Excellent")
    elif cgpa >= 3.0:
        print("Standing     : Good")
    elif cgpa >= 2.0:
        print("Standing     : Average")
    else:
        print("Standing     : Poor")

# Add new semester
def add_semester(records):
    subjects = ["Math", "English", "Science", "Python", "Database"]
    name = input("Enter student name: ")
    semester = input("Enter semester (e.g. Semester 1): ")
    marks = []
    print(f"\nEnter marks for {semester}:")
    for subject in subjects:
        while True:
            try:
                mark = int(input(f"  {subject}: "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                else:
                    print("  Please enter marks between 0 and 100")
            except ValueError:
                print("  Please enter a valid number")

    # Save to records
    if name not in records:
        records[name] = []
    records[name].append({
        "semester": semester,
        "marks": marks
    })
    save_records(records)
    show_result(name, semester, subjects, marks)
    return name

# Compare two semesters
def compare_semesters(records, name):
    semesters = records.get(name, [])
    if len(semesters) < 2:
        print("Need at least 2 semesters to compare.")
        return
    print(f"\n--- Semester Comparison for {name} ---")
    for i in range(1, len(semesters)):
        prev = semesters[i-1]
        curr = semesters[i]
        prev_gpa = calculate_gpa(prev["marks"])
        curr_gpa = calculate_gpa(curr["marks"])
        diff = curr_gpa - prev_gpa
        if diff > 0:
            trend = "Improved ↑"
        elif diff < 0:
            trend = "Dropped ↓"
        else:
            trend = "Same →"
        print(f"{prev['semester']} GPA: {prev_gpa:.2f} → {curr['semester']} GPA: {curr_gpa:.2f} | {trend}")

# Main menu
def show_menu():
    print("\n=== Student Grade Calculator ===")
    print("1. Add semester result")
    print("2. View full record and CGPA")
    print("3. Compare semesters")
    print("4. Exit")

def main():
    records = load_records()
    while True:
        show_menu()
        choice = input("Enter choice: ")
        if choice == "1":
            name = add_semester(records)
        elif choice == "2":
            name = input("Enter student name: ")
            show_full_record(records, name)
        elif choice == "3":
            name = input("Enter student name: ")
            compare_semesters(records, name)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

main()
