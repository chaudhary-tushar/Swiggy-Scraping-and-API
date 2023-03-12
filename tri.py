from selenium import webdriver
import time
import multiprocessing as mp
import requests
from bs4 import BeautifulSoup
import main
cities=[]
def makelist():
    url="https://www.swiggy.com"
    response=requests.get(url)
    soup=BeautifulSoup(response.content,'html.parser')
    links=soup.find_all('a')
    with open("city.txt",'w',encoding='utf-8') as file1:
        for link in links:
            if(link.get('href')!=None and link.get('href')[0:5]=="/city"  ):
                lkd=url+link.get('href')
                file1.write(lkd+'\n')  
                cities.append(lkd)
            
# def trial(urL): 
#     url=urL
#     print(f"opening {url}")
#     driver = webdriver.Chrome()
#     driver.get(url)
#     time.sleep(5)
#     driver.quit()
        
if __name__=="__main__":
    makelist()
    five=cities[:5]
    times=time.time()
    
    processes=[]
    
    for inp in five:
        p=mp.Process(target=main.reslist, args=(inp,))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
    
    timee=time.time()
    print(timee-times)
    # print(five)
    # times=time.time()
    # for i in five:
    #     trial(i)
        
    # timee=time.time()
    
    # print(timee-times)