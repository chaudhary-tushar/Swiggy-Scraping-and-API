import os
import shutil

fileswig="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
filedesk="C:/Users/tusha/Desktop/txt_files"

count=0
deskv=os.listdir(filedesk)
swigv=os.listdir(fileswig)
for i in range(len(deskv)):
    if(deskv[i]==swigv[i]):
        dmenp=f"C:/Users/tusha/Desktop/txt_files/{deskv[i]}/menus"
        if (os.path.isdir(dmenp)==False):
            print(f"{deskv[i]} menus not copied")
            continue
        smenp=f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{swigv[i]}/menus"
        if os.path.exists(smenp):
            dmen=os.listdir(dmenp)
            smen=os.listdir(smenp)
            for j in range(len(dmen)):
                if(dmen[j] not in smen[j]):
                    source=os.path.join(dmenp,dmen[j])
                    destination=os.path.join(smen,dmen[j])
                    shutil.copyfile(source,destination)
                    count+=1
        else:
            dmenp=f"C:/Users/tusha/Desktop/txt_files/{deskv[i]}/menus"
            smenp=f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{swigv[i]}/"
            shutil.copytree(dmenp,os.path.join(smenp,os.path.basename(dmenp)))
            
                
        
    
print(f"{count} files copied to swiggy") 
