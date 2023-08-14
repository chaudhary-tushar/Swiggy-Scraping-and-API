'''to get the links of different cities in city.csv'''
import requests
from bs4 import BeautifulSoup

url="https://www.swiggy.com"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
response=requests.get(url,headers=headers)
print(response.content)
soup=BeautifulSoup(response.content,'html.parser')
links=soup.find_all('a')
print(links)
with open("city.csv",'w',encoding='utf-8') as file1:
    for link in links:
        if(link.get('href')!=None and link.get('href')[0:5]=="/city"  ):
            lkd=url+link.get('href')
            file1.write(lkd+'\n')
            print(lkd)  