import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import swiggy as sg
import multiprocessing
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



from selenium.webdriver.common.by import By
def reslist(urq):
# pattern=r'^\w+\s\w+'
    url=urq
    driver = webdriver.Chrome()
    driver.get(url)
    hname_ind=urq.rfind('/')
    hname=urq[hname_ind+1:]
    H_name=hname.capitalize()
    
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
    # search_box = driver.find_element(By.XPATH, "//input[@placeholder='Enter your delivery location']")

    # # Click the element

    # driver.find_element_by_xpath("//input[@placeholder='Enter your delivery location']")
    # search_box.send_keys("agra")
    # time.sleep(2)
    # results=driver.find_element(By.XPATH,"//span[normalize-space()='Agra, Uttar Pradesh, India']").click()
    # search_box.send_keys(Keys.RETURN)

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
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # Find all the restaurant names on the page and print them to the console
    restaurant_names = soup.find_all('div', {'class': '_3XX_A'})
    restn=[]
    prename=[]
    folder_path='C:/Users/tusha/Desktop/vscode/SWIGGY/text_files'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) 
    file_path=folder_path+'/'+ f"restaurants_names_{H_name}.txt"
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
    file_path1=folder_path+'/'+ f"restaurants_links_{H_name}.txt"
    file_path2=folder_path+'/'+ f"prename_{H_name}.txt"
    with open(file_path1, 'w',encoding='utf-16') as file1,open(file_path2,'w',encoding='utf-16') as file2:
        # Write a string to the file
        
        for link in links:
            if(link.get('href')!=None and link.get('href')[0:5]=="/rest"  ): 
                lkd=url+link.get('href')
                last_slash_index = lkd.rfind('/')
                nline=lkd[last_slash_index + 1:last_slash_index +20]
                neline=nline.replace("-","_")
                file2.write(neline+'\n')
                prename.append(neline)
                restl.append(lkd)
                file1.write(lkd+'\n')
                #print(lkd)
                
    print(len(restn),len(restl),len(prename))  
 
    
        # processes=[] 
        # for i in range(len(restl)): 
        #     p=multiprocessing.Process(target=sg.diffres, args=(restl[i],prename[i],H_name,))
        #     processes.append(p)
        #     p.start()
            
        # for p in processes:
        #     p.join()
    
    

