from MemoryList import MemoryList
import logging

class Memory():
    '''
        class Memory: A class which represents the memory of Sandman. 
        
        This class is essentially a dictionay with additional management functions.
        The Keys are names which correspond to the owners of the memory items
        The items are then Memorylist objects which are used to hold MemoryDataBlock objects
        MemoryDataBlock objects can be extended to hold the data the owner needs to remember
    '''
    def __init__(self):
        self.logger = logging.getLogger('logger.'+__name__)
        self._memory_collection = {}
    
    def __getitem__(self, key):
        return self._memory_collection[key]

    def __setitem__(self, key, value):
        if not isinstance(value, MemoryList):
            raise Exception(f'Cannot add item to memory as not MemoryList. Actual class {type(value)}')
        self._memory_collection[key] = value

    def __delitem__(self, key):
        del self._memory_collection[key]

    def __len__(self):
        return len(self._memory_collection)

    def __iter__(self):
        return iter(self._memory_collection)

    def __contains__(self, key):
        return key in self._memory_collection
    
    def __str__(self):
        """
        Return a string representation of the Memory.

        Returns:
            str: A formatted string representing all tasks in the Memory.
        """
        mem_str = ''
        for key, mem in self._memory_collection.items():
            mem_str = mem_str + key+ ':\n' + str(mem) + '----------\n'
            
        return f"All Memories:\n===========\n{mem_str}=========="
    
    def force_forget_by_count(self, count) -> None:
        '''
            force_forget_by_count: Used to forget all of the MemoryDataBlocks beyond count

            args:
                count: integer which tells it how many blocks to forget
            
            returns: None            
        '''
        for key, ml in self._memory_collection.items():
            ml.force_forget_by_count(count)
