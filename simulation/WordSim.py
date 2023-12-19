import pyautogui
import time

# Function to type text in the active window
def type_text(text, typing_speed=0.05):
    for char in text:
        pyautogui.typewrite(char, interval=typing_speed)

text_to_type = "This is a sample text being typed!"

# Time allowance to switch to Word
print("You have 5 seconds to switch to the Word document...")
time.sleep(10)

type_text(text_to_type)
