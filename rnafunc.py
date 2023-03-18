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
            
    five=cities[:5]
    print(five)
    rlinks=[]
    fp=swiggyscrape.Folder()
    for name in five:
        clinks=[]
        file1=fp.getdbfile("links",name)
        with open(file1 ,'r',encoding='utf-16') as file:
            for line in file:
                clinks.append(line.strip())
        rlinks.append(clinks[:10])
    return rlinks

def citynames():
    bity=[]
    with open('city.csv','r',encoding='utf-8') as file1:
        for line in file1:
            cty=line.rfind('/')
            mity=line[cty+1:-1]
            nity=mity.capitalize()
            bity.append(nity)
    return bity[:5]




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
    with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(menu, crlink, [city_name]*len(crlink))
            executor.shutdown(wait=True)
            
    timee=time.time()
    print("time taken for 10 per city restaurants when data csv exists: = ", timee-times)
    




if __name__=="__main__":
    resit=difflinks()
    cityn=citynames()
    
    print(len(resit),len(cityn))
    times=time.time()
    num_processes = cpu_count()  # Get the number of CPU cores available on the system
    print(f"Running {num_processes} processes in parallel...")
    

    with Pool(num_processes) as w:
        #w=mp.Pool()
        w.starmap(mpmenu,[(resit[_],cityn[_]) for _ in range(len(resit))])
    
    # w.close()
    # w.join()
    
    timee=time.time()
    runtime=timee-times
    print("time taken for 50 restaurants : = ", timee-times)
    
    with open("data.csv",'a') as file:
        if(runtime<50):
            file.write(f"Pool {num_processes} and ThreadPoolExecutor(max_workers=5) time taken to check {len(resit)*len(resit[0])} csv files== {runtime} secs \n")
        else:
            file.write(f"Pool {num_processes} and ThreadPoolExecutor(max_workers=5) time taken to create {len(resit)*len(resit[0])} csv files== {runtime} secs \n")
    

        

    
    


