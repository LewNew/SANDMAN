from Task import Task

class NotepadTask(Task):
    
    def __init__(self, name, task_type, percent_complete=0, last_worked_on=None, inception_time=None,channel=None):
        super().__init__(name, task_type, percent_complete, last_worked_on, inception_time, channel)

        
    def do_work(self,**kwargs):
        print("doing work")

    def read_work(self,**kwargs):
        print("reading work")




if __name__ == "__main__":
    
    word_task_instance = NotepadTask(name="Example Task", task_type="Word",percent_complete=50)
    print(word_task_instance.do_work())


