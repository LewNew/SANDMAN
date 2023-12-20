from abc import ABC, abstractmethod
import subprocess
import pyautogui
import time
from Channel import Channel
import os



class NotepadChannel(Channel):
    def __init__(self,file_path,file_name):
        super().__init__()
        self.file_path = file_path
        self.file_name = file_name

    #parent method #
    #needs:
    #text = "text to be imputted"
    def send(self, **kwargs):

        text = kwargs["text"]


        # Open Notepad using subprocess
        if not self.check_file_exists():
            self.new_file(text)
        else:
            self.continue_file(text)

        return True
        
    #parent method
    def recv(self):
        # This method could be used to receive data from Notepad, if applicable
        pass

    #parent method
    def read(self):
        #see if the file exsists
        if self.check_file_exists():
            #if it does return all the text

            #content of the file
            content = ""

            #reading the file
            try:
                with open(self.file_path+self.file_name, 'r') as file:
                    content = file.read()
            except FileNotFoundError:
                print(f"Error: The file '{self.file_path+self.file_name}' does not exist.")
                return None
            except Exception as e:
                print(f"Error: An unexpected error occurred - {e}")
                return None


            #then simulate reading it
            #open the file
            subprocess.Popen(['notepad.exe',self.file_path+self.file_name])
            #spend 5 seconds reading it
            time.sleep(5)
            pyautogui.hotkey('alt', 'f4')

            #then return the content
            return content
            
        else:
            #else the file does not exsist
            #TODO something here if trying to read a file that does not exsist
            pass




    def save_new_file(self):
        # Press Ctrl + S to trigger the Save dialog
        pyautogui.hotkey('ctrl', 's')
        # Wait for the Save As dialog to appear
        time.sleep(2)
        # Type the file path and press Enter
        pyautogui.typewrite(self.file_path+self.file_name)
        # Wait for the file path to be registered
        time.sleep(2)
        pyautogui.press('enter')
        # Wait for the Save dialog to close
        time.sleep(2)

    def check_file_exists(self):
        return os.path.exists(self.file_path+self.file_name)

    def new_file(self,text):

        subprocess.Popen(['notepad.exe'])
        # Wait for Notepad to open
        time.sleep(2)
        # Type and send the text to Notepad
        pyautogui.typewrite(text,interval=0.2)
        # wait to save
        time.sleep(2)
        #save the file
        self.save_new_file()
        #close the program
        pyautogui.hotkey('alt', 'f4')
        pass

    def continue_file(self,text):

        #if file already exsists continue it
        subprocess.Popen(['notepad.exe',self.file_path+self.file_name])
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





# Example usage:
if __name__ == "__main__":
    notepad_channel = NotepadChannel("H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework.txt")
    notepad_channel.send(text="continueing!")
    time.sleep(2)
    print(notepad_channel.read())




