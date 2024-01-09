from abc import ABC, abstractmethod
import subprocess
import pyautogui
import time
from Channel import Channel
import os


class NotepadChannel(Channel):
    """
    NotepadChannel Class

    This class represents a communication channel with Notepad, inheriting from the Channel class.

    Attributes:
    - file_path (str): The path to the directory where files are stored.
    - file_name (str): The name of the file to be manipulated.

    Methods:
    - __init__: Constructor for the NotepadChannel class.
    - send: Implementation of the send method for sending text to Notepad.
    - recv: Implementation of the recv method for receiving data (not implemented).
    - read: Implementation of the read method for reading text from a Notepad file.
    - save_new_file: Save a new Notepad file.
    - check_file_exists: Check if a Notepad file exists.
    - new_file: Create and save a new Notepad file.
    - continue_file: Continue an existing Notepad file.

    """

    def __init__(self, file_path, file_name):
        """
        Constructor for the NotepadChannel class.

        Parameters:
        - file_path (str): The path to the directory where file is stored.
        - file_name (str): The name of the file to be manipulated.

        Returns:
        - None
        """
        super().__init__()
        self.file_path = file_path
        self.file_name = file_name
        self.full_path = os.path.abspath(self.file_path)

    def send(self, **kwargs):
        """
        Implementation of the send method for sending text to Notepad.

        Parameters:
        - kwargs (dict): Keyword arguments representing data to be sent.
            - text (str): The text to be sent to Notepad.

        Returns:
        - bool: True if the operation is successful.
        """
        text = kwargs["text"]

        # Open Notepad using subprocess
        if not self.check_file_exists():
            self.new_file(text)
        else:
            self.continue_file(text)

        return True

    def recv(self):
        """
        Implementation of the recv method for receiving data (not implemented).

        Parameters:
        - None

        Returns:
        - None
        """
        pass

    def read(self):
        """
        Implementation of the read method for reading text from a Notepad file.

        Parameters:
        - None

        Returns:
        - str or None: The content of the Notepad file, or None if an error occurs.
        """
        # Check if the file exists
        if self.check_file_exists():
            content = ""

            # Read the file
            try:
                with open(self.full_path + "\\" + self.file_name, 'r') as file:
                    content = file.read()
            except FileNotFoundError:
                print(f"Error: The file '{self.full_path + "\\" + self.file_name}' does not exist.")
                return None
            except Exception as e:
                print(f"Error: An unexpected error occurred - {e}")
                return None

            # Simulate reading it
            subprocess.Popen(['notepad.exe', self.full_path + "\\" + self.file_name])
            time.sleep(5)  # Spend 5 seconds reading it
            pyautogui.hotkey('alt', 'f4')

            # Then return the content
            return content
        else:
            # File does not exist
            # TODO: Handle the case where trying to read a file that does not exist
            pass

    def save_new_file(self):
        """
        Save a new Notepad file.

        Parameters:
        - None

        Returns:
        - None
        """
        pyautogui.hotkey('ctrl', 's')
        time.sleep(2)
        #uses full path
        pyautogui.typewrite(self.full_path + "\\" + self.file_name,interval=0.02)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)

    def check_file_exists(self):
        """
        Check if a Notepad file exists.

        Parameters:
        - None

        Returns:
        - bool: True if the file exists, False otherwise.
        """
        return os.path.exists(self.full_path +"\\"+ self.file_name)

    def new_file(self, text):
        """
        Create and save a new Notepad file.

        Parameters:
        - text (str): The text to be written to the new file.

        Returns:
        - None
        """
        subprocess.Popen(['notepad.exe'])
        time.sleep(2)
        pyautogui.typewrite(text, interval=0.02)
        time.sleep(2)
        self.save_new_file()
        pyautogui.hotkey('alt', 'f4')
        pass

    def continue_file(self, text):
        """
        Continue an existing Notepad file.

        Parameters:
        - text (str): The text to be appended to the existing file.

        Returns:
        - None
        """
        subprocess.Popen(['notepad.exe', self.full_path + "\\" + self.file_name])
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'end')
        pyautogui.typewrite(text, interval=0.02)
        time.sleep(2)
        pyautogui.hotkey('ctrl', 's')
        pyautogui.hotkey('alt', 'f4')
        pass




# Example usage:
if __name__ == "__main__":
    notepad_channel = NotepadChannel("H:\\PhD\\sandman\\project\\SANDMAN\\","fakework.txt")
    notepad_channel.send(text="hello!")
    time.sleep(2)
    print(notepad_channel.read())




