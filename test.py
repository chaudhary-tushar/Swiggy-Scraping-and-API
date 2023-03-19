import swiggyscrape as ss
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
import restaurant_finder as rf
import time

if __name__=="__main__":
    TIMES=time.time()
    url="https://www.swiggy.com"

    city1=ss.City()
    city=city1.city(url)
    city_url_list=city[0]  ###array of url links
    city_name_list=city[1] ###array of city names
    #print(len(city_url_list))
    city_names=city_name_list[:5]

    five=city_url_list[:5]  ### need to work for 5 city links for testing
    print(len(five))
    print(city_names)
    print(five)
    
    
    #########initializing rf as class for finding restaurant###########
    
    rf=ss.Restaurant_finder()
    times=time.time()

    num_processes1 = cpu_count()
    with Pool(num_processes1) as p:
        p.map(rf.rest_list,five)
    
    timee=time.time()
    print(timee-times)
    
    #######################uncomment here
    
    
    pre=ss.Multi_res_links()
    city_res_links=pre.get_links(city_names)  ###gets the 2-D array of restaurant links
    print("the total length of links and names is ",len(city_res_links),len(city_names))
    #print(city_res_links)
    print("*******======*******")
    for i in range(len(city_res_links)):
        print(city_res_links[i])
        print(len(city_res_links[i]))
        
        
    ########calling multiprocessing menu builder this call nested multiprocessing#########
    
    times=time.time()
    menu=ss.MenuBuilder()
    num_processes = cpu_count()    
    with Pool(num_processes) as w:
        #w=mp.Pool()
        w.starmap(menu.mpmenu,[(city_res_links[_],city_names[_]) for _ in range(len(city_res_links))])
        
    timee=time.time()
    print("time taken by main function = ",timee-times,"secs")
    TIMEE=time.time()
    runtime=TIMEE-TIMES
    with open('data.csv','a',encoding='utf-8')as file0:
        file0.write(f"time taken from start to end for {len(city_res_links)*len(city_res_links[0])} restaurants is = {runtime}\n")
        
    