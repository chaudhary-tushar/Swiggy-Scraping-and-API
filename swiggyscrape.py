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
import traceback
import multiprocessing as mp
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
import time
import multiprocessing as mp
from bs4 import BeautifulSoup
import mysql.connector as connector
import pymongo
import psycopg2
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException,StaleElementReferenceException,ElementNotInteractableException,ElementNotSelectableException,ElementNotVisibleException,NoAlertPresentException,NoSuchFrameException,NoSuchWindowException,SessionNotCreatedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pandas as pd


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
        if(stng=="det_links"):
            return f'{fold_path}/restaurant_det_links_{Cname}.csv'
        
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
    
    def city(self,url):
        fp=Folder()
        folder_path=fp.get_folder()
        file_name="city.csv"
        file_path = f"{folder_path}/{file_name}"      
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
            headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.3"}
            response=requests.get(url,headers=headers)
            #response=requests.get(url)
            soup=BeautifulSoup(response.content,'html.parser')
            links=soup.find_all('a')
            with open(file_path,'w',encoding='utf-8') as file1:
                for link in links:
                    if(link.get('href')!=None and link.get('href')[0:5]=="/city" and link.get('href')[-11:]!="restaurants" ):
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
        options.add_argument('--ignore-certificate-errors')
        #options.add_argument('--headless')
        #options.add_argument("--blink-settings=imagesEnabled=false")
        #options.add_argument("--disable-javascript")
        options.binary_location = "C:/Users/tusha/AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe"
        #options.add_argument("--disable-animations")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #driver = webdriver.Chrome(options=options)
        # print(url)
        chrome_driver_path = "C:/Users/tusha/Desktop/vscode/SWIGGY/driver/chromedriver.exe"
        service=Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service,options=options)
        print(f"working on {H_name}")
        try:
            driver.get(url)
        except (TimeoutException,NoSuchElementException,WebDriverException,StaleElementReferenceException,ElementNotInteractableException,ElementNotSelectableException,ElementNotVisibleException,NoAlertPresentException,NoSuchFrameException,NoSuchWindowException,SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed 1st")
            driver.quit()
            exp_msg=type(e).__name__
            fault=f"{H_name} + {exp_msg}"
            return fault
        
        wait = WebDriverWait(driver, 5)

        # wait for the element to be clickable 
        #updated on 15 march 2023 since swiggy update changing the label to class
        try:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='sc-beySbM clsZsT style__TextContainerMain-sc-btx547-3 fObFec']")))
        except (TimeoutException,NoSuchElementException,WebDriverException,StaleElementReferenceException,ElementNotInteractableException,ElementNotSelectableException,ElementNotVisibleException,NoAlertPresentException,NoSuchFrameException,NoSuchWindowException,SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed 2nd")
            driver.quit()
            exp_msg=type(e).__name__
            fault=f"{H_name} + {exp_msg}"
            return fault

        # click the element
        element.click()
        try:
            wait = WebDriverWait(driver, 15)
            search_box=driver.find_element(By.XPATH, "//input[@placeholder='Search for area, street name...']")
            search_box.send_keys(H_name)
        except (TimeoutException,NoSuchElementException,WebDriverException,StaleElementReferenceException,ElementNotInteractableException,ElementNotSelectableException,ElementNotVisibleException,NoAlertPresentException,NoSuchFrameException,NoSuchWindowException,SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed  3rd")
            driver.quit()
            exp_msg=type(e).__name__
            fault=f"{H_name} + {exp_msg}"
            return fault
        
        try:
            wait = WebDriverWait(driver, 5)
            results=wait.until(EC.element_to_be_clickable((By.XPATH, f"//body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]"))) 
            results.click()
        except (TimeoutException,NoSuchElementException,WebDriverException,StaleElementReferenceException,ElementNotInteractableException,ElementNotSelectableException,ElementNotVisibleException,NoAlertPresentException,NoSuchFrameException,NoSuchWindowException,SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed 4th")
            driver.quit()
            exp_msg=type(e).__name__
            fault=f"{H_name} + {exp_msg}"
            return fault
        try:
            wait = WebDriverWait(driver, 15)
            element = wait.until(EC.presence_of_element_located((By.XPATH,"//h2[normalize-space()='Popular restaurants near me']")))
            
        except (TimeoutException,NoSuchElementException,WebDriverException,StaleElementReferenceException,ElementNotInteractableException,ElementNotSelectableException,ElementNotVisibleException,NoAlertPresentException,NoSuchFrameException,NoSuchWindowException,SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed  5th")
            driver.quit()
            exp_msg=type(e).__name__
            fault=f"{H_name} + {exp_msg}"
            return fault
        
        else:
            scroll_pause_time = 1  # You can set your own pause time. dont slow too slow that might not able to load more data
            i = 1

            toscroll=True
            while toscroll==True and i < 5:
                time.sleep(scroll_pause_time)
                try:
                    wait = WebDriverWait(driver, 5)
                    more=wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(text(),'Show more')]")))
                    more.click()
                    toscroll=True
                except:
                    toscroll=False 
                i+=1   
            # Wait for the search results to load and get the HTML content of the page

            html = driver.page_source
            driver.quit()
            print(f"{H_name} parsed")
            # Parse the HTML content using Beautiful Soup
            soup = BeautifulSoup(html, 'html.parser')

            # # Find all the restaurant names on the page and print them to the console
            fp=Folder()
            link_elements = soup.find_all('a', class_='RestaurantList__RestaurantAnchor-sc-1d3nl43-3 kcEtBq')
            names=[]
            links=[]
            for linkd in link_elements:
                links.append(linkd.get('href'))
                names.append(linkd.find('div', class_='sc-beySbM cwvucc').text.strip())
            print(H_name, len(names), len(links))
            file_path1=fp.getdbfile("det_links",H_name)
            data_dict = {"Details": names, "Links":links }

            # Create a pandas DataFrame from the dictionary
            df = pd.DataFrame(data_dict)

            # Check if the CSV file already exists
            try:
                existing_df = pd.read_csv(file_path1)
            except FileNotFoundError:
                existing_df = pd.DataFrame()

            # Check for duplicate values based on the "Details" and "Links" columns
            existing_names = set(existing_df["Details"]) if not existing_df.empty else set()
            existing_links = set(existing_df["Links"]) if not existing_df.empty else set()
            new_names = set(df["Details"])
            new_links = set(df["Links"])
            new_names_and_links = new_names.union(new_links)
            duplicate_names = new_names_and_links.intersection(existing_names)
            duplicate_links = new_names_and_links.intersection(existing_links)

            # If there are duplicate values, remove them from the new DataFrame
            if len(duplicate_names) > 0 or len(duplicate_links) > 0:
                df = df[~df["Details"].isin(duplicate_names)]
                df = df[~df["Links"].isin(duplicate_links)]

            # Append the new DataFrame to the existing one and write to a CSV file
            df.to_csv(file_path1, mode="a", index=False, header=existing_df.empty)
        


class Multi_res_links:
    '''This class is to take restaurant_links{citynames} from different folders and output them as an array'''
    
    def get_links(self,flist):
        '''This function takes citynames list as a parameter and outputs a 2-D array'''
        rlinks=[]
        fp=Folder()
        for name in flist:
            clinks=[]
            file1=fp.getdbfile("det_links",name)
            with open(file1 ,'r',encoding='utf-8') as file:
                lines=file.readlines()[1:]
                
                for line in lines:
                    lind=line.rfind(',')
                    link=line[lind+1:]
                    clinks.append(link.strip())
            rlinks.append(clinks[1:2])          #remove the slicing in finished version
            
        return rlinks
    
    
class DivFinder:
    def div_finder(self,url):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument("--blink-settings=imagesEnabled=false")
        # options.add_argument("--disable-javascript")
        # options.add_argument("--disable-animations")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--enable-chrome-browser-cloud-management")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_driver_path = "C:/Users/tusha/Desktop/vscode/SWIGGY/driver/chromedriver.exe"
        service=Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service,options=options)
        driver.get(url)
        driver.implicitly_wait(10)
        # Get the HTML source code of the page using Selenium
        html = driver.page_source
        driver.close()
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html, 'lxml')
        p_elements = soup.find_all('p', class_='ScreenReaderOnly_screenReaderOnly___ww-V', tabindex=0)
        p_element = p_elements[0]

        # Find all the divs on the page with class 'my-class'
        specific_div = soup.find('div', class_='nDVxx')
        divs = specific_div.find_all('div')

        dids=[]
        # Loop through each div and print its text content
        for div in divs:
            div_id = div.get('id')
            if div_id:
                dids.append(div) 
        # Close the Selenium webdriver
        return p_element, dids
    
class MenuBuilder:
    '''This class builds the menus of different restaurant and stores it in /txt_files/city/menus/*'''
    
    def menu(self,urq,cname):
        '''This function takes arguments as url and city name but is called by inbuilt class function mpmenu'''
        
        url=urq
        nameind=urq.rfind('/')
        name=urq[nameind+1:nameind+20]
        fp=Folder()
        file_path=fp.getmenudb(cname,name)
        if os.path.isfile(file_path):
            print(f"{file_path} File exists!")
            return
        else:
            print(f"{file_path} does not exists")
            DI=DivFinder()
            res_info, divs = DI.div_finder(url)
            print("reached menu writing stage with restaurant details as, ", res_info.text)
            with open(file_path,'w',encoding='utf-8') as file1:
                file1.write(res_info.text+ '\n')
                for div in divs:
                    file1.write('\n'+div.get('id')+'\n'+'\n')
                    paragraphs = div.find_all('p', {'class': 'ScreenReaderOnly_screenReaderOnly___ww-V'})
                    
                    
                    # Loop through the paragraphs and print their text content
                    for paragraph in paragraphs:
                        file1.write(paragraph.text.strip().replace('\n', '')+'\n')

    
    def mpmenu(self,crlink,city_name):
        '''This function takes argument as links array and city_name and calls menu function parallely'''
    
        with ThreadPoolExecutor(max_workers=4) as executor:
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



class restArr:
    '''This class makes the 2-D array of different restaurants to be filled in dbs.
    every array in the 2-d array has structure [city,restaurant_name,restaurant_url,cuisine,ratings,cost_for_two,discount,coupon]
    '''
    def __init__(self):
        self.foldpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
        
    def rest_makear(self):
        cit=os.listdir(self.foldpath)
        kamaalarr=[]
        
        for city in cit:
            detpath=f"{self.foldpath}/{city}/restaurant_det_links_{city}.csv"
            if (os.path.isfile(detpath)):
                menpath=f"{self.foldpath}/{city}/menus"
                df=pd.read_csv(detpath)
                details=df["Details"]
                links=df["Links"]
                x=len(links)
                for i in range(x):
                    pres=[]
                    pres.append(city)
                    rind=links[i].rfind('/')
                        
                    if ("%" in details[i]):
                        discountind=details[i].rfind('%')
                        discount=details[i][discountind-2:discountind]
                        couponind=details[i].rfind("Use")
                        couponlind=details[i].rfind("Quick")
                        coupon=details[i][couponind+4:couponlind]
                    restaurantname=links[i][rind+1:rind+20]
                    menu=f"{menpath}/restaurant_{restaurantname}.csv"
                    if os.path.isfile(menu):
                        with open(menu,'r',encoding='utf-8') as fileq:
                            lines3=fileq.readlines()
                            impdat=lines3[3:8]
                            
                            namind=impdat[0].rfind(':')
                            namelind=impdat[0].find(',',namind)
                            name=impdat[0][namind+2:namelind]
                            pres.append(name.replace("'",""))
                            
                            pres.append(links[i].replace('\n',''))
                                
                            cusind=impdat[1].rfind(':')
                            cuslind=impdat[1].rfind(',')
                            cuisine=impdat[1][cusind+2:cuslind]
                            if len(cuisine)>=10:
                                cuisine=cuisine.replace(","," &")
                            pres.append(cuisine)
                                
                            ratind=impdat[2].rfind(':')
                            ratlind=impdat[2].rfind(',')
                            rating=impdat[2][ratind+2:ratlind]
                            if len(rating)<4:
                                pres.append(rating)
                            else:
                                pres.append("3.8")
                                
                            costind=impdat[4].rfind(':')
                            costlind=impdat[4].rfind('f')
                            costfortwo=impdat[4][costind+3:costlind]
                            pres.append(costfortwo)
                            fileq.close()
                    else:
                        pass
                    pres.append(discount)
                    if len(coupon)<=10:   
                        pres.append(coupon)
                    else:
                        pres.append(None)
                    while(len(pres)<8):
                        pres.append(None)
                    kamaalarr.append(pres)
        with open("insertingdb.csv",'w',encoding='utf- 16')as fil:
            for i in range(len(kamaalarr)):
                fil.write(f'{kamaalarr[i]}\n')
        return kamaalarr  
    def city_makearr(self):
        '''Makes 2-D array of citynames and citylinks'''
        ctar=[]
        with open('city.csv','r') as file:
            i=1
            for line in file:
                perc=[]
                lnk=line.rstrip('\n')
                nind=lnk.rfind('/')
                nme=lnk[nind+1:]
                name=nme.capitalize()
                perc.append(i)
                perc.append(name)
                perc.append(lnk)
                i+=1
                ctar.append(perc)
        return ctar
    
class MSQL:
    def __init__(self):
        self.con=connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'swiggdb')
        query='CREATE TABLE if not exists citydat(cityId int PRIMARY KEY AUTO_INCREMENT, CityName varchar(50), CityUrl varchar(200))'
        cur=self.con.cursor()
        cur.execute(query)
        print("table created")
        
        query="CREATE TABLE if not exists restaurant_dat(rest_Id int PRIMARY KEY AUTO_INCREMENT,city_name varchar(50) NULL, rest_Name varchar(50) NULL, rest_Url varchar(200) NULL,cuisine varchar(100) NULL,ratings varchar(5) NULL,cost_for_two varchar(50) NULL , discount int NULL , coupon varchar(20) NULL)"
        cur=self.con.cursor()
        cur.execute(query)
        print("restaurant table created")  
    def city_insert(self,ctname,cturl):
        '''inserts cityname , cityurl into citydat'''
        query=f"insert into citydat(CityName,CityUrl) values ('{ctname}','{cturl}')"
        cur=self.con.cursor()
        try:
            cur.execute(query)
        except:
            pass
        self.con.commit()
        
    
    def rest_insert(self,list):
        '''inserts [city name ,restaurant name , rest url ,cuisine,ratings ,cost for two, discount ,coupon] into restaurant dat'''
        query=f"insert into restaurant_dat(city_name,rest_name,rest_url,cuisine,ratings,cost_for_two,discount,coupon) values ('{list[0]}','{list[1]}','{list[2]}','{list[3]}','{list[4]}','{list[5]}','{list[6]}','{list[7]}')"
        cur=self.con.cursor()
        try:
            cur.execute(query)
        except:
            pass
        self.con.commit()
    
    def data(self):
        cur=self.con.cursor()
        print("data in Mysql")
        print("restaurants")
        cur.execute('SELECT COUNT(*) FROM restaurant_dat')
        count=cur.fetchone()[0]
        print(count)
        print("cities")
        cur.execute('SELECT COUNT(*) FROM citydat')
        count=cur.fetchone()[0]
        print(count)
        
    

class MNGDB:
    '''To insert data into Mongodb'''
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['swiggdb'] 
    
    def city_insert(self,name,url):
        '''To insert cityname and cityurl into cities'''
        db=self.db
        citydata=[{'CityName':f'{name}','CityUrl':f'{url}'}]
        try:
            db.Cities.insert_many(citydata)
        except:
            pass
        
        
    def rest_insert(self,list):
        '''input the restArr list '''
        db=self.db
        Restaurant_details=[{'City': f'{list[0]}','RestaurantName': f'{list[1]}','Rest_Url': f'{list[2]}','Cuisine': f'{list[3]}','Ratings': f'{list[4]}','Cost_Two': f'{list[5]}','Discount': f'{list[6]}','Coupon': f'{list[7]}'}]
        
        try:
            db.Restaurants.insert_many(Restaurant_details)
        except:
            pass
    def data(self):
        db=self.db
        print("Documents in Mongodb")
        print("restaurants")
        print(db.Restaurants.count_documents({}))
        print("cities")
        print(db.Cities.count_documents({}))
        
class PGSQL:
    '''To insert data into Postgresql'''
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            database="swiggdb",
            user="postgres",
            password="root"
        )
        query = 'CREATE TABLE IF NOT EXISTS citydat(cityId SERIAL PRIMARY KEY, CityName VARCHAR(50), CityUrl VARCHAR(200))'
        cur = self.con.cursor()
        cur.execute(query)
        print("table created")
        query = "CREATE TABLE IF NOT EXISTS restaurant_dat(rest_Id SERIAL PRIMARY KEY, city_name VARCHAR(50), rest_Name VARCHAR(50), rest_Url VARCHAR(200), cuisine VARCHAR(100), ratings VARCHAR(5), cost_for_two VARCHAR(50), discount INTEGER, coupon VARCHAR(20))"
        cur = self.con.cursor()
        cur.execute(query)
        print("restaurant table created")
        
    def city_insert(self, ctname, cturl):
        query = f"INSERT INTO citydat(CityName, CityUrl) VALUES ('{ctname}', '{cturl}')"
        cur = self.con.cursor()
        try:
            cur.execute(query)
        except:
            pass
        self.con.commit()
        
        
    def rest_insert(self, lst):
        '''[city name, restaurant name, rest url, cuisine, ratings, cost for two, discount, coupon]'''
        query = f"INSERT INTO restaurant_dat(city_name, rest_name, rest_url, cuisine, ratings, cost_for_two, discount, coupon) VALUES ('{lst[0]}', '{lst[1]}', '{lst[2]}', '{lst[3]}', '{lst[4]}', '{lst[5]}', '{lst[6]}', '{lst[7]}')"
        cur = self.con.cursor()
        try:
            cur.execute(query)
        except:
            pass
        self.con.commit()
        
        
    def data(self):
        cur=self.con.cursor()
        print("rows in postgresql")
        print("restaurants")
        cur.execute('SELECT COUNT(*) FROM restaurant_dat')
        count=cur.fetchone()[0]
        print(count)
        print("cities")
        cur.execute('SELECT COUNT(*) FROM citydat')
        count=cur.fetchone()[0]
        print(count)
        
        