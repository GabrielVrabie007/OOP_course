import json

class Student:
    def __init__(self, name, student_id, email, group):
        self.name = name
        self.student_id = student_id
        self.email = email
        self.graduated = False
        self.group = group

    def graduate(self):
        self.graduated = True

    def __repr__(self):
        return f"Student(name={self.name}, id={self.student_id}, email={self.email}, graduated={self.graduated}, group={self.group})"


class Faculty:
    def __init__(self, name, field):
        self.name = name
        self.field = field
        self.enrolled_students = []
        self.graduates = []

    def add_student(self, student):
        self.enrolled_students.append(student)

    def graduate_student(self, student_id):
        for student in self.enrolled_students:
            if student.student_id == student_id:
                student.graduate()
                self.graduates.append(student)
                self.enrolled_students.remove(student)
                return f"{student.name} has graduated."
        return "Student not found."

    def is_student_enrolled(self, student_id):
        return any(student.student_id == student_id for student in self.enrolled_students)

    def display_enrolled_students(self):
        return [student for student in self.enrolled_students]

    def display_graduates(self):
        return [student for student in self.graduates]

    def __repr__(self):
        return f"Faculty(name={self.name}, field={self.field})"


class University:
    def __init__(self):
        self.faculties = []
        self.last_student_id = 0
        self.load_data()

    def create_faculty(self, name, field):
        faculty = Faculty(name, field)
        self.faculties.append(faculty)
        self.save_data()

    def generate_student_id(self):
        self.last_student_id += 1
        return f"{self.last_student_id:04d}"

    def assign_student_to_faculty(self, faculty_name, student):
        faculty = self.get_faculty_by_name(faculty_name)
        if faculty:
            faculty.add_student(student)
            self.save_data()
            return f"Student {student.name} assigned to {faculty_name}."
        return "Faculty not found."

    def graduate_student(self, faculty_name, student_id):
        faculty = self.get_faculty_by_name(faculty_name)
        if faculty:
            result = faculty.graduate_student(student_id)
            self.save_data()
            return result
        return "Faculty not found."

    def get_faculty_by_name(self, name):
        for faculty in self.faculties:
            if faculty.name == name:
                return faculty
        return None

    def search_student_faculty(self, email):
        for faculty in self.faculties:
            for student in faculty.enrolled_students:
                if student.email == email:
                    return faculty.name
        return "Student not found."

    def display_faculties(self):
        return [faculty.name for faculty in self.faculties]

    def display_faculties_by_field(self, field):
        return [faculty.name for faculty in self.faculties if faculty.field == field]

    def save_data(self):
        data = {
            "faculties": [
                {
                    "name": faculty.name,
                    "field": faculty.field,
                    "enrolled_students": [
                        {"name": s.name, "id": s.student_id, "email": s.email, "graduated": s.graduated, "group": s.group}
                        for s in faculty.enrolled_students
                    ],
                    "graduates": [
                        {"name": s.name, "id": s.student_id, "email": s.email, "graduated": s.graduated, "group": s.group}
                        for s in faculty.graduates
                    ]
                } for faculty in self.faculties
            ],
            "last_student_id": self.last_student_id
        }
        with open("university_data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open("university_data.json", "r") as file:
                data = json.load(file)
                self.last_student_id = data.get("last_student_id", 0)
                for faculty_data in data["faculties"]:
                    faculty = Faculty(faculty_data["name"], faculty_data["field"])

                    for student_data in faculty_data["enrolled_students"]:
                        group = student_data.get("group", "Unknown")
                        student = Student(student_data["name"], student_data["id"], student_data["email"], group)
                        student.graduated = student_data["graduated"]
                        faculty.add_student(student)

                    for graduate_data in faculty_data["graduates"]:
                        group = graduate_data.get("group", "Unknown")
                        graduate = Student(graduate_data["name"], graduate_data["id"], graduate_data["email"], group)
                        graduate.graduated = True
                        faculty.graduates.append(graduate)
                    self.faculties.append(faculty)
        except FileNotFoundError:
            print("No data file found, starting fresh.")
            pass

def main():
    university = University()

    while True:
        print("\n1. Create Faculty")
        print("2. Add Student")
        print("3. Graduate Student")
        print("4. Show Faculties")
        print("5. Search Student by Email")
        print("6. Show Faculties by Field")
        print("7. Exit")
        option = input("\nChoose an option: ")

        if option == '1':
            name = input("Enter faculty name: ")
            field = input("Enter faculty field: ")
            university.create_faculty(name, field)
            print(f"Faculty {name} has been created.")

        elif option == '2':
            faculty_name = input("Enter faculty name: ")
            student_name = input("Enter student's name: ")
            student_email = input("Enter student's email: ")
            student_id = university.generate_student_id()
            group = input("Enter student's group: ")
            student = Student(student_name, student_id, student_email, group)
            print(university.assign_student_to_faculty(faculty_name, student))

        elif option == '3':
            faculty_name = input("Enter faculty name: ")
            student_id = input("Enter student ID to graduate: ")
            print(university.graduate_student(faculty_name, student_id))

        elif option == '4':
            faculties = university.display_faculties()
            print("Existing faculties:", faculties)

        elif option == '5':
            student_email = input("Enter student's email: ")
            faculty = university.search_student_faculty(student_email)
            print(f"Student belongs to faculty: {faculty}")

        elif option == '6':
            field = input("Enter the field of the faculty: ")
            faculties_by_field = university.display_faculties_by_field(field)
            print(f"Faculties in {field}: {faculties_by_field}")

        elif option == '7':
            print("Exiting the program.")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()


