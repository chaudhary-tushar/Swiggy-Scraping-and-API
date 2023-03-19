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
    for name in nity:
        delpath=f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{name}/menus"
        if os.path.exists(delpath):
            files = os.listdir(delpath)
            num_files = len(files)
            print(num_files)
        else:
            print(f"no menu folder for {name}")

# Use len() to get the number of files in the list

    

bity=[]
with open('city.csv','r',encoding='utf-8') as file1:
    for line in file1:
        cty=line.rfind('/')
        mity=line[cty+1:-1]
        nity=mity.capitalize()
        bity.append(nity) 

print(bity[:20])
nity=bity[:20]
x=int(input("Enter choice 1 for counting 2 for deletion : "))
if x==1:
    countcsv(nity)
else:
    delcsv(nity)
    
