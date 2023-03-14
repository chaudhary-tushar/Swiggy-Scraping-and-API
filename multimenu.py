#this function is trial for multiprocessing different restaurants in a city 
#ideal number of restaurants is taken as 5 
#this is a copy of swiggy.py w/o the function


import sleswig as sw
import os
import multiprocessing as mp


res_links=[]
def make_list():
    file_path_ahem='C:/Users/tusha/Desktop/vscode/SWIGGY/text_files/restaurants_links_Ahmedabad.txt'
    with open(file_path_ahem,'r',encoding='utf-16') as filea:
        for line in filea:
            print(line)
            res_links.append(line)
    print(len(res_links))


def menu(urq):
    url=urq 
    nameind=urq.rfind('/')
    name=urq[nameind+1:nameind+15]
    print(name)
    
    divs = sw.perres(url)[1:-1]
    cnt=0
    # Loop through each div and find all the paragraphs with class 'my-class'
    folder_path='C:/Users/tusha/Desktop/vscode/SWIGGY/text_files/city_res_menus'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) 
    file_path=folder_path+'/'+ f"restaurant_{name}.txt"

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
                cnt+=1
                
    print(cnt)
    
if __name__== "__main__":
    make_list()
    for i in range(len(res_links)):
        five=res_links[i:i+15]
        i+=15
        processes=[]
        
        for inp in five:
            p=mp.Process(target=menu, args=(inp,))
            processes.append(p)
            p.start()
            
        for p in processes:
            p.join()