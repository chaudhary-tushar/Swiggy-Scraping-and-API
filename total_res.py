'''this file is for checking the total restaurants listed linked and present at 1700 hrs'''
import os 
import csv
import time
import re

file_path="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
tup=[]
tup1=[]
tup2=[]
tup3=[]
avgt=[]
avgl=[]
def gettotal(urq):
    
    hname_ind=urq.rfind('/')        #H_name is the variable used for naming 3 files
    hname=urq[hname_ind+1:]  
    hname=hname.replace("\n","")    # Pre_name (contains only name), Restaurants_link (contains links to restaurants)
    Hname=hname.capitalize() 
    fp=f"{file_path}/{Hname}/total_restaurants_{Hname}.csv"
    if os.path.exists(fp):
        with open(fp,'r',encoding='utf-8') as file1:
            listed=0
            linked=0
            for line in file1:
                
                if "listed" in line:
                    listed=int(re.search(r'\d+', line).group())
                    avgt.append(listed)
                    tup.append(f"{Hname}={listed}")
                elif "links" in line:
                    linked=int(re.search(r'\d+', line).group())
                    avgl.append(linked)
                    tup1.append(f"{Hname}={linked}")
            tup2.append(listed-linked)
                    
    else:
        tup3.append(f"{Hname} city not listed in site")
                    
tup4=[]
def fivepmlist():
    with open('aa.csv','r')as fileq:
        for line in fileq:
            listed=int(re.search(r'\d+', line).group())
            if(listed!=0):
                tup4.append(listed)
                  
def getlinks():               
    city_links=[]                
    with open("city.csv",'r',encoding='utf-8') as file1:
        for line in file1:
            if line not in city_links:
                city_links.append(line[:-1])
    return city_links

if __name__=='__main__':
    times=time.time()
    city_links=getlinks()
    for cityrl in city_links:
        gettotal(cityrl)
    fivepmlist()               
    print(f"Average listed restaurants = {sum(avgt)/len(avgt)}")
    print(f"Average linked restaurants = {sum(avgl)/len(avgl)}")
    print(f"Average listed restaurants at 5PM = {sum(tup4)/len(tup4)}")
    timee=time.time()
    print(timee-times)
    with open('aaa.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['LISTED RESTAURANTS', 'LINKS RESTAURANTS','DIFFERENCE','5PM FILES'])
        for i in range(len(tup)):
            writer.writerow([tup[i], tup1[i],tup2[i],tup4[i]])



    

        

