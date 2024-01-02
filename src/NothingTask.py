from Task import Task
from RAWChannel import RAWChannel
import time

class NothingTask(Task):
    
    def __init__(self, name, task_type, percent_complete=0, last_worked_on=None, inception_time=None,task_list=None):

        #TODO dont know why i need to do "a ="" but if i pass task_list as is its just None
        a = task_list
        super().__init__(name, task_type, percent_complete, last_worked_on, inception_time, task_list=a)        
        
    def do_work(self,persona=None,mood=None,memory=None):
        print("doing work")
        #TODO wait_time is currently hard coded, this might want to be changed by generating  number some how, could be random or could be from LLM or persona or something.
        #or from the task name or something.
        wait_time = 5
        time.sleep(wait_time)

        print("finished work")

        #TODO maybe dont do self.finish_work() as a do nothing isnt something you can complete, its just do nothing, still probably need to update the last_worked_on var tho
        #update task so that its finished
        self.finish_work()

        return True

    def read_work(self,**kwargs):
        return None


if __name__ == "__main__":
    
    nothing_task_instance = NothingTask(name="Nothing Task", task_type="Nothing",percent_complete=0)
    print(nothing_task_instance.do_work(persona=None,mood=None,memory=None))
    print(nothing_task_instance)


