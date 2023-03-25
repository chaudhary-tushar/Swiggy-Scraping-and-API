'''This is the main file which calls swiggyscrape functions and classes'''
import swiggyscrape as ss
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
import restaurant_finder as rf
import time
from datetime import datetime



if __name__=="__main__":
    timestart=time.time()
    url="https://www.swiggy.com"

    city1=ss.City()
    city=city1.city(url)
    city_url_list=city[0]  ###array of url links
    city_name_list=city[1] ###array of city names
    city_names=city_name_list[500:]  #changed from 5 to 9
    # city_names.extend(city_name_list[11:16])
    print("appending total cities = ",len(city_names))

    five=city_url_list[500:]  ### changed from 5 to 9
    # five.extend(city_url_list[11:16])
    print(len(five))
    print(city_names)
    print(five)
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    
    #########initializing rf as class for finding restaurant###########
    print(city_names)
    rf=ss.Restaurant_finder()
    times=time.time()

    num_processes1 = cpu_count()
    print(f"Running {num_processes1} processes in parallel...")
    with Pool(num_processes1) as p:
        results=p.map(rf.rest_list,five)
    redcity = list(filter(lambda x: x is not None, results))
    
    timee=time.time()
    runtimez=timee-times
    with open("data.csv",'a',encoding='utf-8') as fileq:
        fileq.write(f"Ran ON : {date_time}\n")
        fileq.write(f"time taken to parse {len(five)} cities is {runtimez}\n")
        for names in redcity:
            fileq.write(names + " , ")
        fileq.write(str(len(redcity))+"\n")
        fileq.close()
    
    
    redcity = list(filter(lambda x: x is not None, results))
    print(redcity)
    

    # red=ss.Managelists()
    # for citi in redcity:
    #     city_names,five= red.remcity(city_names,five,citi)
            
    
    
    #######################uncomment here
    
    # pre=ss.Multi_res_links()
    # city_res_links=pre.get_links(city_names)  ###gets the 2-D array of restaurant links
    # print("*******======*******")
    # tot_count=0
    # for i in range(len(city_res_links)):
    #     tot_count+=len(city_res_links)
    # print(tot_count)
        
    ########calling multiprocessing menu builder this call nested multiprocessing#########
    # TIMES=time.time()
    # menu=ss.MenuBuilder()
    # num_processes = cpu_count()    
    # with Pool(num_processes) as w:
    #     #w=mp.Pool()
    #     w.starmap(menu.mpmenu,[(city_res_links[_],city_names[_]) for _ in range(len(city_res_links))])
        
    # TIMEE=time.time()
    # runtime=TIMEE-TIMES
    # timeend=time.time()
    # runTIME=timeend-timestart
    # with open('data.csv','a',encoding='utf-8')as file0:
    #     file0.write(f"time taken from start to end for {len(city_res_links)*len(city_res_links[0])} restaurants is = {runtime}\n")
    #     file0.write(f"time taken for parsing and building menu is of {len(city_names)} cities and {tot_count} restaurants is = {runTIME}\n\n")
    #     file0.close()
        
    