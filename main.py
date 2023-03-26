'''This file exists during the development process of making a web scraper
    Takes multiple imports from defined function file like menu_builder.py and restaurant finder.py'''
from selenium import webdriver
import time
import multiprocessing as mp
import requests
from bs4 import BeautifulSoup
import restaurant_finder
from concurrent.futures import ThreadPoolExecutor
cities=[]

#below function works like city.py // basically builds the file and array containing the links of different cities swiggy page
#there are total around 598 cities listed in swiggy servicable areas
def makelist():
    url="https://www.swiggy.com"
    response=requests.get(url)
    soup=BeautifulSoup(response.content,'html.parser')
    links=soup.find_all('a')
    with open("city.csv",'w',encoding='utf-8') as file1:
        for link in links:
            if(link.get('href')!=None and link.get('href')[0:5]=="/city"  ):
                lkd=url+link.get('href')
                if lkd not in cities:
                    file1.write(lkd+'\n')
                    cities.append(lkd)
                
#the below function main calls the restaurant finder file and builds the file and list of restaurants links for every city.
#It uses multiprocessing to fasten the process and for test purposes another list is made from cities[] containing 5-10 elements/links
#it also prints time taken by code                  
        
if __name__=="__main__":
    makelist()
    print(len(cities))
    print("*******======*******")
    
    times=time.time()
    five=cities[:1]
    
    
    
    ##########mp using threadpool###############
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(restaurant_finder.reslist, five)
        executor.shutdown(wait=True)
    
    
    ########### mp using pooling ############
    # p=mp.Pool()
    # p.map(restaurant_finder.reslist,five)
    
    
    
    ######### mp using mp.process############
    # for i in range(0,20,5):
        
    #     # five=cities[i:i+5]
    #     # processes=[]
        
    #     # for inp in five:
    #     #     p=mp.Process(target=restaurant_finder.reslist, args=(inp,))
    #     #     processes.append(p)
    #     #     p.start()
            
    #     # for p in processes:
    #     #     p.join()
        
    timee=time.time()
    print("time taken to parse 5 restaurants using pooling",timee-times)