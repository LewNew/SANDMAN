import time
import logging
import datetime

class MemoryDataBlock():
    '''
        class MemoryDataBlock: Stores a chunk of memory 
        Each rememberer must extend this class to manage the specific information it needs to remember.
    '''
    @property
    def created(self):
        return self._created
    
    @property
    def data(self):
        return self._data
    
    def __init__(self) -> None:
        self._created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._data = None


class MemoryList():
    '''
        class MemoryList: Represents a list of data blocks with some additional
        management functions for data blocks.
        Only types of MemoryDataBlock are accepted into the list

        The class can be extended if the rememberer needs additional features.
    '''
    @property
    def max_size(self):
        return self._db_max_size
    def __init__(self, max_size=10):
        self.logger = logging.getLogger('logger.'+__name__)
        self._datablocks = []
        self._db_max_size = max_size

    def __getitem__(self, index):
        return self._datablocks[index]

    def __setitem__(self, index, value):
        if not isinstance(value,MemoryDataBlock):
            raise Exception(f'trying to set item at {index} {type(value) in MemoryList}')
        self._datablocks[index] = value

    def __len__(self):
        return len(self._datablocks)

    def __iter__(self):
        return iter(self._datablocks)
    
    def append(self, value):
        if not isinstance(value,MemoryDataBlock):
            raise Exception(f'trying to append {type(value) in MemoryList}')
        if len(self._datablocks) == self._db_max_size:
            lim = 1 - self._db_max_size
            self._datablocks = self._datablocks[lim:]
        self._datablocks.append(value)
    
    def __str__(self):
        ml_str = f'+ BD Max Size:{self._db_max_size}\n+ Memory count:{len(self._datablocks)}\n'
        for mb in self._datablocks:
            ml_str += f'+ {str(mb)}\n'
        return ml_str
    
    def force_forget_by_count(self, count):
        self._datablocks = self._datablocks[-count:]
    
    
