import sys
sys.path.append('./src/')
sys.path.append('./src/channels')
import json
from Persona import Persona

from Task import Task
from NotepadChannel import NotepadChannel
from TextGenerator import TextGenerator
from NotepadChannel import NotepadChannel
import time
import random
from MemoryList import MemoryList, MemoryDataBlock
import os



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
            'status':'valid',
            'args':{}
        }
        return _metadata
    
    def __init__(self, config, context, **kwargs):

        super().__init__(config,context, **kwargs)
        #set the name of the task to WriteDocumentNotepadTask-{random numbers}
        self._name = ''.join(str(random.randint(0,9)) for _ in range(5))
        self._name = "WriteDocumentNotepadTask-"+self._name

        self.COLOR_RED = "\x1b[31m"
        self.COLOR_GREEN = "\x1b[1;32m"
        self.COLOR_RESET = "\x1b[0m"
        self.COLOR_BLUE = "\x1b[94m"
        self.COLOR_YELLOW = "\x1b[93m"

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
            # print("File name is valid.")
            pass
        else:
            print("Invalid file name. Please choose a different name.")
            self._file_name = ''
            characters = string.ascii_letters + string.digits
            self._file_name = ''.join(secrets.choice(characters) for _ in range(16))
            self._file_name = ''.join(secrets.choice(characters) for _ in range(16))
            self._file_name = self._file_name + '.txt'

        self._channel = NotepadChannel(self._file_path,self._file_name)

        self._prompt = "can you write a document that fits this criteria:" + self._context

        self._logger.info(f"INFO: created {self._name} with the file name: {self._file_name}")
        self._logger.debug(f"DEBUG: Additional debug information here.")

        # self._logger.info(f"created {self._name} with the file name: {self._file_name}")


        
        
    def do_work(self,persona=None,mood=None,memory=None):

        # self._logger.info(f"{self._name} doing work")
        self._logger.info(f"{self._name} doing work - Info Level")
        self._logger.debug(f"{self._name} doing work - Debug Level")

        print(f"Prompt:\n{self._prompt}\n")

        #print(f"persona: {persona.generate_persona_summary()}")

        print("\n\x1b[1;32mPress Enter to continue...\x1b[0m")
        input()

        print(f"[+] Working on {self.COLOR_YELLOW}{self._name}{self.COLOR_RESET}")
        
        text = self._generator.generate_text(self,persona,mood)

        #sending the data to channel
        self._channel.send(text=text)

        #wait a few seconds just for padding
        #TODO probably want to remove this wait in future
        # for _ in range(0,3):
        #     print('*', end='')
        #     time.sleep(1)

        print(f"\n[+] Finished working on {self.COLOR_YELLOW}{self._name}{self.COLOR_RESET}")


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
    

    #checks to see if the file name is valid
    def is_valid_filename(self,filename):
        invalid_chars = r'\/#%&{}<>*?$!":@+` |='  # Invalid characters
        # Check length
        if len(filename) > 255:
            self._logger.warning(f"_file_name: {self._file_name} generated from LLM is invalid as it is too long so useing random numbers for file name instead")
            return False

        # Check for invalid characters
        if any(char in invalid_chars for char in filename):
            self._logger.warning(f"_file_name: {self._file_name} generated from LLM is invalid as it have invalid characters so useing random numbers for file name instead")
            return False

        # Check for reserved names on Windows
        reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "LPT1"]
        if os.name == 'nt' and filename.upper() in reserved_names:
            self._logger.warning(f"_file_name: {self._file_name} generated from LLM is invalid as it uses a reserved name on Windows so useing random numbers for file name instead")
            return False

        return True


if __name__ == "__main__":

    config = {"workingdir":'./fakeWork/'}
    context = "Draft an outline for your upcoming conference paper on AI. Begin by summarizing the research objectives, methodology, and anticipated outcomes. Provide a compelling introduction to captivate the scientific community."

    persona_file = './src/agent_attributes_config.json'

    with open(persona_file, 'r') as file:
        persona_config = json.load(file)

    persona = Persona(persona_config["first_name"],persona_config["last_name"],persona_config["personality_description"],persona_config["job_role"],persona_config["organisation"],persona_config["gender"],persona_config["age"],persona_config["traits"])

    notepadTaskTest = WriteDocumentNotepadTask(config,context)

    print("\n")



    # print(f"persona: {persona.generate_persona_summary()}\n")

    print("Decision engine decided on:\n")

    print(f"Name: {notepadTaskTest.Name}\n")
    print(f"Context:\n{notepadTaskTest.Context}\n")

    notepadTaskTest.do_work(persona)
