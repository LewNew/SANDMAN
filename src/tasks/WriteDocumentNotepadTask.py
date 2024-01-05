from Task import Task
from NotepadChannel import NotepadChannel
from TextGenerator import TextGenerator
from NotepadChannel import NotepadChannel
import time
import random
from MemoryList import MemoryList, MemoryDataBlock


import secrets
import string

class WriteDocumentNotepadTaskMemoryBlock(MemoryDataBlock):
    
    def __init__(self, data):
        super().__init__()
        self._data = data
    
    def __str__(self):
        return f'Created:{self._created}, data: {self._data}'

class WriteDocumentNotepadTask(Task):

    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'WriteDocumentNotepadTask',
            'description': 'Interacts with a simple txt file document useing notepad',
            'status':'valid'
        }
        return _metadata
    
    def __init__(self, config, context):

        super().__init__(config,context)
        #set the name of the task to WriteDocumentNotepadTask-{random numbers}
        self._name = ''.join(str(random.randint(0,9)) for _ in range(5))
        self._name = "WriteDocumentNotepadTask-"+self._name
        #set the filename to random letters
        characters = string.ascii_letters + string.digits
        self._file_name = ''.join(secrets.choice(characters) for _ in range(16))
        self._file_name = self._file_name + '.txt'
        #load file path from config
        self._file_path = config['workingdir']

        #create the NotepadChannel and TextGenerator
        self._logger.info(f"created {self._name}")
        self._channel = NotepadChannel(self._file_path,self._file_name)
        self._generator = TextGenerator("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")
        
        
    def do_work(self,persona=None,mood=None,memory=None):
        self._logger.info(f"{self._name} doing work")
        print("doing work")
        
        #sending the data to channel
        self._channel.send(text = self._generator.generate_text(self,persona,mood))

        #wait a few seconds just for padding
        #TODO probably want to remove this wait in future
        for _ in range(0,3):
            print('*', end='')
            time.sleep(1)

        print("finished work")


        if not memory == None:
            if not 'WriteDocumentNotepadTask' in memory:
                memory['WriteDocumentNotepadTask'] = MemoryList(2)

            new_ntmb = WriteDocumentNotepadTaskMemoryBlock(self._name)
            memory['WriteDocumentNotepadTask'].append(new_ntmb)

        #update task so that its finished
        self.finish_work()

        #TODO do work should return some usefull value
        return True



    def read_work(self,**kwargs):
        print("reading work")
        work = self._channel.read()
        print("finished reading")
        return work


if __name__ == "__main__":
    
    word_task_instance = WriteDocumentNotepadTask(name="Example Task", task_type="Word",percent_complete=50,file_path = "H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork", file_name = "fakework.txt")
    print(word_task_instance.do_work(word_task_instance,"persona"))


