from Task import Task
from TaskList import TaskList

class DecisionEngine:
    """
    Represents a basic decision engine with a task list.

    Attributes:
        task_list (TaskList): An instance of TaskList to store Task objects.
    """

    def __init__(self):
        """
        Initializes a new BasicDecisionEngine object with an empty task list.
        """
        self.task_list = TaskList()

    def make_decision(self):
        """
        Decides what task to do next based on the duration the task has been pending and the completion percentage.

        Returns:
            Task: The next task to be executed.
        """
        if not self.task_list.taskList:
            return None  # If no tasks are available, return None

        # Sort tasks by duration they have been pending (from time_created to last_worked)
        self.task_list.taskList.sort(key=lambda task: task.get_duration(), reverse=True)

        # If there are tasks that are nearly complete, prioritize them
        nearly_complete_tasks = [task for task in self.task_list.taskList if task.percent_complete > 80]
        if nearly_complete_tasks:
            # Assuming the personality trait 'completionist' is high, prioritize tasks that are almost complete
            # Need to define personality traits. Completionist is just a trait for an agent that intends to complete
            # ongoing or pending tasks prior to starting new ones.
            return nearly_complete_tasks[0]

        # Otherwise, return the task with the longest duration
        return self.task_list.taskList[0]

    def execute_task(self, task):
        """
        Executes the chosen task. This function would typically trigger the task's do_work method.

        Parameters:
            task (Task): The task to be executed.
        """
        # TODO: Implement the logic to execute the task
        print(f"Executing task: {task.name}")
        # Assuming the Task class has a method 'do_work' that handles task execution
        task.do_work()

    def send_to_channel(self, task):
        """
        Sends the chosen task to the appropriate channel for execution.

        Parameters:
            task (Task): The task to be sent to the channel.
        """
        # TODO: Implement the logic to send the task to the channel
        print(f"Sending task '{task.name}' to its appropriate channel for execution.")


# Example usage:
if __name__ == "__main__":
    decision_engine = DecisionEngine()

    task1 = Task("Project A", "Development")
    task2 = Task("Project B", "Testing")

    # Now add tasks to the TaskList inside BasicDecisionEngine
    decision_engine.task_list.add_task(task1)
    decision_engine.task_list.add_task(task2)

    # Decide on the next task and execute it
    next_task = decision_engine.make_decision()
    if next_task:
        print("Next task to do:")
        next_task.display_task_details()
        decision_engine.execute_task(next_task)
        decision_engine.send_to_channel(next_task)
    else:
        print("No tasks to do.")
