class TaskList:
    """
    Represents a list of tasks with the ability to add and remove tasks.

    Attributes:
        tasks (list): A list to store Task objects.

    Methods:
        add_task(Task)
        remove_task(Task)
        print_all_tasks()
    """

    def __init__(self):
        """
        Initializes a new TaskList object with an empty list of tasks.
        """

        # TODO probably load tasks from a json file as default tasks??? maybe that should be created by the D-engine???

        self.taskList = []

    def add_task(self, task):
        """
        Adds a task to the task list.

        Parameters:
            task (Task): The Task object to be added.
        """

        # makes sure that a Task object was passed into the method
        if not isinstance(task, Task):
            raise TypeError(f"Expected a Task object, but received {type(task)}")

        self.taskList.append(task)

    def remove_task(self, task):
        """
        Removes a task from the task list.

        Parameters:
            task (Task): The Task object to be removed.
        """

        # makes sure that a Task object was passed into the method
        if not isinstance(task, Task):
            raise TypeError(f"Expected a Task object, but received {type(task)}")

        self.taskList.remove(task)

    def print_all_tasks(self):
        """
        Display detailed information about all tasks in the list.
        """
        print("All tasks:\n-------")

        for task in self.taskList:
            task.display_task_details()
            print("-------")


if __name__ == "__main__":
    from Task import Task

    # Example usage:
    task_list = TaskList()

    task1 = Task("Project A", "Development")
    task2 = Task("Project B", "Testing")

    task_list.add_task(task1)
    task_list.add_task(task2)

    task_list.print_all_tasks()

    print("\nRemoving task1:")
    task_list.remove_task(task1)

    print("Remaining tasks:\n")
    task_list.print_all_tasks()