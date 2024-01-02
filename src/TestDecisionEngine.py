from abc import ABC, abstractmethod

class DecisionEngine(ABC):
    
    def __init__ (self, task_list):
        self._task_list = task_list

    @property
    def task_list(self):
        return self._task_list
    
    @abstractmethod
    def make_decision(self):
        pass
    