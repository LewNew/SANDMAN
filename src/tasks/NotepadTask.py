from Task import Task
from NotepadChannel import NotepadChannel
from TextGenerator import TextGenerator
from RAWChannel import RAWChannel

import secrets
import string


class NotepadTask(Task):

    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'NotepadTask',
            'description': 'Interacts with a simple txt file document',
            'status':'valid'
        }
        return _metadata
    
    def __init__(self, config, context):


        #TODO dont know why i need to do "a ="" but if i pass task_list as is its just None
        super().__init__(config,context)
        self.name = 'NotepadTask'
        
        #TODO dont know if this key is right??? just fond it and used it from TextGenerator.py class
        self.generator = TextGenerator("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")

        #TODO the file_path should proably be hard coded but the file name can be created from the generator class
        self.file_path = config['workingdir']
        characters = string.ascii_letters + string.digits

        self.file_name = ''.join(secrets.choice(characters) for _ in range(16))
        self.file_name = self.file_name + '.txt'
        print(self.file_name)
        
        self.channel = NotepadChannel(self.file_path,self.file_name)
        
        
    def do_work(self,persona=None,mood=None,memory=None):
        print("doing work")
        #TODO  is currenetly hard coded, persoan and mood should be from what is passed into the do_work function
        self.channel.send(text = self.generator.generate_text(self,persona,mood))
        print("finished work")

        #update task so that its finished
        self.finish_work()

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


