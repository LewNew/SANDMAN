from datetime import datetime
from abc import ABC, abstractmethod
import logging

class Task(ABC):
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
    @staticmethod
    def ValidateClassMetadata(metadata)->bool:
        if not isinstance(metadata,dict):
            raise TypeError(f'Metadata is not dictionary, actually type:{type(metadata)}')
        
        #TODO should args be included???
        if not set(['name', 'description', 'status','args']).issubset(set(metadata.keys())):
            print("\n\n")
            print(metadata)
            print(f'Metadata strcuture missing prie keys {metadata.keys()}')
            raise Exception(f'Metadata strcuture missing prie keys {metadata.keys()}')
        
        if not isinstance(metadata['name'], str) or not isinstance(metadata['description'], str):
            raise Exception(f'Metadata name({type(metadata['name'])}) or description({type(metadata['description'])}) not a string')
        
        return True        


    @staticmethod
    @abstractmethod
    def get_class_metadata():
        '''A class method used to extract information about the task for dynamic loading
        It should retun the following type of structure with the key fields

        _metadata = {
            'name': 'ParentTaskClass',
            'description': 'The parent abstract class to be extended'
            'status':'ignore',
            'args': None
        }
        '''
        #self.logger.warning(f"not implemented")
        raise NotImplementedError(f'not implemented')
    
    @property
    def TaskList(self):
        return self.task_list

    @property
    def prompt(self):
        return self._prompt
    
    @TaskList.setter
    def TaskList(self, newList):
        #if not isinstance(newList, TaskList):
        #    raise TypeError(f"Expected a TaskList object, but received {type(newList)}")
        self._task_list = newList

    @property
    def Name(self):
        '''
            Name: returns the name the class is defined. 
                Note: If this is 'unset' then the inheritor has not overriden it properly
            returns:
                string: the name of the task.      
        '''
        return self._name
    
    @property
    def Context(self):
        return self._context
    
    @property
    def PercentComplete(self):
        return self._percent_complete

    def __init__(self, config, context)->None:
        """
        Initializes a new Task object.

        Parameters:
            context: A string passed to the task which describes what the task should and must do. 
                     Ideally this should e something that can be interpreted by an LLM
            config: A dictionary object with the rigth confg data pulled from the config file

            NOTE: if the child class needs additional parameters they can only be optional. It is up to
                  the task to make sure a lack of information is handled properly.
        """

        self._logger = logging.getLogger('logger.'+__name__)
        self._task_list = None

        self._name = 'unset'
        self._percent_complete = 0
        self._last_worked_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._inception_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._channel = None
        self._config = config

        if context == None:
            self._context = ""
        else:
            self._context = context

        self._prompt = None

    def __str__(self):
        """
        Return a string representation of the Task.

        Returns:
            str: A formatted string representing the Task.
        """
        #TODO Task does not print its parent task list otherwise printing a TaskList or task would cause an infinate recuresie look
        # might want to change this
        obj_vars = vars(self)
        task_details_str = "\n".join(f"{key}: {value}" for key, value in vars(self).items() if key != '_task_list')
        return f"{task_details_str}"

    def add_to_parent_task_list(self,task):
        if (self._task_list == None):
            self._logger.warning(f'Add to parent task list called in {self.name} but no task_list set')
            raise Exception(f'Add to parent task list called in {self._name} but no task_list set')
        self._task_list.add_task(task)

    def remove_from_parent_task_list(self,task):
        if (self._task_list == None):
            self._logger.warning(f'remove from parent task list called in {self.name} but no task_list set')
            raise Exception(f'remove from parent task list called in {self._name} but no task_list set')
        self._task_list.remove_task(task)


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
        self._percent_complete = 100
        self.set_last_worked_on()
        self._logger.info(f'{self.Name} completed')
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
        self._logger.warning(f'do_work method in {__name__} being called without being implemented in the concrete subclass')
        raise NotImplementedError("do_work method must be implemented in the concrete subclass")

    @abstractmethod
    def read_work(self,**kwargs):
        """
        abstract method for sub classes to implement to facilitate reading the work they have done or reading communication e.g. reading an email
        or reading a partialy complete word document to then continue that word document

        """
        self._logger.warning(f'read_work method in {__name__} being called without being implemented in the concrete subclass')
        raise NotImplementedError("read_work method must be implemented in the concrete subclass")