import requests
import bs4
import sleswig as sw
import os

def diffres(url,name,cname):

    divs = sw.perres(url)[1:-1]
    cnt=0
    # Loop through each div and find all the paragraphs with class 'my-class'
    folder_path='C:/Users/tusha/Desktop/vscode/SWIGGY/text_files/menus'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) 
    file_path=folder_path+'/'+ f"{cname}_{name}.txt"
    
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
