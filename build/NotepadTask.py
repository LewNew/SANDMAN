from Task import Task
from NotepadChannel import NotepadChannel

class NotepadTask(Task):
    
    def __init__(self, name, task_type,file_path,file_name, percent_complete=0, last_worked_on=None, inception_time=None):
        super().__init__(name, task_type, percent_complete, last_worked_on, inception_time)
        self.file_path = file_path
        self.file_name = file_name
        self.channel = NotepadChannel(self.file_path,self.file_name)
        #TODO have the generate text class here
        
    #TODO text  should be generated here, this function should take a personality and pass that to a generate class that
    #TODO !!!!!!!!!
    def do_work(self,**kwargs):
        print("doing work")
        self.channel.send(text = kwargs["text"])
        print("finished work")

        #TODO do work should return some usefull value
        return True



    def read_work(self,**kwargs):
        print("reading work")
        work = self.channel.read()
        print("finished reading")
        return work




if __name__ == "__main__":
    
    word_task_instance = NotepadTask(name="Example Task", task_type="Word",percent_complete=50,file_path = "H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork", file_name = "fakework.txt")
    print(word_task_instance.do_work())


