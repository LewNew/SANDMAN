from MemoryList import MemoryList

class Memory():
    def __init__(self):
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
            mem_str = mem_str + key+ ':\n' + str(mem) + '----------'
            
        return f"All Memories:\n===========\n{mem_str}\n=========="
    
    def force_forget_by_count(self, count):
        for key, ml in self._memory_collection.items():
            ml.force_forget_by_count(count)
