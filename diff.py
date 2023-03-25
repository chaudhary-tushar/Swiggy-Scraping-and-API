'''To compute runtimes of different multiprocessing algorithms and with different configuations'''
import rnafunc
import delmenu
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor
import time
import os

if __name__=="__main__":
    for i in range(1):
        resit=rnafunc.difflinks()
        cityn=rnafunc.citynames()
        tot_count=0
        for i in range(len(resit)):
            tot_count+=len(resit[i])
        print(f" total number of restaurants is : {tot_count}")
        times=time.time()
        ##########using pooling ############
        # num_processes = cpu_count() # Get the number of CPU cores available on the system
        # print(f"Running {num_processes} processes in parallel...")
        # with Pool(num_processes) as w:
        #     w.starmap(rnafunc.mpmenu,[(resit[_],cityn[_]) for _ in range(len(resit))])
        #     w.close()
        #     w.join()
        
        ############using threading###########
        
        with ThreadPoolExecutor(max_workers=8) as executor:
                executor.map(rnafunc.mpmenu, resit,cityn)
                executor.shutdown(wait=True)
        timee=time.time()
        runtime=timee-times   
        with open("processing_data.csv",'a') as file:
            if(runtime<50):
                file.write(f"\n\nThreadPoolExecutor(max_workers=8) and ThreadPoolExecutor(max_workers=8) time taken to check {tot_count} csv files== {runtime} secs \n")
            else:
                file.write(f"ThreadPoolExecutor(max_workers=4) within ThreadPoolExecutor(max_workers=8) time taken to create {tot_count} csv files== {runtime} secs \n")
            file.close()
        
        
        delmenu.delfunc(1)
        #delmenu.delfunc(2)