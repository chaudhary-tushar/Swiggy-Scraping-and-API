'''this contains 4 functions and is called by diff.py
difflinks=returns  2-D array of restaurant links
citynames=returns array of city names
menu= outpust menu.csv of a restaurant link
mpmenu= calls menu function using multiprocessing
'''
import os
import time
import swiggyscrape
import div_finder as sw
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count

def difflinks():
    cities=[]
    with open('city.csv','r', encoding='utf-8') as file: 
        for line in file:
            ind=line.rfind('/')
            line=line[ind+1:]
            city=line.replace("\n","")
            city=city.capitalize()
            cities.append(city)
            
    five=cities[:8]
    print(five)
    rlinks=[]
    fp=swiggyscrape.Folder()
    for name in five:
        clinks=[]
        file1=fp.getdbfile("links",name)
        if os.path.isfile(file1):
            with open(file1 ,'r',encoding='utf-16') as file:
                for line in file:
                    clinks.append(line.strip())
        else: continue
        rlinks.append(clinks[:20])
    return rlinks

def citynames():
    bity=[]
    with open('city.csv','r',encoding='utf-8') as file1:
        for line in file1:
            cty=line.rfind('/')
            mity=line[cty+1:-1]
            nity=mity.capitalize()
            bity.append(nity)
    return bity[:8]




def menu(urq,cname):
    url=urq
    nameind=urq.rfind('/')
    name=urq[nameind+1:nameind+20]
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
        divs = sw.perres(url)[:-1]
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
                    
                    
def mpmenu(crlink,city_name):
    # q=mp.Pool()
    # q.starmap(menu,[(crlink[_],city_name) for _ in range(len(crlink))])
    
    # q.close()
    # q.join()
    times=time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(menu, crlink, [city_name]*len(crlink))
            executor.shutdown(wait=True)
            
    timee=time.time()
    




# def mainpy():
#     resit=difflinks()
#     cityn=citynames()
#     tot_count=0
#     for i in range(len(resit)):
#         tot_count+=len(resit[i])
#     print(tot_count)
#     print(len(resit),len(cityn))
#     print(cityn)
#     times=time.time()
#     num_processes = 4 # Get the number of CPU cores available on the system
#     print(f"Running {num_processes} processes in parallel...")
    

#     with Pool(num_processes) as w:
#         #w=mp.Pool()
#         w.starmap(mpmenu,[(resit[_],cityn[_]) for _ in range(len(resit))])
    
#     # w.close()
#     # w.join()
    
#     timee=time.time()
#     runtime=timee-times
#     print("time taken for 50 restaurants : = ", timee-times)
    
#     with open("processing_data.csv",'a') as file:
#         if(runtime<50):
#             file.write(f"\n\nPool {num_processes} and ThreadPoolExecutor(max_workers=5) time taken to check {tot_count} csv files== {runtime} secs \n")
#         else:
#             file.write(f"Pool {num_processes} and ThreadPoolExecutor(max_workers=10) time taken to create {tot_count} csv files== {runtime} secs \n")
#         file.close()

