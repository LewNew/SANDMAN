from datetime import datetime
from abc import ABC, abstractmethod

class Task:
    """
    Represents a task with details such as name, type, inception time, percent complete, and last worked on.
    this class overwrites __str__ so it can be printed

    Attributes:
        name (str): The name of the task.
        type (str): The type or category of the task.
        percent_complete (int): The percentage of completion for the task.
        last_worked_on (str, optional): The date when the task was last worked on. Default is None.
        inception_time (str, optional): The date and time when the task was created. Default is the current time.

    Methods:
        set_last_worked_on(datatime=None): Set the last worked on time for the task. If no time is provided, the current time is used.
        get_task_data(): Return a dictionary containing the task data.
    """

    def __init__(self, name, task_type, percent_complete=0, last_worked_on=None, inception_time=None,channel=None,task_list=None):
        """
        Initializes a new Task object.

        Parameters:
            name (str): The name of the task.
            task_type (str): The type or category of the task.
            percent_complete (int, optional): The percentage of completion for the task.
            last_worked_on (datetime, optional): The date when the task was last worked on. Default is None.
            inception_time (datetime, optional): The date and time when the task was created. Default is the current time.
        """

        #TODO not finished this __init__ will most likely change
        #TODO probably add channel object that does not exsist yet

        # print(task_list)

        self.name = name
        self.task_type = task_type
        self.percent_complete = percent_complete
        #TODO add functionality to manulary set last_worked_on and inception_time
        self.last_worked_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.inception_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.channel = channel
        self.task_list=task_list


    def __str__(self):
        """
        Return a string representation of the Task.

        Returns:
            str: A formatted string representing the Task.
        """
        #TODO Task does not print its parent task list otherwise printing a TaskList or task would cause an infinate recuresie look
        # might want to change this
        task_details_str = "\n".join(f"{key}: {value}" for key, value in vars(self).items() if key != 'task_list')
        return f"{task_details_str}"

    def add_to_parent_task_list(self,task):
        self.task_list.add_task(task)

    def remvoe_from_parent_task_list(self,task):
        self.task_list.remove_task(task)


    def set_last_worked_on(self, datatime=None):
        """
        Set the last worked on time for the task. If no time is provided, the current time is used.

        Parameters:
            datatime (str, optional): The date and time to set as the last worked on time. Default is None.
        """
        # TODO: Add functionality to manually set last_worked_on
        self.last_worked_on = datatime if datatime else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_task_data(self):
        """
        Return a dictionary containing the task data.

        Returns:
            dict: A dictionary containing task data.
        """
        return vars(self)

    def finish_work(self):
        """
        finihsed work method to set percent complete 100
        #TODO maybe not the best way of doing this
        """
        self.percent_complete = 100
        self.set_last_worked_on()

        return True


    #TODO replace **kwargs with persona which is a instance of persona
    @abstractmethod
    def do_work(self,persona=None,mood=None,memory=None):
        """
        abstract method for sub classes to implement to facilitate the funcionality of a task

        e.g. a "do word document" task will have a do_work function that will facilitate writeing into a word document
        the purpose of this is so that lots of different types of work will have differnet ways of completeing it
        but they will all have a do_work function so all the Task object can be treated the same by the decision engine ragardless of the type of task
        hopefully makeing it extendable as if you want to add a new type of task you can extand tast and implement the do_work function
        without needing to change task list or the decision engine.
        """
        raise NotImplementedError("do_work method must be implemented in the concrete subclass")

    @abstractmethod
    def read_work(self,**kwargs):
        """
        abstract method for sub classes to implement to facilitate reading the work they have done or reading communication e.g. reading an email
        or reading a partialy complete word document to then continue that word document

        """
        raise NotImplementedError("do_work method must be implemented in the concrete subclass")



# Example usage:      
if __name__ == "__main__":

    task1 = Task("Project A", "Development")
    print(task1)


