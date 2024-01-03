from abc import ABC, abstractmethod
from Memory import Memory
from Mood import Mood
from Persona import Persona

class DecisionEngine(ABC):
    
    @property
    def Memory(self):
        return self._memory
    
    @Memory.setter
    def Memory(self, newMemory):
        if not isinstance(newMemory, Memory):
            raise TypeError(f"Expected a Memory object, but received {type(newMemory)}")
        
    @property
    def Persona(self):
        return self._persona
    
    @Persona.setter
    def Persona(self, newPersona):
        if not isinstance(newPersona, Persona):
            raise TypeError(f"Expected a Persona object, but received {type(newPersona)}")
        
    @property
    def Mood(self):
        return self._mood
    
    @Mood.setter
    def Mood(self, newMood):
        if not isinstance(newMood, Mood):
            raise TypeError(f"Expected a Mood object, but received {type(newMood)}")
        
    @property
    def EgoAndId(self):
        return [self._persona, self._memory, self._mood]

    def __init__ (self, task_list):
        self._task_list = task_list
        self._memory = None
        self._persona = None
        self._mood = None

    @property
    def task_list(self):
        return self._task_list
    
    @abstractmethod
    def make_decision(self):
        pass

    @abstractmethod
    def execute_task(self):
        pass

    @abstractmethod
    def run(self):
        pass
    