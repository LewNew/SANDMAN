from Task import Task
from NothingChannel import NothingChannel
import time
import random
from MemoryList import MemoryList, MemoryDataBlock

class LunchTaskMemoryBlock(MemoryDataBlock):
    
    def __init__(self, data):
        super().__init__()
        self._data = data
    
    def __str__(self):
        return f'Created:{self._created}, data: {self._data}'

##########################################################################################################
##TODO THIS IS A PLACE HOLDER WORK IN PROGRES THASK THAT IS IDENTICAL TO NothingTask.py IN FUNCTIONALITY##
##########################################################################################################

class LunchTask(Task):

    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'LunchTask',
            'description': 'A simple task which just idles for between a defined min and max values randomly in seconds',
            'status':'valid',
            'args' :{
                'lower_time': 'is the minimum amount of time to spend on the task',
                'upper_time': 'is the maximum amount of time to spend on the task'
            }
        }
        return _metadata
    
    def __init__(self, config, context, lower_time=5, upper_time=10):

        super().__init__(config, context)
        self._name = ''.join(str(random.randint(0,9)) for _ in range(5))
        self._name = "LunchTask-"+self._name
        self._channel = NothingChannel()
        self._lower_time = lower_time
        self._upper_time = upper_time
        self._logger.info(f"created {self._name}")
        
    def do_work(self,persona=None,mood=None,memory=None):
        self._logger.info(f"{self.Name} doing work")
        print("doing work")
        #TODO wait_time is currently hard coded, this might want to be changed by generating  number some how, could be random or could be from LLM or persona or something.
        #or from the task name or something.

        for _ in range(0, random.randint(self._lower_time,self._upper_time)):
            print('*', end='')
            time.sleep(1)
        print("\nfinished work")

        if not memory == None:
            if not 'LunchTask' in memory:
                memory['LunchTask'] = MemoryList(2)

            new_ntmb = LunchTaskMemoryBlock(self._name)
            memory['LunchTask'].append(new_ntmb)

        #TODO maybe dont do self.finish_work() as a do nothing isnt something you can complete, its just do nothing, still probably need to update the last_worked_on var tho
        #update task so that its finished
        self.finish_work()

        return True

    def read_work(self,**kwargs):
        return None


