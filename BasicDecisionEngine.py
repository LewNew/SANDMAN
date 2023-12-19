from Task import Task
from TaskList import TaskList

class BasicDecisionEngine:
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

    def make_decision(self)
        """
        method that decideds what task to do
        """
        #TODO
        pass

# Example usage:
if __name__ == "__main__":
        
    decision_engine = BasicDecisionEngine()

    task1 = Task("Project A", "Development")
    task2 = Task("Project B", "Testing")

    # Now add tasks to the TaskList inside BasicDecisionEngine
    decision_engine.task_list.add_task(task1)
    decision_engine.task_list.add_task(task2)

    print("All tasks:")
    decision_engine.task_list.print_all_tasks()
