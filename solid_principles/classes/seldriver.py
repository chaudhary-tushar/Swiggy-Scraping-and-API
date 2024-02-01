from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Sel_Driver:
    """This class returns the initialized selenium driver"""

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--log-level=3')
        options.add_argument('--headless')
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-javascript")
        options.binary_location = "C:/Users/tusha/AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe"  # noqa
        options.add_argument("--disable-animations")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_driver_path = "C:/Users/tusha/Desktop/vscode/SWIGGY/driver/chromedriver.exe"
        service = Service(executable_path=chrome_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)

    def get_driver(self):

        return self.driver

    def get_page_source(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        return self.driver.page_source
