from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time


class WebChannel:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.geckodriver_path = "C:\\Program Files\\Mozilla Firefox\\geckodriver.exe"


    def open_browser(self):
        """Open Firefox and navigate to URL"""
        # Set up the Firefox driver with the specified executable path
        firefox_options = FirefoxOptions()
        firefox_options.binary_location = "C:\\Program Files\\Mozilla Firefox\\Firefox.exe"

        service = Service(self.geckodriver_path)
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        self.driver.get(self.url)


    def scroll_page(self):
        """Simulated scrolling on page"""
        if self.driver:
            body = self.driver.find_element_by_tag_name('body')
            for _ in range(10):  # Scrolls down 10 times
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)  # Brief pause between scrolls


    def close_browser(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()


    def retrieve(self, url):
        pass


# Example usage:
if __name__ == "__main__":
    web_channel = WebChannel("https://www.reddit.com")
    web_channel.open_browser()
    time.sleep(5)  # Let the page load
    web_channel.scroll_page()
    time.sleep(5)  # Let the page scroll
    web_channel.close_browser()
