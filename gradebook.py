import json
import os

FILENAME = "gradebook.json"

# -----------------------------
# Load & Save
# -----------------------------
def load_data():
    if not os.path.exists(FILENAME):
        return {}
    with open(FILENAME, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------
# Features
# -----------------------------
def add_course(data):
    code = input("Course code: ").upper()

    if code in data:
        print("Course already exists!\n")
        return

    name = input("Course name: ")
    credits = float(input("Credits: "))
    score = float(input("Score (0–10): "))
    semester = input("Semester: ")

    if score < 0 or score > 10:
        print("Invalid score!\n")
        return

    data[code] = {
        "name": name,
        "credits": credits,
        "score": score,
        "semester": semester
    }
    save_data(data)
    print("Added!\n")


def update_course(data):
    code = input("Course code to update: ").upper()

    if code not in data:
        print("Not found!\n")
        return

    print("Press Enter to keep old value.")

    old = data[code]

    name = input(f"New name ({old['name']}): ") or old['name']
    credits = input(f"New credits ({old['credits']}): ")
    score = input(f"New score ({old['score']}): ")
    semester = input(f"New semester ({old['semester']}): ") or old['semester']

    credits = float(credits) if credits else old['credits']
    score = float(score) if score else old['score']

    data[code] = {
        "name": name,
        "credits": credits,
        "score": score,
        "semester": semester
    }
    save_data(data)
    print("Updated!\n")


def delete_course(data):
    code = input("Course to delete: ").upper()
    if code in data:
        del data[code]
        save_data(data)
        print("Deleted!\n")
    else:
        print("Not found!\n")


def view_courses(data):
    print("\n==== Gradebook ====")
    print("CODE  | NAME                | CRED | SCORE | SEM")
    print("-----------------------------------------------")

    for code, c in data.items():
        print(f"{code:<5} | {c['name']:<18} | {c['credits']:<4} | {c['score']:<5} | {c['semester']}")
    print()


def gpa_summary(data):
    if not data:
        print("No courses!\n")
        return

    total_points = 0
    total_credits = 0
    sem_gpa = {}

    for code, c in data.items():
        total_points += c["credits"] * c["score"]
        total_credits += c["credits"]

        sem = c["semester"]
        if sem not in sem_gpa:
            sem_gpa[sem] = {"points": 0, "credits": 0}
        sem_gpa[sem]["points"] += c["credits"] * c["score"]
        sem_gpa[sem]["credits"] += c["credits"]

    print("\n==== GPA Summary ====")
    print(f"Overall GPA: {total_points / total_credits:.2f}")

    for sem, s in sem_gpa.items():
        print(f"{sem} GPA: {s['points'] / s['credits']:.2f}")
    print()


# -----------------------------
# Main Menu
# -----------------------------
def main():
    data = load_data()

    while True:
        print("===== Gradebook Menu =====")
        print("1. Add course")
        print("2. Update course")
        print("3. Delete course")
        print("4. View gradebook")
        print("5. GPA summary")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_course(data)
        elif choice == "2":
            update_course(data)
        elif choice == "3":
            delete_course(data)
        elif choice == "4":
            view_courses(data)
        elif choice == "5":
            gpa_summary(data)
        elif choice == "0":
            break
        else:
            print("Invalid!\n")


if __name__ == "__main__":
    main()
