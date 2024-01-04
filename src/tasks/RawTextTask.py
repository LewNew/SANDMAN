from Task import Task
from RAWChannel import RAWChannel
from TextGenerator import TextGenerator
import time
import random
from MemoryList import MemoryList, MemoryDataBlock

import secrets
import string

class RawTextTaskMemoryBlock(MemoryDataBlock):
    
    def __init__(self, data):
        super().__init__()
        self._data = data
    
    def __str__(self):
        return f'Created:{self._created}, data: {self._data}'

class RawTextTask(Task):

    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'RawTextTask',
            'description': 'types text into a file (no GUI)',
            'status':'valid'
        }
        return _metadata
    
    def __init__(self, config=None, context=None):
        super().__init__(config,context)
        #set the name pf the task to RawTextTasl-{random numbers}
        self.name = ''.join(str(random.randint(0,9)) for _ in range(5))
        self.name = "RawTextTask-"+self.name
        #set the filename to random letters
        characters = string.ascii_letters + string.digits
        self.file_name = ''.join(secrets.choice(characters) for _ in range(16))
        self.file_name = self.file_name + '.txt'
        #load file path from config
        self.file_path = config['workingdir']

        #create the RawChannel and TextGenerator
        self.logger.info(f"created {self.name}")
        self.channel = RAWChannel(self.file_path,self.file_name)
        self.generator = TextGenerator("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")

        
        
        
    def do_work(self,persona=None,mood=None,memory=None):
        self.logger.info(f"{self.name} doing work")
        print("doing work")
        
        #sending the data to channel
        self.channel.send(text = self.generator.generate_text(self,persona,mood))

        #wait a few seconds just for padding
        #TODO probably want to remove this wait in future
        for _ in range(0,3):
            print('*', end='')
            time.sleep(1)

        print("finished work")


        if not memory == None:
            if not 'RawTextTask' in memory:
                memory['RawTextTask'] = MemoryList(2)

            new_rttmb = RawTextTaskMemoryBlock(self.name)
            memory['RawTextTask'].append(new_rttmb)



        #update task so that its finished
        self.finish_work()

        #TODO do work should return some usefull value
        return True

    def read_work(self,**kwargs):
        print("reading work")
        work = self.channel.read()
        print("finished reading")
        return work