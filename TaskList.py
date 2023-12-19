class TaskList:    
    """
    Represents a list of tasks with the ability to add and remove tasks.

    Attributes:
        tasks (list): A list to store Task objects.
    """

    def __init__(self):
        """
        Initializes a new TaskList object with an empty list of tasks.
        """
        self.taskList = []

    def add_task(self, task):
        """
        Adds a task to the task list.

        Parameters:
            task (Task): The Task object to be added.
        """
        self.taskList.append(task)

    def remove_task(self, task):
        """
        Removes a task from the task list.

        Parameters:
            task (Task): The Task object to be removed.
        """
        self.taskList.remove(task)

    def display_all_tasks(self):
        """
        Display detailed information about all tasks in the list.
        """
        print("All tasks:\n-------")

        for task in self.taskList:
            task.display_task_details()
            print("-------")


from Task import Task
if __name__ == "__main__":
    # Example usage:
    task_list = TaskList()

    task1 = Task("Project A", "Development")
    task2 = Task("Project B", "Testing")

    task_list.add_task(task1)
    task_list.add_task(task2)

    
    task_list.display_all_tasks()

    print("\nRemoving task1:")
    task_list.remove_task(task1)

    print("Remaining tasks:\n")
    task_list.display_all_tasks()
