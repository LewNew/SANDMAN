from Task import Task
from ClassLoaderHelpers import LoadClasses
import random
import logging

class TaskList:    
    """
    this class overwrites __str__, __iter__ and __getitem__ so it functions as as list
    allowing of getting elements by doing TaskList[0] and iterateing over tasks
    in a loop e.g. for Task in TaskList

    Attributes:
        tasks (list): A list to store Task objects.

    Methods:
        add_task(Task)
        remove_task(Task)
    """
    
    def __init__(self, cfg_data):
        """
        Initializes a new TaskList object with an empty list of tasks.
        args:
            cfg_data: a dictionary which contains all the task classes, their configs and where to find them
        """
        #createing logger object for dbuging
        self.logger = logging.getLogger('logger.'+__name__)

        
        #TODO probably load tasks from a json file as default tasks??? maybe that should be created by the D-engine???
        self._task_classes = LoadClasses(cfg_data['TaskClasses'].keys(), cfg_data['TaskClassPath'])
        print('===================\nLoaded Task Classes')
        for key, value in self._task_classes.items():
            print(cfg_data['TaskClasses'][key]['Config'])
            self._task_classes[key]['Config'] = cfg_data['TaskClasses'][key]['Config']
            print(key)
            print(value['metadata'])
        
        print('\n\n')   

        self.taskList = []

    @property
    def task_classes(self):
        return self._task_classes

    #TODO removed this becase now that Tasks has the Task list
    def __str__(self):
        """
        Return a string representation of the TaskList.

        Returns:
            str: A formatted string representing all tasks in the TaskList.
        """
        tasks_str = "\n-------\n".join(str(task) for task in self.taskList)
        return f"All tasks:\n-------\n{tasks_str}\n-------"

    def __iter__(self):
        """
        Allow iteration over tasks in the task list.

        Yields:
            Task: The next Task object in the task list.
        """
        for task in self.taskList:
            yield task

    def __getitem__(self, index):
        """
        Allow accessing a task from the task list using square brackets.

        Parameters:
            index (int): The index of the task to retrieve.

        Returns:
            Task: The Task object at the specified index.
        """
        if 0 <= index < len(self.taskList):
            return self.taskList[index]
        else:
            raise IndexError("Index out of range")

    def add_task(self, task):
        """
        Adds a task to the task list.

        Parameters:
            task (Task): The Task object to be added.
        """

        #makes sure that a Task object was passed into the method
        if not isinstance(task, Task):
            raise TypeError(f"Expected a Task object, but received {type(task)}")

        self.taskList.append(task)
        task.TaskList = self

    def remove_task(self, task):
        """
        Removes a task from the task list.

        Parameters:
            task (Task): The Task object to be removed.
        """

        #makes sure that a Task object was passed into the method
        if not isinstance(task, Task):
            raise TypeError(f"Expected a Task object, but received {type(task)}")

        self.taskList.remove(task)



# Example usage:
if __name__ == "__main__":
    task_list = TaskList()

    task1 = Task("Project A", "Development")
    task2 = Task("Project B", "Testing")

    task_list.add_task(task1)
    task_list.add_task(task2)

    
    print(task_list)

    print("\nRemoving task1:")
    task_list.remove_task(task1)

    print("Remaining tasks:\n")
    print(task_list)
