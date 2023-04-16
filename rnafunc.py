'''this contains 4 functions and is called by diff.py
difflinks=returns  2-D array of restaurant links
citynames=returns array of city names
menu= outpust menu.csv of a restaurant link
mpmenu= calls menu function using multiprocessing
'''
import os
import time
import swiggyscrape
import requests
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, as_completed, CancelledError
from multiprocessing import Pool, cpu_count
from bs4 import BeautifulSoup
from selenium import webdriver

def sw(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu-driver-bug-workarounds")
    options.add_argument("--enable-native-gpu-memory-buffers")
    options.add_argument("--enable-gpu-rasterization")
    options.add_argument("--enable-zero-copy")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument('--headless')
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-javascript")
    options.add_argument("--disable-animations")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get(url) 

    # Get the HTML source code of the page using Selenium
    html = driver.page_source
    

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the divs on the page with class 'my-class'
    divs = soup.find_all('div')

    dids=[]
    # Loop through each div and print its text content
    for div in divs:
        div_id = div.get('id')
        if div_id:
            dids.append(div) 
    # Close the Selenium webdriver
    driver.close()
    return dids

def difflinks():
    cities=[]
    with open('city.csv','r', encoding='utf-8') as file: 
        for line in file:
            ind=line.rfind('/')
            line=line[ind+1:]
            city=line.replace("\n","")
            city=city.capitalize()
            cities.append(city)
            
    five=cities
    rlinks=[]
    fp=swiggyscrape.Folder()
    for name in five:
        clinks=[]
        file1=fp.getdbfile("links",name)
        if os.path.isfile(file1):
            with open(file1 ,'r',encoding='utf-16') as file:
                for line in file:
                    clinks.append(line.strip())
                file.close()
            if len(clinks)<20:
                rlinks.append(clinks[0:])
            else:
                rlinks.append(clinks[:10])
        else: continue
    return rlinks

def citynames():
    path='C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files'
    bity=os.listdir(path)
    return bity




def menu(urq,cname):
    url=urq
    nameind=urq.rfind('/')
    name=urq[nameind+1:nameind+20]
    folder_path=f'C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{cname}/menus'
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) 
    file_path= folder_path +'/'+ f"restaurant_{name}.csv"
    #if os.path.isfile(os.path.join(folder_path, file_path)):
    if os.path.isfile(file_path):
        print(f"{file_path} File exists!")
        return
    else:
        print(f"{file_path} does not exists")
        divs = sw(url)[:-1]
        with open(file_path,'w',encoding='utf-8') as file1:
            for div in divs:
                
                file1.write('\n'+div.get('id')+'\n'+'\n')
                paragraphs = div.find_all('p', {'class': 'ScreenReaderOnly_screenReaderOnly___ww-V'})
                
                
                # Loop through the paragraphs and print their text content
                for paragraph in paragraphs:
                    file1.write(paragraph.text+'\n')
                    
                    
                    
def mpmenu(crlink,city_name):
    # q=mp.Pool()
    # q.starmap(menu,[(crlink[_],city_name) for _ in range(len(crlink))])
    
    # q.close()
    # q.join()
    with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(menu, crlink, [city_name]*len(crlink))
            executor.shutdown(wait=True)
    
    
            

    

