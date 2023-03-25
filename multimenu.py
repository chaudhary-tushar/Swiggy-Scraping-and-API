'''
this function is trial for multiprocessing different restaurants in a city 
ideal number of restaurants is taken as 5 
this is a copy of swiggy.py w/o the function
this file contains 4 different types of parallel computing algorithm namely:-
    processes=[] , p=mp.process : time for creating 10 for each 10 = 840 secs, iterating = 400 secs
    pooling , pool.starmap()  : time for creating 10 for each 10 = 350 secs , iterating = 9.335 secs
    threading , ThreadPoolExecutor as executor : time for creating 10 for each 10 =305 secs, iterating= 0.05 secs'''


import div_finder as sw
import os
import multiprocessing as mp
import time
from concurrent.futures import ThreadPoolExecutor
#import tensorflow as tf



def make_list(res_links,cname):
    file_path_vary=f'C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{cname}/restaurant_links_{cname}.csv'
    with open(file_path_vary,'r',encoding='utf-16') as filea:
        for line in filea:
            #print(line)
            res_links.append(line)
    #print(cname,len(res_links))
    return res_links



def menu(urq,cname):
    url=urq
    # url=ar[0]
    # urq=ar[0]
    # cname=ar[1] 
    nameind=urq.rfind('/')
    name=urq[nameind+1:nameind+20]
    #print(name)
    
    #divs = sw.perres(url)[1:-1]
    
    
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
        divs = sw.perres(url)[1:-1]
        with open(file_path,'w',encoding='utf-8') as file1:
            for div in divs:
                #print()
                #print(div.get('id'))
                file1.write('\n'+div.get('id')+'\n'+'\n')
                #print()
                paragraphs = div.find_all('p', {'class': 'ScreenReaderOnly_screenReaderOnly___ww-V'})
                #print()
                
                # Loop through the paragraphs and print their text content
                for paragraph in paragraphs:
                    file1.write(paragraph.text+'\n')
                    #print(paragraph.text)
                
                
    
    
    
if __name__== "__main__":
    #here lies two ways to multiprocess , pooling is better
    time1=time.time()
    bity=[]
    with open('city.csv','r',encoding='utf-8') as file1:
        for line in file1:
            cty=line.rfind('/')
            mity=line[cty+1:-1]
            nity=mity.capitalize()
            #print(nity)
            bity.append(nity)
       
    city=bity[0:5]   ###array of city names
    time2=time.time()
    runtime=time2-time1
    print(city)
    print(f"Time taken to make array of city names :{runtime} ")
    
    timeS=time.time()
    lenlinks=0
    for j in range(len(city)):
        time3=time.time()
        restaurants=[]  ### array of links
        restaurants=make_list(restaurants,city[j])
        time4=time.time()
        runtim=time4-time3
        print(f"time taken to make lists of all the restaurants of {city[j]} : {runtim}")
        time5=time.time()
        #for i in range(0,10,5):
        # five = [[1 for j in range(2)] for i in range(10)]
        # for q in range(10):
        #     five[q][0]=restaurants[q]
        #     five[q][1]=city[j]
        # print(five)
        five=restaurants[20:30]
        lenlinks=len(five)
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(menu, five, [city[j]]*len(five))
            executor.shutdown(wait=True)
        
        #print(i)
        
        
        # p=mp.Pool()
        # p.starmap(menu,[(five[_],city[j]) for _ in range(len(five))])
        
        
        # processes=[]
        
        # for inp in five:
        #     p=mp.Process(target=menu, args=(inp,city[j],))
        #     processes.append(p)
        #     p.start()
            
        # for p in processes:
        #     p.join()
        time6=time.time()
        runti=time6-time5
        print(f"Time taken to iterate through 10 restaurants for creating/checking csv :{runti} ")
        del restaurants
        del five
        
    timeE=time.time()
    runtimez=timeE-timeS
    print(f"total runtime for 10 restaurants for each of the 10 cities for creating/checking in csv  : {runtimez}")
    # with open("data.csv",'a') as file:
    #     file.write(f"Using for loop and ThreadPoolExecutor(max_workers=10) time taken to store {len(city)*lenlinks} == {runtimez} secs \n")

    with open("data.csv",'a') as file:
        if(runtime<50):
            file.write(f"Using for loop and ThreadPoolExecutor(max_workers=10) time taken to check {len(city)*lenlinks} csv files == {runtimez} secs \n")
        else:
            file.write(f"Using for loop and ThreadPoolExecutor(max_workers=10) time taken to create {len(city)*lenlinks} csv files == {runtimez} secs \n")