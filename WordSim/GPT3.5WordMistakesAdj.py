import pyautogui
import time
import random
from openai import OpenAI

# Lewis' OpenAI Key
client = OpenAI(api_key='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')

# Function to get response from OpenAI GPT
def get_gpt_response(prompt):
    response = client.completions.create(
        prompt=prompt,
        model="gpt-3.5-turbo-instruct",
        top_p=0.5, max_tokens=150,
        stream=True)

    response_text = ""
    for part in response:
        response_text += part.choices[0].text or ""
    return response_text

# Adjacent QWERTY Keys
adjacent_keys = {
    'a': 'qwsz',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'erfcx',
    'e': 'rdsw34',
    'f': 'tgvcdr',
    'g': 'yhbvf',
    'h': 'ujngb',
    'i': 'u8kjo',
    'j': 'ikmnhu',
    'k': 'oljm',
    'l': 'pok',
    'm': 'njk',
    'n': 'bhjm',
    'o': 'i90lp',
    'p': 'o0l',
    'q': 'wa12',
    'r': 't45efqd',
    's': 'awedxz',
    't': 'y56rfg',
    'u': 'y7ijh',
    'v': 'cfbg',
    'w': 'q23esa',
    'x': 'zsdc',
    'y': 't67uh',
    'z': 'asx',
    '0': 'p9',
    '1': '2q',
    '2': '13qw',
    '3': '24we',
    '4': '35er',
    '5': '46rt',
    '6': '57ty',
    '7': '68yu',
    '8': '79iu',
    '9': '80oi',
}


# Function to type text in the active window with realistic mistakes
def type_text(text, typing_speed=0.02):
    for i, char in enumerate(text):
        if random.random() < 0.03 and i > 0:  # 3% mistake chance
            previous_char = text[i - 1].lower()
            mistake_options = adjacent_keys.get(previous_char, '')
            if mistake_options:
                mistake = random.choice(mistake_options)
                pyautogui.typewrite(mistake, interval=typing_speed)
                pyautogui.press('backspace', interval=typing_speed)

        pyautogui.typewrite(char, interval=typing_speed)

        if random.random() < 0.03:  # 3% chance to pause
            time.sleep(random.uniform(0.2, 1.5))  # Random pause between 0.2 to 1.5 sec

def main():
    prompt = "Very concisely give me an overview of Lancaster University in the UK\n\n"
    #prompt = "True or false: a banana is smaller than a lemon.\n\n"
    gpt_response = get_gpt_response(prompt)

    print("Switch to Word")
    time.sleep(5)

    type_text(gpt_response)

if __name__ == "__main__":
    main()
