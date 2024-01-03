from Task import Task
from NothingChannel import NothingChannel
import time
import random

class NothingTask(Task):

    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'NothingTask1',
            'description': 'A simple task which just idles for between 5 and 10 seconds randomly',
            'status':'valid'
        }
        return _metadata
    
    def __init__(self, config):

        super().__init__(config)
        self.name = ''.join(str(random.randint(0,9)) for _ in range(5))
        self.name = "NothingTask-"+self.name
        self.channel = NothingChannel()
        self.logger.info(f"created {self.name}")
        
    def do_work(self,persona=None,mood=None,memory=None):
        self.logger.info(f"{self.name} doing work")
        print("doing work")
        #TODO wait_time is currently hard coded, this might want to be changed by generating  number some how, could be random or could be from LLM or persona or something.
        #or from the task name or something.

        wait_time = random.randint(5,10)
        for _ in range(0, random.randint(5,10)):
            print('*', end='')
            time.sleep(1)
        print("\nfinished work")

        #TODO maybe dont do self.finish_work() as a do nothing isnt something you can complete, its just do nothing, still probably need to update the last_worked_on var tho
        #update task so that its finished
        self.finish_work()

        return True

    def read_work(self,**kwargs):
        return None


