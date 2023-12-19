from datetime import datetime

class Task:
    """
    Represents a task with details such as name, type, inception time, percent complete, and last worked on.

    Attributes:
        name (str): The name of the task.
        type (str): The type or category of the task.
        percent_complete (int): The percentage of completion for the task.
        last_worked_on (str, optional): The date when the task was last worked on. Default is None.
        inception_time (str, optional): The date and time when the task was created. Default is the current time.

    Methods:
        display_task_details(): Display detailed information about the task.
        set_last_worked_on(datatime=None): Set the last worked on time for the task. If no time is provided, the current time is used.
        get_task_data(): Return a dictionary containing the task data.
    """

    def __init__(self, name, task_type, percent_complete=0, last_worked_on=None, inception_time=None):
        """
        Initializes a new Task object.

        Parameters:
            name (str): The name of the task.
            task_type (str): The type or category of the task.
            percent_complete (int, optional): The percentage of completion for the task.
            last_worked_on (str, optional): The date when the task was last worked on. Default is None.
            inception_time (str, optional): The date and time when the task was created. Default is the current time.
        """

        #TODO not finished this __init__ will most likely change

        self.name = name
        self.task_type = task_type
        self.percent_complete = percent_complete
        #TODO add functionality to manulary set last_worked_on and inception_time
        self.last_worked_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.inception_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def set_last_worked_on(self, datatime=None):
        """
        Set the last worked on time for the task. If no time is provided, the current time is used.

        Parameters:
            datatime (str, optional): The date and time to set as the last worked on time. Default is None.
        """
        # TODO: Add functionality to manually set last_worked_on
        self.last_worked_on = datatime if datatime else datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def display_task_details(self):
        """
        Display detailed information about the task.
        """
        print(f"Task: {self.name}")
        print(f"Type: {self.task_type}")
        print(f"Inception Time: {self.inception_time}")
        print(f"Percent Complete: {self.percent_complete}%")
        print(f"Last Worked On: {self.last_worked_on}")

    def get_task_data(self):
        """
        Return a dictionary containing the task data.

        Returns:
            dict: A dictionary containing task data.
        """
        return {
            "name": self.name,
            "type": self.type,
            "percent_complete": self.percent_complete,
            "last_worked_on": self.last_worked_on,
            "inception_time": self.inception_time
        }


    

        
if __name__ == "__main__":
    # Example usage:
    task1 = Task("Project A", "Development")
    task1.display_task_details()
    task1.set_last_worked_on()
