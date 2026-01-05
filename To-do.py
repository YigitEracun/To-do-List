from datetime import date

# -------------------- CLASS --------------------
class Task:  # Creating a class to define the term "task"
    def __init__(self, name, desc, importance, completation, deadline):
        self.name = name
        self.desc = desc
        self.importance = importance
        self.completation = completation
        self.deadline = deadline

    def __str__(self):
        status = "Completed" if self.completation else "Pending"  # Completion status
        return f"{self.name} | {importance_text(self.importance)} | {self.deadline} | {status}"


# Global task list
Task_list = []  # This list stores tasks.

# -------------------- FILE OPERATIONS --------------------
def load_tasks(filename="tasks.txt"):
    """Load tasks from a text file into Task_list."""
    global Task_list
    Task_list = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                name, desc, importance, completation, deadline = line.split("|")
                task = Task(
                    name,
                    desc,
                    int(importance),
                    completation == "True",
                    date.fromisoformat(deadline)
                )
                Task_list.append(task)
    except FileNotFoundError:
        Task_list = []


def save_tasks(filename="tasks.txt"):
    """Save all tasks from Task_list into a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        for task in Task_list:
            line = f"{task.name}|{task.desc}|{task.importance}|{task.completation}|{task.deadline.isoformat()}\n"
            f.write(line)
# ---------------------------------------------------------

# -------------------- INPUT HELPERS --------------------
def get_valid_date():
    """Ensure the user enters a valid date."""
    while True:
        try:
            year = int(input("Deadline year: "))
            month = int(input("Deadline month: "))
            day = int(input("Deadline day: "))
            return date(year, month, day)
        except ValueError:
            print("Invalid date! Please enter a correct date.")


def get_task_importance():
    """Ensure the user enters a valid importance level."""
    while True:
        importance = input("Choose importance level (Low-Medium-High): ").capitalize()
        if importance == "Low":
            return 1
        elif importance == "Medium":
            return 2
        elif importance == "High":
            return 3
        print("Invalid input! Please enter Low, Medium or High.")


def importance_text(value):
    """Convert numeric importance to text."""
    return {1: "Low", 2: "Medium", 3: "High"}[value]

# -------------------- SORTING --------------------
def Sort_tasks():
    """Sort tasks by completion, importance, and closest deadline."""
    Task_list.sort(
        key=lambda task: (task.completation, -task.importance, task.deadline)
    )

# -------------------- LIST TASK --------------------
def List_task():
    """List all tasks and optionally show a task's description."""
    Sort_tasks()
    if not Task_list:
        print("No tasks available.")
        return

    # Print all tasks with index
    for i, task in enumerate(Task_list, 1):
        print(f"{i}. {task}")

    # Ask if user wants to read a description
    read_desc = input("Would you like to read a task description? (yes/no): ").lower()
    if read_desc == "yes":
        while True:
            try:
                num = int(input("Enter task number: "))
                if 1 <= num <= len(Task_list):
                    print("\n--- TASK DESCRIPTION ---")
                    print(Task_list[num - 1].desc)
                    print("------------------------\n")
                    break
                else:
                    print("Invalid task number!")
            except ValueError:
                print("Please enter a valid number!")

# -------------------- ADD TASK --------------------
def Add_task():
    """Add a new task to the list."""
    while True:
        task_name = input("Please enter the task's name: ").strip()
        if task_name:
            break
        print("Task name cannot be empty!")

    while True:
        task_desc = input("Please describe the task: ").strip()
        if task_desc:
            break
        print("Task description cannot be empty!")

    task_importance = get_task_importance()
    task_deadline = get_valid_date()

    new_task = Task(task_name, task_desc, task_importance, False, task_deadline)
    Task_list.append(new_task)
    print(f"Task '{task_name}' added successfully!")

    Sort_tasks()
    save_tasks()

# -------------------- EDIT TASK --------------------
def Edit_task():
    """Edit an existing task."""
    List_task()
    if not Task_list:
        return

    while True:
        try:
            num = int(input("Enter the number of the task you want to edit: "))
            if 1 <= num <= len(Task_list):
                task = Task_list[num - 1]
                break
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

    while True:
        print("Which attribute do you want to edit?")
        print("Name - description - importance - completion - deadline")
        edit_choose = input().lower()

        if edit_choose == "name":
            task.name = input("New name: ").strip()
        elif edit_choose == "description":
            task.desc = input("New description: ").strip()
        elif edit_choose == "importance":
            task.importance = get_task_importance()
        elif edit_choose == "completion":
            task.completation = input("Completed? (yes/no): ").lower() == "yes"
        elif edit_choose == "deadline":
            task.deadline = get_valid_date()
        else:
            print("Invalid choice!")
            continue

        if input("Edit anything else? (yes/no): ").lower() == "no":
            break

    save_tasks()

# -------------------- DELETE TASK --------------------
def Delete_task():
    """Delete a task from the list."""
    List_task()
    if not Task_list:
        return

    while True:
        try:
            num = int(input("Enter the number of the task you want to delete: "))
            if 1 <= num <= len(Task_list):
                removed = Task_list.pop(num - 1)
                print(f"Task '{removed.name}' deleted.")
                save_tasks()
                break
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

# -------------------- MAIN PROGRAM --------------------
def Main():
    load_tasks()
    print("Hello! Welcome to To-do list program!")

    while True:
        print("\n1-List tasks")
        print("2-Add new task")
        print("3-Edit task")
        print("4-Delete task")
        print("5-Exit")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid input!")
            continue

        if choice == 1:
            List_task()
        elif choice == 2:
            Add_task()
        elif choice == 3:
            Edit_task()
        elif choice == 4:
            Delete_task()
        elif choice == 5:
            print("Exiting program...")
            break
        else:
            print("Invalid option!")

        if input("Would you like to do anything else? (yes/no): ").lower() != "yes":
            break

# -------------------- RUN PROGRAM --------------------
if __name__ == "__main__":
    Main()
