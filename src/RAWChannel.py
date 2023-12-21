from abc import ABC, abstractmethod
import subprocess
import pyautogui
import time
from Channel import Channel
import os


class RAWChannel(Channel):
    """
    Abstract Base Class for reading RAW files

    Attributes:
    - None

    Methods:
    - __init__: Constructor for the Channel class.
    - send: Abstract method to send data through the channel.
    - recv: Abstract method to receive data through the channel.
    - read: Abstract method to read data through the channel.
    """

    def __init__(self, file_path, file_name):
        """
        Constructor for the RAWChannel class.

        Parameters:
        - file_path (str): The path to the directory where file is stored.
        - file_name (str): The name of the file to be manipulated.

        Returns:
        - None
        """
        super().__init__()
        self.file_path = file_path
        self.file_name = file_name

    @abstractmethod
    def send(self, **kwargs):
        """
        Abstract method to send data through the channel.

        Parameters:
        - kwargs (dict): Keyword arguments representing data to be sent.

        Returns:
        - None
        """
        pass

    @abstractmethod
    def recv(self, **kwargs):
        """
        Abstract method to receive data through the channel.

        Parameters:
        - kwargs (dict): Keyword arguments representing parameters for receiving data.

        Returns:
        - None
        """
        pass

    @abstractmethod
    def read(self, **kwargs):
        """
        Abstract method to read data through the channel.

        Parameters:
        - kwargs (dict): Keyword arguments representing parameters for reading data.

        Returns:
        - None
        """
        pass

