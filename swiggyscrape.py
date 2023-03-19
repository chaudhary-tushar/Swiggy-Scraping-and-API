''' This File contains the Scraping functions of the Project with appropriate documentation for every function when called
For the workflow to be defined as the the following steps in which function are called:-
Step1: City               :     This functions takes the swiggy url and outputs links contained in cities[] and city.csv
Step2: Restaurant finder  :     This functions takes the URL's of cities from cities[] and calls selenium webdriver to scroll through all the restaurant in that url 
                                and outputs {city} named folder containing name of restaurant , links of restaurant  
Step3: Menu Builder       :     This functions takes the URL's of restaurant and builds the menus in the menu folder inside the city folder created in step 2. 
                                This functions calls Step 4 to get divs for scraping.
Step4: Div finder         :     This function is necessary for step 3 since without this opening driver.chrome the divs we get from request just gives the recommended part of the menu
Step5: CheckF             :     This function checks if the website listed value of restaurants and menu items is as same as extracted in scraping.
'''
import requests
import os
import multiprocessing as mp
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
import time
import multiprocessing as mp
import requests
from bs4 import BeautifulSoup
import re
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Folder:
    
    folder_path="C:/Users/tusha/Desktop/vscode/SWIGGY"

    def get_folder(self):
        current_folder_path = self.folder_path
        return current_folder_path
    
    def get_file(self,str):
        fold_path=self.get_folder()
        return f'{fold_path}/{str}.csv'
    
    def getdbfolder(self,Cname):
        current_path=self.get_folder()
        med_path='/txt_files/'
        target_path=f'{Cname}'
        med=current_path+med_path
        if not os.path.exists(med):
            os.makedirs(med)
        fold_path=med+target_path
        if not os.path.exists(fold_path):
            os.makedirs(fold_path)
        return fold_path
    
    def getdbfile(self,stng,Cname):
        fold_path=self.getdbfolder(Cname)
        if(stng=="details"):
            return f'{fold_path}/restaurant_details_{Cname}.csv'
        if(stng=="links"):
            return f'{fold_path}/restaurant_links_{Cname}.csv'
        if(stng=="pre"):
            return f'{fold_path}/pre_names_{Cname}.csv'
        if(stng=="tot"):
            return f'{fold_path}/total_restaurants_{Cname}.csv'
        
    def getmenufolder(self,Cname):
        current_path=self.get_folder()
        med_path=f'/txt_files/{Cname}'
        target_path='/menus'
        med=current_path+med_path
        if not os.path.exists(med):
            os.makedirs(med)
        fold_path=med+target_path
        if not os.path.exists(fold_path):
            os.makedirs(fold_path)
        return fold_path
        
    def getmenudb(self,Cname,resname):
        fold_path=self.getmenufolder(Cname)
        target_path=f'/restaurant_{resname}.csv'
        fpath=fold_path+target_path
        return fpath
    
        
    
        
        
    
class City:
    def __init__(self):
        pass
    
    def city(self,url):
        fp=Folder()
        folder_path=fp.get_folder()
        file_name="city.csv"
        file_path = os.path.join(folder_path, file_name)
        
        city_links=[]
        city_names=[]

        if os.path.isfile(file_path):
            with open(file_path,'r',encoding='utf-8') as file1:
                for line in file1:
                    if line not in city_links:
                        city_links.append(line[:-1])
                        ind=line.rfind('/')
                        line=line[ind+1:]
                        city=line.replace("\n","")
                        city=city.capitalize()
                        city_names.append(city)
            print("File exists in the folder.")
            
            
            
        else:
            response=requests.get(url)
            soup=BeautifulSoup(response.content,'html.parser')
            links=soup.find_all('a')
            with open(file_path,'w',encoding='utf-8') as file1:
                for link in links:
                    if(link.get('href')!=None and link.get('href')[0:5]=="/city"  ):
                        lkd=url+link.get('href')
                        if lkd not in city_links:
                            file1.write(lkd+'\n')
                            city_links.append(lkd)
                            ind=lkd.rfind('/')
                            line=lkd[ind+1:]
                            city=line.replace("\n","")
                            city=city.capitalize()
                            city_names.append(city) 
                            
            print(f"{file_name} is created in {folder_path}")
        return city_links,city_names
    
    
    

class Restaurant_finder:
    '''This class is to crawl through all the city links from city.csv and print them in their named folder'''
    
    def rest_list(self,urq):
        '''This function takes url as an argument and outputs csv files containing: restaurant details/links/prenames'''
        url=urq
        
        hname_ind=urq.rfind('/')        #H_name is the variable used for naming 3 files
        hname=urq[hname_ind+1:]  
        hname=hname.replace("\n","")    # Pre_name (contains only name), Restaurants_link (contains links to restaurants)
        H_name=hname.capitalize()       # and restaurants name (which include all the information like promotion and address)
        options = webdriver.ChromeOptions()
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
        #print(f"//div[@class='sc-dmyDGi iDBMVs'][normalize-space()='{H_name}']")
        #updated on 15 march 2023 since swiggy updated the relpath of first button on dropddown.
        results=wait.until(EC.element_to_be_clickable((By.XPATH, f"//body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]")))                                             
        results.click()
        try:
            wait = WebDriverWait(driver, 15)
            element = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='BZR3j']")))
            countres=element.text
            
        except  TimeoutException:
            print(f"{H_name} restaurants not listed ")
            driver.quit()
            return H_name
        
        else:
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
                # if i>5:
                #     break
                
            # Wait for the search results to load and get the HTML content of the page

            html = driver.page_source
            driver.quit()
            print(f"{H_name} parsed")
            # Parse the HTML content using Beautiful Soup
            soup = BeautifulSoup(html, 'html.parser')

            # Find all the restaurant names on the page and print them to the console
            restaurant_names = soup.find_all('div', {'class': '_3XX_A'})
            restn=[]
            fp=Folder()
            file_path0=fp.getdbfile("details",H_name)
            if os.path.isfile(file_path0):
                with open(file_path0, 'r',encoding='utf-8') as file:
                    # Write a string to the file
                    for name in file:
                        restn.append(name)
                    file.close()
                        
                with open(file_path0, 'a',encoding='utf-8') as file:
                    # Write a string to the file
                    for name in restaurant_names:
                        if name.text not in restn:
                            line=name.text
                            name=line
                            restn.append(name)
                            file.write(name+'\n')
            else:            
                with open(file_path0, 'w',encoding='utf-8') as file:
                    # Write a string to the file
                    for name in restaurant_names:
                        line=name.text
                        name=line
                        restn.append(name)
                        file.write(name+'\n')


            my_div = soup.find('div', {'class': 'nDVxx'})

            # Find all the links within the div
            links = my_div.find_all('a')

            # Loop through each link and print its URL
            restl=[]
            prename=[]
            file_path1=fp.getdbfile("links",H_name)
            
            file_path2=fp.getdbfile("pre",H_name)
            if os.path.isfile(file_path1) and os.path.isfile(file_path2):
                with open(file_path1, 'r',encoding='utf-16') as file1,open(file_path2,'r',encoding='utf-16') as file2:
                    for line in file1:
                        restl.append(line)
                    for line1 in file2:
                        prename.append(line1)
                    file1.close()
                    file2.close()
                with open(file_path1, 'a',encoding='utf-16') as file1,open(file_path2,'a',encoding='utf-16') as file2:
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
            
            else:
                with open(file_path1, 'w',encoding='utf-16') as file1,open(file_path2,'w',encoding='utf-16') as file2:
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
            mv=0
            qre=re.search(r'\d+',countres)
            countres=int(qre.group())
            file_path3=fp.getdbfile("tot",H_name)  
            if os.path.isfile(file_path3):  
                with open(file_path3,'r',encoding='utf-8') as filem:
                    for line in filem:
                        if "listed" in line:
                            match = re.search(r'\d+',line)
                            matchq=int(match.group())
                            mv=matchq       
                    filem.close()
                
                if mv<countres:
                    with open (file_path3,'w',encoding='utf-8') as fileq:
                        fileq.write(f"Total restaurants listed in {H_name} = {countres}\n")
                        fileq.write(f"Total restaurant links in {H_name}= {len(restl)}\n")
                        fileq.close()
                        
                else:
                    with open (file_path3,'a',encoding='utf-8') as fileq:
                        fileq.write(f"Total restaurant links in {H_name}= {len(restl)}\n")
                        fileq.close()
            else:
                with open (file_path3,'w',encoding='utf-8') as fileq:
                        fileq.write(f"Total restaurants listed in {H_name} = {countres}\n")
                        fileq.write(f"Total restaurant links in {H_name}= {len(restl)}\n")
                        fileq.close()
          
            
            
        
                  
                  
                  
class Multi_res_links:
    '''This class is to take restaurant_links{citynames} from different folders and output them as an array'''
    
    def get_links(self,flist):
        '''This function takes citynames list as a parameter and outputs a 2-D array'''
        rlinks=[]
        fp=Folder()
        for name in flist:
            clinks=[]
            file1=fp.getdbfile("links",name)
            with open(file1 ,'r',encoding='utf-16') as file:
                for line in file:
                    clinks.append(line.strip())
            rlinks.append(clinks[:10])          #remove the slicing in finished version
            
        return rlinks
    
    
class DivFinder:
    def div_finder(self,url):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
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
            driver.quit()
            return dids
    
class MenuBuilder:
    '''This class builds the menus of different restaurant and stores it in /txt_files/city/menus/*'''
    
    def menu(self,urq,cname):
        '''This function takes arguments as url and city name but is called by inbuilt class function mpmenu'''
        
        url=urq
        nameind=urq.rfind('/')
        name=urq[nameind+1:nameind+20]
        fp=Folder()
        #folder_path=fp.getmenufolder(cname)
        file_path=fp.getmenudb(cname,name)
        #file_path= folder_path +'/'+ f"restaurant_{name}.csv"
        #if os.path.isfile(os.path.join(folder_path, file_path)):
        if os.path.isfile(file_path):
            print(f"{file_path} File exists!")
            return
        else:
            print(f"{file_path} does not exists")
            DI=DivFinder()
            divs = DI.div_finder(url)[:-1]
            with open(file_path,'w',encoding='utf-8') as file1:
                for div in divs:
                    file1.write('\n'+div.get('id')+'\n'+'\n')
                    paragraphs = div.find_all('p', {'class': 'ScreenReaderOnly_screenReaderOnly___ww-V'})
                    
                    
                    # Loop through the paragraphs and print their text content
                    for paragraph in paragraphs:
                        file1.write(paragraph.text+'\n')
                        
    
    def mpmenu(self,crlink,city_name):
        '''This function takes argument as links array and city_name and calls menu function parallely'''
    
        with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(self.menu, crlink, [city_name]*len(crlink))
                executor.shutdown(wait=True)

    
class Managelists:
    '''This class is to remove cities from the url and names list to not make menus of those restaurants'''
    def remcity(self,namelist,urllist,name):
        '''This function takes city names,url names and cities to remove'''
        name=name.capitalize()
        index=namelist.index(name)
        namelist.pop(index)
        urllist.pop(index)
        return namelist,urllist
        