import os
import pandas as pd
import sys
import string
import re 

class Menu_Obj:
    def __init__(self):
        self.item_name = ""
        self.item_type = ""
        self.item_cid = ""
        self.cost = 0
        self.description = ""
        self.customization = False
        self.bestseller = False
        self.city_name = ""
        self.rest_url_link = ""


def get_name(line):
    start_marker = "Veg Item. " if line.startswith('Veg Item') else "Non-veg item."
    end_marker = ". This" if ('This item is a Bestseller' in line) else ". Costs:" 
    start_pos = line.find(start_marker)
    end_pos = line.find(end_marker)
    flag = False
    # Extract the substring
    if start_pos != -1 and end_pos != -1:
        extracted_substring = line[start_pos + len(start_marker):end_pos].strip()
        flag =True
    # print(len(extracted_substring))
    if flag:
        return extracted_substring
    else:
        print(line)
        sys.exit()


def get_discription(line):
    if not ('Descrition' in line):
        return None
    start_marker = "Description: "
    end_marker = "Swipe"
    start_pos = line.find(start_marker)
    end_pos = line.find(end_marker)
    if start_pos != -1 and end_pos != -1:
        extracted_substring = line[start_pos + len(start_marker):end_pos].strip()
    
    return extracted_substring
    


def maker():
    mahabaliar = []
    fpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    cities=os.listdir(fpath)
    cost_pattern = r'Costs: (\d+(?:\.\d+)?) rupees'
    for city in cities[:25]:
        file_path=f"{fpath}/{city}/restaurant_det_links_{city}.csv"
        df=pd.read_csv(file_path)
        linkd=df['Links']
        for link in linkd:
            inde=link.rfind("/")
            menname=link[inde+1:inde+20]
            menuname=f"{fpath}/{city}/menus/restaurant_{menname}.csv"
            if os.path.isfile(menuname):
                # print(menuname)
                with open(menuname,'r',encoding='utf-8') as file:
                    
                    lines=file.readlines()
                    section=""
            
                    i=0
                    for i  in range(len(lines)):
                        if lines[i].startswith("cid"):
                            section=lines[i].replace("cid-","").rstrip("\n")
                            break
            
                    for i in range(i,len(lines)):
                        if  not(lines[i].startswith("Veg ") or lines[i].startswith("Non-") or lines[i].startswith("cid")) :
                            continue
                        if lines[i].startswith("cid"):
                            section=lines[i].replace("cid-","").strip()
                            continue 
                        menuObj = Menu_Obj()
                        cost_match = re.search(cost_pattern, lines[i])
                        if cost_match:
                            menuObj.cost = int(float(cost_match.group(1)))
                        else:
                            print(menuname,'\n',lines[i])
                            sys.exit()
                        city=city.translate(str.maketrans("", "", string.punctuation))
                        menuObj.city_name = city
                        menuObj.rest_url_link = link
                        
                        type="Veg" if lines[i].startswith('Veg') else "Non-Veg"
                        type=type.translate(str.maketrans("", "", string.punctuation))
                        menuObj.item_type = type
                        section=section.translate(str.maketrans("", "", string.punctuation))
                        menuObj.item_cid = section
                        bestseller= True if "Bestseller" in lines[i] else False
                        menuObj.bestseller = bestseller
                        menuObj.customization = True if "customizable" in lines[i] else False

                        menuObj.item_name = get_name(lines[i])
                        if len(menuObj.item_name) > 150:
                            print(menuname)
                            print(lines[i])
                        
                        
                        description = get_discription(lines[i])
                        menuObj.description = description
                        
                        
                        
                        mahabaliar.append(menuObj)
    print(len(mahabaliar))
    return mahabaliar
                

                
                    
                    
                    
                
    