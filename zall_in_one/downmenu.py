from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
import csv, os, sys
import multiprocessing as mp
import time
import shutil


def linksTo_name(details_path):
    city_set = set()
    with open(details_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                link = row[1].strip()
                nameind=link.rfind('/')
                name=link[nameind+1:nameind+20]
                det_name = f"restaurant_{name}.csv"
                city_set.add(det_name)
    return city_set

def link_to_name(details_path):
    city_set = {}
    with open(details_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                link = row[1].strip()
                nameind=link.rfind('/')
                name=link[nameind+1:nameind+20]
                det_name = f"restaurant_{name}.csv"
                city_set[det_name] = link
    return city_set

class Sel_Driver:
    """This class returns the initialized selenium driver"""

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--log-level=3')
        options.add_argument('--headless')
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-javascript")
        options.binary_location = "C:/Users/tusha/AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe"  # noqa
        options.add_argument("--disable-animations")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_driver_path = "C:/Users/tusha/Desktop/vscode/SWIGGY/driver/chromedriver.exe"
        service = Service(executable_path=chrome_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)

    def get_driver(self):

        return self.driver

    def get_page_source(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        return self.driver.page_source


class DivFinder:
    def div_finder(self, html):

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html, 'lxml')
        p_elements = soup.find_all('p', class_='ScreenReaderOnly_screenReaderOnly___ww-V', tabindex=0) # noqa
        if len(p_elements) == 0:
            return None, None
        p_element = p_elements[0]

        # Find all the divs on the page with class 'my-class'
        specific_div = soup.find('div', class_='nDVxx')
        divs = specific_div.find_all('div')

        dids = []
        for div in divs:
            div_id = div.get('id')
            if div_id:
                dids.append(div)
        return p_element, dids



class MenuBuilder:
    '''This class builds the menus of different restaurant
    and stores it in /txt_files/city/menus/*'''

    def menu(self, res_info, divs, file_path):
        '''This function takes arguments as url and city name
        but is called by inbuilt class function mpmenu'''

        

        with open(file_path, 'w', encoding='utf-8') as file1:

            file1.write(res_info.text + '\n')
            for div in divs:
                file1.write('\n'+div.get('id')+'\n'+'\n')
                paragraphs = div.find_all('p', {'class': 'ScreenReaderOnly_screenReaderOnly___ww-V'})   # noqa

                # Loop through the paragraphs and print their text content
                for paragraph in paragraphs:
                    file1.write(paragraph.text.strip().replace('\n', '') + '\n')
    

    def mp_menu(self, lurls):
        '''This function takes a list of urls and calls menu function'''
        driver_init = Sel_Driver()
        div = DivFinder()
        print(len(lurls))
        for url in lurls:
            urq = url
            nameind = urq.rfind('/')
            name = urq[nameind+1:nameind+20]
            f_name = f"restaurant_{name}.csv"
            fp = "C:/Users/tusha/Desktop/vscode/SWIGGY/zall_in_one/menus"
            file_path = os.path.join(fp, f_name)
            if os.path.isfile(file_path):
                
                # print(f"{file_path} File exists!")
                continue
            else:
                html = driver_init.get_page_source(url)
                res_info, divs = div.div_finder(html)
                if res_info == None:
                    continue
                self.menu(res_info, divs, file_path)
        driver_init.driver.quit()


def migrate():
    og_folder = "C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    temp_folder = "C:/Users/tusha/Desktop/vscode/SWIGGY/zall_in_one/menus"
    tmp_menus = os.listdir(temp_folder)
    tmp_dict = {}
    for menu in tmp_menus:
        tmp_dict[menu] = os.path.join(temp_folder,menu)
    count = 0
    cities = os.listdir(og_folder)
    for city  in cities:
        file_path = os.path.join(og_folder, city, f"restaurant_det_links_{city}.csv")
        got_set = set(linksTo_name(file_path))
        menu_path = os.path.join(og_folder, city, "menus")
        for key,value in tmp_dict.items():
            if key in got_set:
                count+=1
                shutil.copy(tmp_dict[key],menu_path)
    return count


if __name__ == "__main__":
    url_list = []
    with open('missngres.csv', 'r',encoding='utf-8') as file:
        lines = file.readlines()
        temp = []
        for line in lines[:801]:
            if len(temp)==200:
                url_list.append(temp)
                temp = []
            line = line.strip()
            temp.append(line)
        file.close()
    print(len(url_list))
    num_processes = 4
    MB = MenuBuilder()
    with Pool(num_processes) as pool:
        pool.starmap(MB.mp_menu, [(arr,) for arr in url_list])

    print(migrate())
    # MB = MenuBuilder()
    # MB.mp_menu(url_list)

