from Task import Task
from NotepadChannel import NotepadChannel
from TextGenerator import TextGenerator

class NotepadTask(Task):
    
    def __init__(self, name, task_type,file_path,file_name, percent_complete=0, last_worked_on=None, inception_time=None):
        super().__init__(name, task_type, percent_complete, last_worked_on, inception_time)
        
        #TODO dont know if this key is right??? just fond it and used it from TextGenerator.py class
        self.generator = TextGenerator("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")

        #TODO the file_path should proably be hard coded but the file name can be created from the generator class
        self.file_path = file_path
        self.file_name = file_name
        
        self.channel = NotepadChannel(self.file_path,self.file_name)
        
        
    def do_work(self,task=None,persona=None,mood=None,Memory=None):
        print("doing work")
        #TODO  is currenetly hard coded, persoan and mood should be from what is passed into the do_work function
        self.channel.send(text = self.generator.generate_text(task,persona,mood))
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
    print(word_task_instance.do_work(word_task_instance,"persona"))


