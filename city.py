import requests
from bs4 import BeautifulSoup

url="https://www.swiggy.com"
response=requests.get(url)
soup=BeautifulSoup(response.content,'html.parser')
links=soup.find_all('a')
with open("city.csv",'w',encoding='utf-8') as file1:
    for link in links:
        if(link.get('href')!=None and link.get('href')[0:5]=="/city"  ):
            lkd=url+link.get('href')
            file1.write(lkd+'\n')
            print(lkd)  