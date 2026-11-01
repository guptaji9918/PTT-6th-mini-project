giimport os
import json
import csv
from datetime import datetime

DATA_FILE = "students.json"
CSV_FILE = "students.csv"
LOG_FILE = "activity_log.txt"
SUBJECTS = ("Python", "Maths", "DBMS")


def load_students(path=DATA_FILE):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("JSON root must be a dictionary.")
        return data
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Could not load {path}: {error}")
        print("Existing file has been preserved. No records were loaded.")
        return None


def save_students(students, path=DATA_FILE):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)
    print(f"Records saved to {path}.")


def log_activity(message, path=LOG_FILE):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def get_marks():
    marks = {}
    for subject in SUBJECTS:
        while True:
            value = input(f"{subject} marks (0-100): ").strip()
            try:
                mark = float(value)
                if not 0 <= mark <= 100:
                    print("Marks must be between 0 and 100.")
                    continue
                marks[subject] = mark
                break
            except ValueError:
                print("Please enter a numeric mark.")
    return marks


def add_student(students):
    student_id = input("Student ID: ").strip()
    if not student_id:
        print("Student ID cannot be empty.")
        return
    if student_id in students:
        print("That student ID already exists.")
        return

    name = input("Name: ").strip()
    department = input("Department: ").strip()
    if not name or not department:
        print("Name and department cannot be empty.")
        return

    students[student_id] = {
        "name": name,
        "department": department,
        "marks": get_marks()
    }
    save_students(students)
    log_activity(f"Added student record: {student_id}")
    print("Student record added.")


def update_student(students):
    student_id = input("Student ID to update: ").strip()
    if student_id not in students:
        print("Student not found.")
        return
    name = input(f"Name [{students[student_id]['name']}]: ").strip()
    department = input(f"Department [{students[student_id]['department']}]: ").strip()
    if name:
        students[student_id]["name"] = name
    if department:
        students[student_id]["department"] = department
    print("Enter the three subject marks:")
    students[student_id]["marks"] = get_marks()
    save_students(students)
    log_activity(f"Updated student record: {student_id}")
    print("Student record updated.")


def display_student(student_id, record):
    marks = record["marks"]
    print(f"\nID: {student_id}")
    print(f"Name: {record['name']} | Department: {record['department']}")
    print(" | ".join(f"{subject}: {marks[subject]}" for subject in SUBJECTS))


def search_student(students):
    student_id = input("Enter student ID: ").strip()
    record = students.get(student_id)
    if record is None:
        print("Student not found.")
    else:
        display_student(student_id, record)


def list_students(students):
    if not students:
        print("No student records.")
        return
    for student_id, record in students.items():
        display_student(student_id, record)


def export_csv(students, path=CSV_FILE):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", "Name", "Department", *SUBJECTS])
        for student_id, record in students.items():
            writer.writerow([
                student_id, record["name"], record["department"],
                *(record["marks"][subject] for subject in SUBJECTS)
            ])
    log_activity(f"Exported student records to {path}")
    print(f"CSV export completed: {path}")


def view_log():
    if not os.path.exists(LOG_FILE):
        print("Activity log does not exist yet.")
        return
    print("\n1. read()  2. readline()  3. readlines()")
    choice = input("Choose reading method: ").strip()
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        if choice == "1":
            print(file.read(), end="")
        elif choice == "2":
            print(file.readline(), end="")
        elif choice == "3":
            print("".join(file.readlines()), end="")
        else:
            print("Invalid choice.")


def demonstrate_json_strings(students):
    student_id = input("Student ID for JSON string demonstration: ").strip()
    if student_id not in students:
        print("Student not found.")
        return
    json_text = json.dumps(students[student_id], indent=4)
    print("\nJSON string:")
    print(json_text)
    restored_record = json.loads(json_text)
    print("\nParsed back into Python:")
    print(restored_record)


def demonstrate_text_writing():
    """Demonstrate write() and writelines() using a separate demonstration file."""
    demo_path = "text_methods_demo.txt"
    with open(demo_path, "w", encoding="utf-8") as file:
        file.write("Text file handling demonstration\n")
    with open(demo_path, "a", encoding="utf-8") as file:
        file.writelines(["write() wrote the first line.\n", "writelines() wrote this line.\n"])
    print(f"Demonstration written to {demo_path}.")


def main():
    students = load_students()
    if students is None:
        print("Program stopped to protect the existing JSON file.")
        return

    while True:
        print("\nSTUDENT RECORDS SYSTEM")
        print("1. Add student")
        print("2. Update student")
        print("3. Search student")
        print("4. List all students")
        print("5. Export records to CSV")
        print("6. View activity log")
        print("7. JSON string demonstration")
        print("8. Demonstrate write() and writelines()")
        print("9. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            update_student(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            list_students(students)
        elif choice == "5":
            export_csv(students)
        elif choice == "6":
            view_log()
        elif choice == "7":
            demonstrate_json_strings(students)
        elif choice == "8":
            demonstrate_text_writing()
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "_main_":
    main()