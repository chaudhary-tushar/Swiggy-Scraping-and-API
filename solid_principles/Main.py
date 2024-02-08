'''This is the main file which calls swiggyscrape functions and classes'''
from classes import (
    city, folders,
    restaurants, menus,
    workers
)
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
import time
from datetime import datetime
import sys


def remcity(namelist, urllist, name):
    '''This function takes city names,url names and cities to remove'''
    name = name.capitalize()
    index = namelist.index(name)
    namelist.pop(index)
    urllist.pop(index)
    return namelist, urllist


if __name__ == "__main__":
    timestart = time.time()
    url = "https://www.swiggy.com"

    x, y = 0, -1
    city1 = city.City()
    city = city1.city(url)
    city_url_list = city[0]
    city_name_list = city[1]
    city_names = city_name_list
    print("appending total cities = ", len(city_names))
    five = city_url_list
    print(five)
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # rf = restaurants.Restaurant_finder()
    # times = time.time()

    # num_processes1 = cpu_count()
    # print(f"Running {4} processes in parallel...")

    # # with Pool(4) as p:
    # #     results=p.map(rf.rest_list,five)
    # # redcity = list(filter(lambda x: x is not None, results))

    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     results = list(executor.map(rf.rest_list, five))
    # redcity = list(filter(lambda x: x is not None, results))
    # timee = time.time()
    # runtimez = timee-times
    # with open("atad.csv", 'a', encoding='utf-8') as fileq:
    #     fileq.write(f"Ran ON : {date_time}\nRan with 4 cores\n")
    #     fileq.write(f"time taken to parse {len(five)} cities is {runtimez}\n")
    #     for names in redcity:
    #         fileq.write(names + " , ")
    #     fileq.write(str(len(redcity))+"\n")
    #     fileq.close()

    # print(redcity)

    # if (len(redcity) != 0):
    #     for citi in redcity:
    #         city_names, five = remcity(city_names, five, citi)

    print(city_names)
    metric = workers.Metrics()
    start_csv = metric.countcsv()
    pre = folders.Multi_res_links()
    city_res_links = pre.get_links(city_names)
    print("*******======*******")
    tot_count = 0
    for i in range(len(city_res_links)):
        tot_count += len(city_res_links[i])
    print(tot_count)

    # calling multiprocessing menu builder this call nested multiprocessing #

    TIMES = time.time()
    menu = menus.MenuBuilder()
    # ################ POOLING##############

    num_processes = cpu_count()
    with Pool(num_processes) as w:
        w = mp.Pool()
        w.starmap(menu.mpmenu, [(city_res_links[_], city_names[_])
                                for _ in range(len(city_res_links))])

    # ##########THREADING###########

    # with ThreadPoolExecutor(max_workers=8) as executor:
    #             executor.map(menu.mpmenu, city_res_links,city_names)
    #             executor.shutdown(wait=True)
    

    end_csv = metric.countcsv()
    menu_dict = metric.menus_5608_dict()
    print(metric.count_copied_menus(menu_dict))
    print(f"csv count changed from {start_csv} to {end_csv} \nNew files added = {end_csv-start_csv}")
    sys.exit()

    Arrays = ss.restArr()
    carr = Arrays.city_makearr()
    rarr = Arrays.rest_makear()

    Msql = ss.MSQL()
    Mngdb = ss.MNGDB()
    Pgdb = ss.PGSQL()

    for i in range(len(carr)):
        Msql.city_insert(carr[i][1], carr[i][2])
        Mngdb.city_insert(carr[i][1], carr[i][2])
        Pgdb.city_insert(carr[i][1], carr[i][2])
    for i in range(len(rarr)):
        Msql.rest_insert(rarr[i])
        Mngdb.rest_insert(rarr[i])
        Pgdb.rest_insert(rarr[i])

    Msql.data()
    Mngdb.data()
    Pgdb.data()

    TIMEE = time.time()
    runtime = TIMEE-TIMES
    timeend = time.time()
    runTIME = timeend-timestart
    with open('data.csv', 'a', encoding='utf-8')as file0:
        file0.write("time taken from start to end for " +
                    f"{len(city_res_links)*len(city_res_links[0])} " +
                    f"restaurants is = {runtime}\n")
        file0.write("time taken for parsing and building menu is of " +
                    f"{len(city_names)} cities and {tot_count} " +
                    f"restaurants is = {runTIME}\n\n")
        file0.close()
