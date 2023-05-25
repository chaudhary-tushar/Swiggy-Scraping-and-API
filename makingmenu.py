import os
import pandas as pd
import sys
import string

mahabaliar=[]
def maker():
    fpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    cities=os.listdir(fpath)[:1]
    for city in cities:
        file_path=f"{fpath}/{city}/restaurant_det_links_{city}.csv"
        df=pd.read_csv(file_path)
        linkd=df['Links']
        for link in linkd:
            inde=link.rfind("/")
            menname=link[inde+1:inde+20]
            menuname=f"{fpath}/{city}/menus/restaurant_{menname}.csv"
            if os.path.isfile(menuname):
                print(menuname)
                
                with open(menuname,'r',encoding='utf-8') as file:
                    
                    lines=file.readlines()
                    section=""
                    getname=lines[3]
                    nameind=getname.rfind(":")
                    name=getname[nameind+2:].rstrip("\n")
                    resname=name.replace(",","")
            
                    i=8
                    for i  in range(len(lines)):
                        if lines[i].startswith("cid"):
                            section=lines[i].replace("cid-","").rstrip("\n")
                            break
            
                    for i in range(i,len(lines)):
                        if len(lines[i])<=5 or not(lines[i].startswith("Veg ") or lines[i].startswith("Non-") or lines[i].startswith("cid")) :
                            continue
                        perres=[]
                        city=city.translate(str.maketrans("", "", string.punctuation))
                        perres.append(city)
                        resname=resname.translate(str.maketrans("", "", string.punctuation))
                        perres.append(resname)
                        perres.append(link)
                        if lines[i].startswith("cid"):
                            section=lines[i].replace("cid-","")
                            continue 
                        type="Veg" if lines[i].startswith('Veg') else "Non-Veg"
                        
                        
                        perar=lines[i].split(".")
                        
                        item_name=perar[1].strip()
                        item_name=item_name.translate(str.maketrans("", "", string.punctuation))
                        perres.append(item_name)
                        type=type.translate(str.maketrans("", "", string.punctuation))
                        perres.append(type)
                        section=section.translate(str.maketrans("", "", string.punctuation))
                        perres.append(section)
                        det=perar[2]
                        costind=det.find(":")
                        costlind=det.find("rupees")
                        cost=det[costind+2:costlind]
                        cost=cost.translate(str.maketrans("", "", string.punctuation))
                        perres.append(cost)
                        customizability="" 
                        if "customizable" in det:
                            customizability="Yes"
                            if "Description" in det:
                                descind=det.find("Description:")
                                desclind=det.find("This")
                                description=det[descind+12:desclind]
                            else:
                                description="NONE"
                            description=description.translate(str.maketrans("", "", string.punctuation))
                            perres.append(description)
                        else:
                            customizability="No"
                            if "Description" in det:
                                descind=det.find("Description:")
                                desclind=det.find("Swipe")
                                description=det[descind+12:desclind]
                            else:
                                description="NONE"
                            description=description.translate(str.maketrans("", "", string.punctuation))
                            perres.append(description)
                        customizability=customizability.translate(str.maketrans("", "", string.punctuation))
                        perres.append(customizability)
                        bestseller="Yes" if "Bestseller" in det else "No"
                        bestseller=bestseller.translate(str.maketrans("", "", string.punctuation))
                        perres.append(bestseller)
                        mahabaliar.append(perres)
    with open("menudbmngdb.csv",'w',encoding='utf-8') as file0:
        for item in mahabaliar:
            file0.write(f"{len(item)} : {item}\n")
    return mahabaliar
                

                
                    
                    
                    
                
    