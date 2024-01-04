from abc import ABC, abstractmethod
from Memory import Memory
from Mood import Mood
from Persona import Persona
import logging

class DecisionEngine(ABC):
    
    @property
    def Memory(self):
        return self._memory
    
    @Memory.setter
    def Memory(self, newMemory):
        if not isinstance(newMemory, Memory):
            self.logger.warning(f"Expected a Memory object, but received {type(newMemory)}")
            raise TypeError(f"Expected a Memory object, but received {type(newMemory)}")
        
    @property
    def Persona(self):
        return self._persona
    
    @Persona.setter
    def Persona(self, newPersona):
        if not isinstance(newPersona, Persona):
            self.logger.warning(f"Expected a Persona object, but received {type(newPersona)}")
            raise TypeError(f"Expected a Persona object, but received {type(newPersona)}")
        
    @property
    def Mood(self):
        return self._mood
    
    @Mood.setter
    def Mood(self, newMood):
        if not isinstance(newMood, Mood):
            self.logger.warning(f"Expected a Mood object, but received {type(newMood)}")
            raise TypeError(f"Expected a Mood object, but received {type(newMood)}")
        
    @property
    def EgoAndId(self):
        return [self._persona, self._memory, self._mood]

    def __init__ (self, task_list):
        self.logger = logging.getLogger('logger.'+__name__)
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
    