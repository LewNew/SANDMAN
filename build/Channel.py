from abc import ABC, abstractmethod

class Channel:

    def __init__(self):
        pass

    @abstractmethod
    def send(self,**kwargs):
        pass

    @abstractmethod
    def recv(self,**kwargs):
        pass

    @abstractmethod
    def read(self,**kwargs):
        pass


if __name__ == "__main__":

    new_channel = Channel()

    pass