#these 3 comments are for if you want to test without running main
# import sys
# sys.path.append('./src/')
# sys.path.append('./src/channels')

from Task import Task
from WebChannel import WebChannel
from TextGenerator import TextGenerator

import time
import random
from MemoryList import MemoryList, MemoryDataBlock

class WebTaskMemoryBlock(MemoryDataBlock):
    
    def __init__(self, data):
        super().__init__()
        self._data = data
    
    def __str__(self):
        return f'Created:{self._created}, data: {self._data}'

class WebTask(Task):

    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'WebTask',
            'description': 'simple task to browse the web',
            'status':'valid',
            'args':{}
        }
        return _metadata

    def __init__(self,config,context,**kwargs):
        super().__init__(config,context,**kwargs)

        self._name = ''.join(str(random.randint(0,9)) for _ in range(5))
        self._name = 'WebTask-' + self._name
        self.COLOR_RED = "\x1b[31m"
        self.COLOR_GREEN = "\x1b[1;32m"
        self.COLOR_RESET = "\x1b[0m"
        self.COLOR_BLUE = "\x1b[94m"
        self.COLOR_YELLOW = "\x1b[93m"
        # self.url = config['url']

        # Initialize a WebChannel or similar class for managing web interactions
        # self.channel = WebChannel(self.url)
        self._channel = WebChannel()

    def do_work(self,persona=None,mood=None,memory=None):
        print(f"[+] Working on {self.COLOR_YELLOW}{self._name}{self.COLOR_RESET}")

        self._channel.send()

        for _ in range(0, 5):
            print('*', end='')
            time.sleep(1)
            
        print(f"\n[+] Finished working on {self.COLOR_YELLOW}{self._name}{self.COLOR_RESET}")

        if not memory == None:
            if not 'WebTask' in memory:
                memory['WebTask'] = MemoryList(2)

            new_ntmb = WebTaskMemoryBlock(self._name)
            memory['WebTask'].append(new_ntmb)

        self.finish_work()

    def read_work(self,**kwargs):
        print("reading work")

    # def browse(self):
    #     print("Starting to browse:", self.url)
    #     # Simulate browsing activity, for example, by retrieving and displaying web content
    #     browsing_result = self.channel.retrieve(self.url)
    #     print("Finished browsing")
    #     return browsing_result

    # def read_browsing_history(self):
    #     print("Reading browsing history")
    #     history = self.channel.read_history()
    #     print("Finished reading history")
    #     return history

if __name__ == "__main__":

    web_task_instance = WebTask(None,None)
    web_task_instance.do_work()

    print(web_task_instance.browse())
