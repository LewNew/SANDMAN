from abc import ABC, abstractmethod
import subprocess
import pyautogui
import time
from Channel import Channel
import os

filePath = "H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\fakework.txt"

class NotepadChannel(Channel):
    def __init__(self):
        super().__init__()

    def send(self, text):
        # Open Notepad using subprocess
        if not self.check_file_exists(filePath):
            self.new_file(text,filePath)
        else:
            self.continue_file(text,filePath)

        return True
        

    def recv(self):
        # This method could be used to receive data from Notepad, if applicable
        pass

    def read(self):
        # This method could be used to read data from Notepad, if applicable
        pass


    def save_new_file(self, file_path):
        # Press Ctrl + S to trigger the Save dialog
        pyautogui.hotkey('ctrl', 's')
        # Wait for the Save As dialog to appear
        time.sleep(2)
        # Type the file path and press Enter
        pyautogui.typewrite(file_path)
        # Wait for the file path to be registered
        time.sleep(2)
        pyautogui.press('enter')
        # Wait for the Save dialog to close
        time.sleep(2)

    def check_file_exists(self,file_path):
        return os.path.exists(file_path)

    def new_file(self,text,file_path):

        subprocess.Popen(['notepad.exe'])
        # Wait for Notepad to open
        time.sleep(2)
        # Type and send the text to Notepad
        pyautogui.typewrite(text,interval=0.2)
        # wait to save
        time.sleep(2)
        #save the file
        self.save_new_file(filePath)
        #close the program
        pyautogui.hotkey('alt', 'f4')
        pass

    def continue_file(self,text,file_path):

        #if file already exsists continue it
        subprocess.Popen(['notepad.exe',filePath])
        #open and wait 2 seconds
        time.sleep(2)
        #move curser to EofF
        pyautogui.hotkey('ctrl', 'end')
        #type
        pyautogui.typewrite(text,interval=0.2)
        #wait 2 seconds
        time.sleep(2)
        #save the file
        pyautogui.hotkey('ctrl', 's')
        pyautogui.hotkey('alt', 'f4')
        pass

    def read_file(self):

        #see if the file exsists
        if self.check_file_exists(filePath):
            #if it does return all the text

            #content of the file
            content = ""

            #reading the file
            try:
                with open(filePath, 'r') as file:
                    content = file.read()
            except FileNotFoundError:
                print(f"Error: The file '{filePath}' does not exist.")
                return None
            except Exception as e:
                print(f"Error: An unexpected error occurred - {e}")
                return None


            #then simulate reading it
            subprocess.Popen(['notepad.exe',filePath])
            time.sleep(5)
            pyautogui.hotkey('alt', 'f4')

            #then return the content
            return content
            

        else:
            #else the file does not exsist
            #TODO something here if trying to read a file that does not exsist
            pass

        


# Example usage:
if __name__ == "__main__":
    notepad_channel = NotepadChannel()
    notepad_channel.send("continueing!")
    time.sleep(2)
    print(notepad_channel.read_file())




