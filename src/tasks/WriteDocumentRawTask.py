from Task import Task
from RAWChannel import RAWChannel
from TextGenerator import TextGenerator
import time
import random
from MemoryList import MemoryList, MemoryDataBlock

import secrets
import string

class WriteDocumentRawTaskMemoryBlock(MemoryDataBlock):
    
    def __init__(self, data):
        super().__init__()
        self._data = data
    
    def __str__(self):
        return f'Created:{self._created}, data: {self._data}'

class WriteDocumentRawTask(Task):

    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'WriteDocumentRawTask',
            'description': 'types text into a file (no GUI)',
            'status':'valid'
        }
        return _metadata
    
    def __init__(self, config=None, context=None):
        super().__init__(config,context)
        #set the name pf the task to WriteDocumentRawTask-{random numbers}
        self._name = ''.join(str(random.randint(0,9)) for _ in range(5))
        self._name = "WriteDocumentRawTask-"+self._name
        #set the filename to random letters
        characters = string.ascii_letters + string.digits
        self._file_name = ''.join(secrets.choice(characters) for _ in range(16))
        self._file_name = self._file_name + '.txt'
        #load file path from config
        self._file_path = config['workingdir']

        #create the RawChannel and TextGenerator
        self._logger.info(f"created {self._name}")
        self._channel = RAWChannel(self._file_path,self._file_name)
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
            if not 'WriteDocumentRawTask' in memory:
                memory['WriteDocumentRawTask'] = MemoryList(2)

            new_rttmb = WriteDocumentRawTaskMemoryBlock(self._name)
            memory['WriteDocumentRawTask'].append(new_rttmb)



        #update task so that its finished
        self.finish_work()

        #TODO do work should return some usefull value
        return True

    def read_work(self,**kwargs):
        print("reading work")
        work = self._channel.read()
        print("finished reading")
        return work