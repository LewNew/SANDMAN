from MemoryClass import MemoryClass

class Memmory():
    def __init__(self):
        self._memoryCollection = {}

    def addMemoryObject(self, name, mc):
        self._memoryCollection[name] = mc