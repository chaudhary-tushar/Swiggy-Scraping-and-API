'''To delete and count restaurants in menus while testing
    To add functionality to locate and delete files with no data'''
import os
import shutil

#deletes menus for testing 
def delcsv(nity):
    for name in nity:
        delpath=f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{name}/menus"
        if os.path.exists(delpath):
            print(f"deleting {delpath}")
            shutil.rmtree(delpath)
            print("Folder deleted")
        else:
            print("Path does not exists")
            
#counts menus and outputs in processing data csv         
def countcsv(nity):
    num_files=[]
    for name in nity:
        delpath=f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{name}/menus"
        if os.path.exists(delpath):
            files = os.listdir(delpath)
            num_files.append(len(files))
        else:
            print(f"no menu folder for {name}")
    with open("processing_data.csv",'a') as file:
        for i in range(len(num_files)):
            file.write(f"{num_files[i]} , ")
        file.write("\n")
        file.close()
    print(sum(num_files))
    print("Check processing_data.csv")
    
#    checks if a menu file is empty 
emp_path=[] 
def emptymenu():
    
    root_path="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    folderlist=os.listdir(root_path)
    count=0
    for name in folderlist:
        menufolder=f"{root_path}/{name}/menus"
        #print(menufolder)
        
        if os.path.exists(menufolder):
            print("true")
            filelist=os.listdir(menufolder)
            #print(filelist)
            for resname in filelist:
                file_path=f"{menufolder}/{resname}"
                if os.path.isfile(file_path):
                    file_size = os.stat(file_path).st_size
                    if file_size<100:
                        print(f"{file_path} is empty")
                        emp_path.append(file_path)
                        count+=1
    print(count)
    return emp_path
    
#checks duplicate links in restaurant links for cities in list
#def checkdups(name):
    file_path=f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{name}/restaurant_links_{name}.csv"
    count=0
    links=[]
    if os.path.isfile(file_path):
        with open(file_path,'r',encoding='utf-16') as file1:
            for line in file1:
                if line not in links:
                    links.append(line)
                else:
                    count+=1
            file1.close()
        print(f"duplicate links in {name} are {count}")
        unique=set(links)
        print(len(unique))
        if count!=0:
            testf=f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{name}/restaurant_links_{name}.csv"
            with open(testf,'w',encoding='utf-16') as file2:
                file2.writelines(unique)
# deletes empty menu from path received after running def emptymenu : called within function no need for calling explicitly
def delemp(arr):
    for path in arr:
        if os.path.exists(path):
            os.remove(path)

def delfunc(x):
    bity=[]
    with open('city.csv','r',encoding='utf-8') as file1:
        for line in file1:
            cty=line.rfind('/')
            mity=line[cty+1:-1]
            nity=mity.capitalize()
            bity.append(nity) 

    nity=bity
    if x==1:
        countcsv(nity)
    elif x==2:
        delcsv(nity)
    elif x==3:
        emptymenu()
        print(len(emp_path))       
    elif x==5:
        emptymenu()
        print(len(emp_path))
        if len(emp_path)!=0:
            delemp(emp_path)

#input 1 =counting menu files and outputs in processing data
#input 2 = deletes all menu files
#input 3 = checks if a menu file is empty or has size == 0 bytes
#input 4 = Checks if there are duplicates links in restaurant_links_{city_name}.csv
#input 5 = checks if a menu file is empty or has size == 0 bytes and deletes it

#delfunc(5)

