from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import random
import json
import pyautogui
from Channel import Channel

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


class WebChannel(Channel):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\Firefox.exe"
        self.geckodriver_path = "C:\\Program Files\\Mozilla Firefox\\geckodriver.exe"

    def open_browser(self, url):
        # Create FirefoxOptions and set the binary location
        firefox_options = FirefoxOptions()
        firefox_options.binary_location = self.firefox_binary_path

        # Create the WebDriver with FirefoxOptions
        service = FirefoxService(executable_path=self.geckodriver_path)
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        self.driver.get(url)

    def accept_cookies(self):
        try:
            # Wait for the "Accept All" button to be clickable, and then click it
            accept_button_xpath = '/html/body/div[2]/div[3]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div'
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, accept_button_xpath))
            ).click()
            print('Clicked on accept cookies!')
        except Exception as e:
            print('Could not click on accept cookies:', e)

    def load_cookies(self):
        with open("cookies.txt", "r") as cookies_file:
            cookies = json.loads(cookies_file.read())
            for cookie in cookies:
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)
        self.driver.refresh()  # Refresh page to apply cookies

    def search_for(self, keyword):
        if self.driver:
            search_box = self.driver.find_element(By.NAME, 'q')  # Google's search box name='q'
            search_box.send_keys(keyword + Keys.RETURN)
            time.sleep(random.uniform(2, 5))

    def click_link(self):
        if self.driver:
            links = self.driver.find_elements(By.XPATH, '//div[@class="tF2Cxc"]//h3')
            if links:
                links[0].click()  # Clicks the first link
                time.sleep(random.uniform(2, 5))

    def scroll_page(self):
        if self.driver:
            for _ in range(random.randint(5, 15)):
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(0.2)

    def close_browser(self):
        if self.driver:
            self.driver.quit()

    def scroll_page_realistic(self):
        if self.driver:
            scroll_duration = random.uniform(0.5, 1.5)  # Randomize scroll duration
            num_scrolls = random.randint(5, 15)

            for _ in range(num_scrolls):
                scroll_distance = random.randint(100, 300)  # Randomize scroll distance
                pyautogui.scroll(scroll_distance, duration=scroll_duration)
                time.sleep(random.uniform(0.5, 1.5))  # Randomize sleep time between scrolls

    def type_text(self, text, typing_speed=0.02):
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

            if random.random() < 0.03:  # 3% chance to pause
                time.sleep(random.uniform(0.2, 1.5))  # Random pause between 0.2 to 1.5 sec


    def send(self, **kwargs):
        print("send")
        #TODO if you want web task to work then code the implementation from here!!
    
    
    def recv(self, **kwargs):
        print("recv")
        pass

    
    def read(self, **kwargs):
        print("read")
        pass


if __name__ == "__main__":


    # web_channel = WebChannel()
    web_channel.open_browser("https://www.google.com")
    time.sleep(5)  # Adjust time based on network speed and typical load times
    web_channel.accept_cookies()

    try:
        # Wait for the search box to be clickable, and then select it
        WebDriverWait(web_channel.driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'q'))
        ).send_keys("Sky News" + Keys.RETURN)
        print('Typed "Sky News" into the search box and submitted the search')
    except Exception as e:
        print('Could not type "Sky News" into the search box:', e)

    # Click on the first link using a different XPath
    try:
        WebDriverWait(web_channel.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tF2Cxc h3'))
        ).click()
        print('Clicked on the first link')
    except Exception as e:
        print('Could not click on the first link:', e)

    # Slowly scroll the page
    for _ in range(10):  # You can adjust the number of times to scroll
        web_channel.scroll_page()
        time.sleep(2)  # Adjust the sleep time between scrolls

    # Close the browser
    web_channel.close_browser()
