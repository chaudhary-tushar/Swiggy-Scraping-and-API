import os
import sys

fp='C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files'
cities=os.listdir(fp)[4:10]
for city in cities:
    flpath=os.path.join(fp,city)
    menpath=os.path.join(flpath,"menus")
    mens=os.listdir(menpath)
    if len(mens)<2:
        print("golmaal h bhai sab golmaal h")
    # resname=[]
    # for resnam in mens:
    #     resname.append(resnam[11:-4])
    # checkar=[]
    # with open(f"{flpath}/restaurant_links_{city}.csv",'r',encoding='utf-16') as file1:
    #     lines=file1.readlines()
    #     for line in lines:
    #         naem=line.rfind('/')
    #         name=line[naem+1:naem+20]
    #         checkar.append(name)
    # for menu in resname:
    #     if menu not in checkar:
    #         print(f"problem here {city}")
    #         print(menu)
    #         sys.exit()       
    # print("no problem here")
    