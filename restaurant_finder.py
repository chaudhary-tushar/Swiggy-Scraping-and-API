import requests
import Menu_builder as sg
import multiprocessing as mp
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import div_finder as sw

#this is the main function which finds all the restaurants of a city whose url is provided in main.py
#It opens a selenium-automated webpage to scroll and find all the restaurants of the city since swiggy is dynamic and-
# getting all the restaurants is impossible by using requests 

# def menu(urq):
#     url=urq 
#     nameind=urq.rfind('/')
#     name=urq[nameind+1:nameind+20]
#     print(name)
    
#     #divs = sw.perres(url)[1:-1]
    
    
#     folder_path='C:/Users/tusha/Desktop/vscode/SWIGGY/text_files/city_res_menus'
    
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path) 
#     file_path= folder_path +'/'+ f"restaurant_{name}.csv"
#     #if os.path.isfile(os.path.join(folder_path, file_path)):
#     if os.path.isfile(file_path):
#         print(f"{file_path} File exists!")
#         return
#     else:
#         print(f"{file_path} does not exists")
#         divs = sw.perres(url)[1:-1]
#         with open(file_path,'w',encoding='utf-8') as file1:
#             for div in divs:
#                 #print()
#                 #print(div.get('id'))
#                 file1.write('\n'+div.get('id')+'\n'+'\n')
#                 #print()
#                 paragraphs = div.find_all('p', {'class': 'ScreenReaderOnly_screenReaderOnly___ww-V'})
#                 #print()
                
#                 # Loop through the paragraphs and print their text content
#                 for paragraph in paragraphs:
#                     file1.write(paragraph.text+'\n')
#                     #print(paragraph.text)

def reslist(urq):
    url=urq
    driver = webdriver.Chrome()
    driver.get(url)
    hname_ind=urq.rfind('/')    #H_name is the variable used for naming 3 files
    hname=urq[hname_ind+1:]     # Pre_name (contains only name), Restaurants_link (contains links to restaurants)
    H_name=hname.capitalize()   # and restaurants name (which include all the information like promotion and address)
    
    wait = WebDriverWait(driver, 5)

    # wait for the element to be clickable 
    #updated on 15 march 2023 since swiggy update changing the label to class
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='sc-dmyDGi dpnlFb style__TextContainerMain-sc-btx547-3 fObFec']")))



    # click the element
    element.click()
    
    search_box=driver.find_element(By.XPATH, "//input[@placeholder='Search for area, street name...']")
    search_box.send_keys(H_name)
    
    print(f"//div[@class='sc-dmyDGi iDBMVs'][normalize-space()='{H_name}']")
    wait = WebDriverWait(driver, 5)
    #updated on 15 march 2023 since swiggy updated the relpath of first button on dropddown
    results=wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='sc-dmyDGi iDBMVs'][normalize-space()='{H_name}']")))
    results.click()
                                                                

    time.sleep(2)  # Allow 2 seconds for the web page to (open depends on you)
    scroll_pause_time = 2  # You can set your own pause time. dont slow too slow that might not able to load more data
    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
    i = 1

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break
        
        
    # Wait for the search results to load and get the HTML content of the page

    html = driver.page_source
    driver.quit()

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the restaurant names on the page and print them to the console
    restaurant_names = soup.find_all('div', {'class': '_3XX_A'})
    restn=[]
    folder_path=f'C:/Users/tusha/Desktop/vscode/SWIGGY/text_files/{H_name}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) 
    file_path=folder_path+'/'+ f"restaurants_names_{H_name}.csv"
    with open(file_path, 'w',encoding='utf-8') as file:
        # Write a string to the file
        for name in restaurant_names:
            line=name.text
            name=line
            #print(name)
            restn.append(name)
            file.write(name+'\n')

    # Close the Selenium webdriver

    my_div = soup.find('div', {'class': 'nDVxx'})

    # Find all the links within the div
    links = my_div.find_all('a')

    # Loop through each link and print its URL
    restl=[]
    prename=[]
    file_path1=folder_path+'/'+ f"restaurants_links_{H_name}.csv"
    file_path2=folder_path+'/'+ f"prename_{H_name}.csv"
    with open(file_path1, 'w',encoding='utf-16') as file1,open(file_path2,'w',encoding='utf-16') as file2:
        # Write a string to the file
        
        for link in links:
            if(link.get('href')!=None and link.get('href')[0:5]=="/rest"  ): 
                lkd="https://www.swiggy.com"+link.get('href')
                last_slash_index = lkd.rfind('/')
                nline=lkd[last_slash_index + 1:last_slash_index +20]
                neline=nline.replace("-","_")
                file2.write(neline+'\n')
                prename.append(neline)
                restl.append(lkd)
                file1.write(lkd+'\n')
                #print(lkd)
                
    print(len(restn),len(restl),len(prename))  
    
    
        

    
'''Here i have to add functionality to call menu builder with multiprocessing'''
    
    

