'''To delete and count restaurants in menus while testing
    To add functionality to locate and delete files with no data'''
import os
import shutil

def delcsv(nity):
    for name in nity:
        delpath=f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{name}/menus"
        if os.path.exists(delpath):
            print(f"deleting {delpath}")
            #os.removedirs(delpath)
            shutil.rmtree(delpath)
            print("Folder deleted")
        else:
            print("Path does not exists")
            
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
        

# Use len() to get the number of files in the list

    
def delfunc(x):
    bity=[]
    with open('city.csv','r',encoding='utf-8') as file1:
        for line in file1:
            cty=line.rfind('/')
            mity=line[cty+1:-1]
            nity=mity.capitalize()
            bity.append(nity) 

    print(bity[:9])
    nity=bity[:8]
    if x==1:
        countcsv(nity)
    else:
        delcsv(nity)

#delfunc(2)
