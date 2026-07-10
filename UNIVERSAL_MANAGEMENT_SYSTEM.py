# UNIVERSAL MANAGEMENT SYSTEM (Plain Text Version)

# base person class
class Person:
    def __init__(self, name, age, email, role):
        self.name = name
        self.age = age
        self.email = email
        self.role = role

    def show_details(self):
        print(f"Name: {self.name}, Age: {self.age}, Email: {self.email}, Role: {self.role}")


# Project class
class Project:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.manager = None
        self.members = []

    def assign_manager(self, person):
        self.manager = person
        print(f"{person.name} is now managing the project: {self.name}")

    def add_member(self, person):
        if person not in self.members:
            self.members.append(person)
            print(f"{person.name} added to project: {self.name}")
        else:
            print(f"{person.name} is already a member of {self.name}.")

    def show_details(self):
        print(f"\nProject: {self.name} ({self.code})")
        print(f"Manager: {self.manager.name if self.manager else 'None'}")
        if self.members:
            print("Members:", ", ".join([m.name for m in self.members]))
        else:
            print("No members yet.")


def save_data(people, projects):
    # Save people
    with open("people.txt", "w") as f:
        for p in people:
            f.write(f"{p.name},{p.age},{p.email},{p.role}\n")

    # Save projects
    with open("projects.txt", "w") as f:
        for pr in projects:
            manager_name = pr.manager.name if pr.manager else ""
            member_names = ";".join([m.name for m in pr.members])
            f.write(f"{pr.name},{pr.code},{manager_name},{member_names}\n")

    print("Data saved successfully.")


def load_data():
    people = []
    projects = []

    # Load people
    try:
        with open("people.txt", "r") as f:
            for line in f:
                name, age, email, role = line.strip().split(",")
                if not any(p.name == name for p in people):
                    people.append(Person(name, int(age), email, role))
    except FileNotFoundError:
        print("No people data found. Starting fresh.")

    # Load projects
    try:
        with open("projects.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                name, code = parts[0], parts[1]
                manager_name = parts[2] if len(parts) > 2 else ""
                members_str = parts[3] if len(parts) > 3 else ""

                project = Project(name, code)
                manager = next((p for p in people if p.name == manager_name), None)
                if manager:
                    project.manager = manager

                if members_str:
                    for mname in members_str.split(";"):
                        member = next((p for p in people if p.name == mname), None)
                        if member:
                            project.members.append(member)
                projects.append(project)
    except FileNotFoundError:
        print("No project data found. Starting fresh.")

    return people, projects


def main():
    people, projects = load_data()

    while True:
        print("\n=== UNIVERSAL MANAGEMENT SYSTEM ===")
        print("1. Add Person")
        print("2. Create Project")
        print("3. Assign Manager")
        print("4. Add Member to Project")
        print("5. Show All Details")
        print("6. Save Data")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter name: ")
            age = input("Enter age: ")
            if not age.isdigit():
                print("Invalid age.")
                continue
            age = int(age)
            email = input("Enter email: ")
            role = input("Enter role: ")
            if any(p.name == name for p in people):
                print("Person already exists.")
            else:
                people.append(Person(name, age, email, role))
                print(f"{name} added successfully.")

        elif choice == "2":
            pname = input("Enter project name: ")
            pcode = input("Enter project code: ")
            if any(pr.name == pname for pr in projects):
                print("Project already exists.")
            else:
                projects.append(Project(pname, pcode))
                print(f"Project '{pname}' created successfully.")

        elif choice == "3":
            pname = input("Enter project name: ")
            manager_name = input("Enter manager name: ")
            project = next((p for p in projects if p.name == pname), None)
            manager = next((p for p in people if p.name == manager_name), None)
            if project and manager:
                project.assign_manager(manager)
            else:
                print("Project or manager not found.")

        elif choice == "4":
            pname = input("Enter project name: ")
            member_name = input("Enter member name: ")
            project = next((p for p in projects if p.name == pname), None)
            member = next((p for p in people if p.name == member_name), None)
            if project and member:
                project.add_member(member)
            else:
                print("Project or member not found.")

        elif choice == "5":
            print("\n--- PEOPLE ---")
            if not people:
                print("No people available.")
            for p in people:
                p.show_details()

            print("\n--- PROJECTS ---")
            if not projects:
                print("No projects available.")
            for pr in projects:
                pr.show_details()

        elif choice == "6":
            save_data(people, projects)

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
