from Task import Task
from RAWChannel import RAWChannel
from TextGenerator import TextGenerator
import time
import random
from MemoryList import MemoryList, MemoryDataBlock
import os

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
            'status':'valid',
            'args':{}
        }
        return _metadata
    
    def __init__(self, config=None, context=None):
        super().__init__(config,context)
        #set the name of the task to WriteDocumentNotepadTask-{random numbers}
        self._name = ''.join(str(random.randint(0,9)) for _ in range(5))
        self._name = "WriteDocumentRawTask-"+self._name

        #set the filename to random letters
        
        #load file path from config
        
        self._file_path = config['workingdir']

        #create the TextGenerator
        self._generator = TextGenerator()

        #ceate the file name based on text generator
        self._prompt = "can you create me a file name for a document that fits this criteria make sure to shorten it down so its not too big (do not include spaces ' ' and have it end in .txt):" + self._context
        self._file_name = self._generator.generate_text(self,None,None)

        #checking LLM file name output is corredt
        if self.is_valid_filename(self._file_name):
            print("File name is valid.")
        else:
            print("Invalid file name. Please choose a different name.")
            self._logger.warning(f"_file_name: {self._file_name} generated from LLM is invalid so useing random numbers for file name instead")
            self._file_name = ''
            characters = string.ascii_letters + string.digits
            self._file_name = ''.join(secrets.choice(characters) for _ in range(16))
            self._file_name = ''.join(secrets.choice(characters) for _ in range(16))
            self._file_name = self._file_name + '.txt'

        self._channel = RAWChannel(self._file_path,self._file_name)

        self._prompt = "can you write a document that fits this criteria, you can make up as much as you want:" + self._context

        self._logger.info(f"created {self._name} with the file name: {self._file_name}")
        
        
        
        
    def do_work(self,persona=None,mood=None,memory=None):
        self._logger.info(f"{self._name} doing work")
        print("doing work")
        
        #sending the data to channel
        self._channel.send(text = self._generator.generate_text(self,persona,mood))

        #wait a few seconds just for padding
        #TODO probably want to remove this wait in future
        for _ in range(0,5):
            print('*', end='')
            time.sleep(1)

        print("finished work")


        if not memory == None:
            if not 'WriteDocumentRawTask' in memory:
                memory['WriteDocumentRawTask'] = MemoryList(2)

            new_rttmb = WriteDocumentRawTaskMemoryBlock(self._name)
            memory['WriteDocumentRawTask'].append(new_rttmb)

        self._logger.info(f"{self._name} doing work - Info Level")
        self._logger.debug(f"{self._name} doing work - Debug Level")

        #update task so that its finished
        self.finish_work()

        #TODO do work should return some usefull value
        return True

    def read_work(self,**kwargs):
        print("reading work")
        work = self._channel.read()
        print("finished reading")
        return work

    #checks to see if the file name is valid
    def is_valid_filename(self,filename):
        invalid_chars = r'\/'  # Invalid characters

        # Check length
        if len(filename) > 255:
            self._logger.warning(f"_file_name: {self._file_name} generated from LLM is invalid as it is too long so useing random numbers for file name instead")
            return False

        # Check for invalid characters
        #10AM_CreatingOutline_LitReview_AIHealthcare
        if any(char in invalid_chars for char in filename):
            self._logger.warning(f"_file_name: {self._file_name} generated from LLM is invalid as it have invalid characters so useing random numbers for file name instead")
            return False

        # Check for reserved names on Windows
        reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "LPT1"]
        if os.name == 'nt' and filename.upper() in reserved_names:
            self._logger.warning(f"_file_name: {self._file_name} generated from LLM is invalid as it uses a reserved name on Windows so useing random numbers for file name instead")
            return False

        return True



