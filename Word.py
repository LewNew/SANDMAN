import pyautogui
import time

# Function to type text in the active window
def type_text(text, typing_speed=0.05):
    for char in text:
        pyautogui.typewrite(char, interval=typing_speed)

# Sample text to write
text_to_type = "This is a sample text being typed!"

# Make sure there's a pause to switch to the Word document manually
print("You have 5 seconds to switch to the Word document...")
time.sleep(5)

# Call the function to type text
type_text(text_to_type)
