from Task import Task
from NotepadChannel import NotepadChannel
from TextGenerator import TextGenerator
from RAWChannel import RAWChannel
from NotepadTask import NotepadTask

class PlanTaskTask(Task):
    """
    a task to add more tasks, currently very basic and must be changed
    """
    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'PlanTaskTask',
            'description': 'This is a bootstrapping task for sandman status',
            'status':'valid'
        }
        return _metadata
    
    def __init__(self, name, task_type, percent_complete=0, last_worked_on=None, inception_time=None,task_list=None):


        #TODO dont know why i need to do "a ="" but if i pass task_list as is its just None
        a = task_list
        super().__init__(name, task_type, percent_complete, last_worked_on, inception_time, task_list=a)
        
        
        
    def do_work(self,persona=None,mood=None,memory=None):
        print("doing work")

        #TODO very hard coded must be changed
        for key, value in self.task_list.task_classes.items():
            print(key)
            if key == 'NotepadTask':
                task_class = value['module_class']
                task_obj = task_class('Q2Report',key,"./fakeWork", "fakework1.txt", task_list=self.task_list)
                self.add_to_parent_task_list(task_obj)
                self.add_to_parent_task_list(value['module_class']('scriptforpresentation',key,"./fakeWork", "fakework2.txt", task_list=self.task_list))
        #task.add_to_parent_task_list(NotepadTask("q2Report","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework1.txt",task_list=self.task_list))
        #task.add_to_parent_task_list(NotepadTask("scriptForPresentation","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework2.txt",task_list=self.task_list))

        print("finished work")
        
        return True

    def read_work(self,**kwargs):
        
        return None


if __name__ == "__main__":
    
    pass


