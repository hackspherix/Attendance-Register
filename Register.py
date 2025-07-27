import hashlib
import getpass
import datetime
import os

# Define data containers
users = {}
students = {}
attendance_records = {}

# --- UTILITY FUNCTION ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- USER MANAGEMENT ---

def save_users():
    with open(".users.txt", "w") as file:
        for username, hashed_password in users.items():
            file.write(f"{username}:{hashed_password}\n")

def load_users():
    if os.path.exists(".users.txt"):
        with open(".users.txt", "r") as file:
            for line in file:
                username, hashed_password = line.strip().split(":")
                users[username] = hashed_password

def register_user():
    clear_screen()
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[username] = hashed_password
    save_users()
    print("User registered successfully!")

def login_user():
    clear_screen()
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in users and users[username] == hashed_password:
        return True
    else:
        return False

# --- STUDENT MANAGEMENT ---

def save_students():
    with open(".students.txt", "w") as file:
        for roll_number, name in students.items():
            file.write(f"{roll_number}:{name}\n")

def load_students():
    if os.path.exists(".students.txt"):
        with open(".students.txt", "r") as file:
            for line in file:
                roll_number, name = line.strip().split(":")
                students[roll_number] = name
                attendance_records[roll_number] = load_attendance(roll_number)

def add_student():
    clear_screen()
    roll_number = input("Enter roll number: ")
    name = input("Enter student name: ")
    students[roll_number] = name
    attendance_records[roll_number] = []
    save_students()
    print("Student added successfully!")

def view_students():
    clear_screen()
    print("\nStudent List:")
    for roll_number, name in students.items():
        print(f"Roll no: {roll_number}. name: {name}")
    print()

def edit_student():
    clear_screen()
    roll_number = input("Enter roll number of student to edit: ")
    if roll_number in students:
        print("1. Edit Roll Number")
        print("2. Edit Name")
        choice = input("Enter your choice: ")
        if choice == "1":
            new_roll_number = input("Enter new roll number: ")
            students[new_roll_number] = students.pop(roll_number)
            attendance_records[new_roll_number] = attendance_records.pop(roll_number)
            save_students()
            print("Roll number updated successfully!")
        elif choice == "2":
            new_name = input("Enter new name: ")
            students[roll_number] = new_name
            save_students()
            print("Name updated successfully!")
        else:
            print("Invalid choice.")
    else:
        print("Student not found.")

def delete_student():
    clear_screen()
    roll_number = input("Enter roll number of student to delete: ")
    if roll_number in students:
        del students[roll_number]
        del attendance_records[roll_number]
        save_students()
        print("Student deleted successfully!")
    else:
        print("Student not found.")

# --- ATTENDANCE MANAGEMENT ---

def mark_attendance(roll_number):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attendance_records[roll_number].append(current_time)
    save_attendance(roll_number)
    print(f"Attendance marked for {students[roll_number]} at {current_time}")

def view_attendance(roll_number):
    clear_screen()
    if roll_number in students:
        print(f"\nAttendance Records for {students[roll_number]}:")
        for idx, record in enumerate(attendance_records[roll_number], start=1):
            print(f"{idx}. {record}")
        print()
    else:
        print("Student not found.")

def save_attendance(roll_number):
    folder_name = "students"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_name = f"{folder_name}/{students[roll_number]}.txt"
    with open(file_name, "w") as file:
        for record in attendance_records[roll_number]:
            file.write(f"{record}\n")

def load_attendance(roll_number):
    records = []
    folder_name = "students"
    student_name = students.get(roll_number)
    if not student_name:
        return records
    file_name = f"{folder_name}/{student_name}.txt"
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            records = [line.strip() for line in file.readlines()]
    return records

# --- MAIN MENU ---

def main():
    load_users()
    load_students()

    while True:
        clear_screen()
        print("\n--- Attendance System ---")
        print("1. Register User")
        print("2. Login User")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            if login_user():
                print("Login successfully!")
                while True:
                    clear_screen()
                    print("\n--- Student Management ---")
                    print("1. Add Student")
                    print("2. View Students")
                    print("3. Edit Student")
                    print("4. Delete Student")
                    print("5. Mark Attendance")
                    print("6. View Attendance")
                    print("7. Logout")
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        add_student()
                    elif choice == "2":
                        view_students()
                        input("Press Enter to return...")
                    elif choice == "3":
                        edit_student()
                        input("Press Enter to return...")
                    elif choice == "4":
                        delete_student()
                        input("Press Enter to return...")
                    elif choice == "5":
                        while True:
                            view_students()
                            roll_number = input("Enter roll number to mark attendance (or type 'back' to return): ")
                            if roll_number.lower() == "back":
                                break
                            if roll_number in students:
                                mark_attendance(roll_number)
                            else:
                                print("Student not found.")
                            input("Press Enter to continue...")
                    elif choice == "6":
                        roll_number = input("Enter roll number to view attendance: ")
                        view_attendance(roll_number)
                        input("Press Enter to return...")
                    elif choice == "7":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please try again.")
                        input("Press Enter to continue...")
            else:
                print("Invalid username or password.")
                input("Press Enter to try again...")
        elif choice == "3":
            print("Exiting system. Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
