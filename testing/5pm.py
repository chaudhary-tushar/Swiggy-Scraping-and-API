'''This python script is to be ran on 1700 hrs to check the most numbers of restaurant of a city'''


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from multiprocessing import Pool, cpu_count
import time
from datetime import datetime

def getlinks():               
    city_links=[]                
    with open("city.csv",'r',encoding='utf-8') as file1:
        for line in file1:
            if line not in city_links:
                city_links.append(line[:-1])
    return city_links

def rest_list(urq):
    '''This function takes url as an argument and outputs csv files containing: restaurant details/links/prenames'''
    url=urq
    
    hname_ind=urq.rfind('/')        #H_name is the variable used for naming 3 files
    hname=urq[hname_ind+1:]  
    hname=hname.replace("\n","")    # Pre_name (contains only name), Restaurants_link (contains links to restaurants)
    H_name=hname.capitalize()       # and restaurants name (which include all the information like promotion and address)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-javascript")
    options.add_argument("--disable-animations")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    print(f"working on {H_name}")
    wait = WebDriverWait(driver, 5)

    # wait for the element to be clickable 
    #updated on 15 march 2023 since swiggy update changing the label to class
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='sc-dmyDGi dpnlFb style__TextContainerMain-sc-btx547-3 fObFec']")))



    # click the element
    element.click()
    search_box=driver.find_element(By.XPATH, "//input[@placeholder='Search for area, street name...']")
    search_box.send_keys(H_name)
    
    wait = WebDriverWait(driver, 5)
    results=wait.until(EC.element_to_be_clickable((By.XPATH, f"//body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]")))                                             
    results.click()
    try:
        wait = WebDriverWait(driver, 15)
        element = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='BZR3j']")))
        countres=element.text
        return countres,H_name
        
    except  TimeoutException:
        print(f"{H_name} restaurants not listed ")
        driver.quit()
        return 0,H_name
    
if __name__=="__main__":
    times=time.time()
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    cit=getlinks()
    citi=cit
    num_processes=cpu_count()
    print(citi)
    print(f"Running {num_processes} processes in parallel...")
    with Pool(num_processes) as p:
        results=p.map(rest_list,citi)
        p.close()
        p.join()
    print(results)
    timee=time.time()
    runtime=timee-times
    print(runtime)
    
    with open("5pm.csv",'w') as file1:
        file1.write(f"Ran On {date_time}\n{runtime}\n\n\n")
        for item in results:
            line = '{} {}\n'.format(item[0], item[1])
            file1.write(line)
        