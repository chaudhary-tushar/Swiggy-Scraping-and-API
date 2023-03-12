import requests
import bs4
from selenium import webdriver
import time
import multiprocessing as mp
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



url="https://www.swiggy.com/city/bangalore"
h_ind=url.rfind('/')
h_name=url[h_ind+1:]
H_name=h_name.capitalize()
driver=webdriver.Chrome()
driver.get(url)
time.sleep(5)
# assuming you have already created a webdriver instance named "driver"
wait = WebDriverWait(driver, 5)

# wait for the element to be clickable
element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Open Sidebar']")))

# click the element
element.click()
#gee=driver.find_element(By.XPATH, "")
search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search for area, street name..']")
#search_box.send_keys(Keys.ENTER)
search_box.send_keys(H_name)
print(f"//div[normalize-space()={H_name}]")
wait = WebDriverWait(driver, 5)
results=wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[normalize-space()='{H_name}']")))
results.click()
time.sleep(20)


driver.close()
