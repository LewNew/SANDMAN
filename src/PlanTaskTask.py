from Task import Task
from NotepadChannel import NotepadChannel
from TextGenerator import TextGenerator
from RAWChannel import RAWChannel
from tasks.NotepadTask import NotepadTask

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
    
    @property
    def Name(self):
        return self.name
    
    #def __init__(self, name, task_type, percent_complete=0, last_worked_on=None, inception_time=None,task_list=None):
    def __init__(self):

        #TODO dont know why i need to do "a ="" but if i pass task_list as is its just None
        super().__init__()
        self.name = 'PlanTaskTask'
        self.logger.info(f"created {self.name}")
        
    def do_work(self,persona=None,mood=None,memory=None):
        print("doing work")
        if self.task_list == None:
            raise Exception(f'Parent TaskList not specified in {self.name}')

        #TODO very hard coded must be changed
        for key, value in self.task_list.task_classes.items():
            print(key)
            if key == 'NothingTask':
                task_class = value['module_class']
                task_config = None
                if 'Config' in value:
                    task_config = value['Config']
                print(task_config)
                task_obj = task_class(task_config)
                self.add_to_parent_task_list(task_obj)
                self.add_to_parent_task_list(task_class(task_config))
                #self.add_to_parent_task_list(value['module_class']('scriptforpresentation',key,"./fakeWork", "fakework2.txt", task_list=self.task_list))
        #task.add_to_parent_task_list(NotepadTask("q2Report","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework1.txt",task_list=self.task_list))
        #task.add_to_parent_task_list(NotepadTask("scriptForPresentation","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework2.txt",task_list=self.task_list))

        print("finished work")
        
        return True

    def read_work(self,**kwargs):
        
        return None


if __name__ == "__main__":
    
    pass


