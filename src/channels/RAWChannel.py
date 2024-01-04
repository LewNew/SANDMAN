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
        self.logger.debug(f"created {self}")



    def send(self, **kwargs):
        """
        Abstract method to send data through the channel.

        Parameters:
        - kwargs (dict): Keyword arguments representing data to be sent.

        Returns:
        - None
        """
        self.logger.info(f"{self} sending data")

        text = kwargs["text"]

        try:
            with open(self.file_path + self.file_name, 'w') as file:
                file.write(text)
            self.logger.info(f"Content successfully written to '{self.file_path + self.file_name}'.")
            print(f"Content successfully written to '{self.file_path + self.file_name}'.")
        except Exception as e:
            self.logger.warning(f"Error writing to file '{self.file_path + self.file_name}': {e}")
            print(f"Error writing to file '{self.file_path + self.file_name}': {e}")

        



    def recv(self, **kwargs):
        """
        Abstract method to receive data through the channel.

        Parameters:
        - kwargs (dict): Keyword arguments representing parameters for receiving data.

        Returns:
        - None
        """
        pass


    def read(self, **kwargs):
        """
        Abstract method to read data through the channel.

        Parameters:
        - kwargs (dict): Keyword arguments representing parameters for reading data.

        Returns:
        - None
        """
        self.logger.info(f"{self} reading data")

        try:
            with open(self.file_path + self.file_name, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"Error: File '{self.file_path + self.file_name}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file '{self.file_path + self.file_name}': {e}")
            return None


