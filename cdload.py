import requests
import time
import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

def citycsvmaker():
    url="https://www.swiggy.com"
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.3"}
    response=requests.get(url,headers=headers)
    if(response.status_code!=200):
        print("Code not 200")
        sys.exit(1)
    print("creating city.csv")
    soup=BeautifulSoup(response.content,'html.parser')
    links=soup.find_all('a')
    
    with open("cityt3.csv",'w',encoding='utf-8') as file1:
        for link in links:
            if(link.get('href')!=None and link.get('href')[0:5]=="/city"  ):
                lkd=url+link.get('href')
                file1.write(lkd+'\n')
                



citycsvmaker()