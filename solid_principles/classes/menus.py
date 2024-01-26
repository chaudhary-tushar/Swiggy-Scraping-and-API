import os
from classes import seldriver as sd
from classes import folders as fols
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class DivFinder:
    def div_finder(self, url):
        Driver = sd.Sel_Driver()
        html = Driver.get_page_source(url)

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html, 'lxml')
        p_elements = soup.find_all('p', class_='ScreenReaderOnly_screenReaderOnly___ww-V', tabindex=0) # noqa
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

    def menu(self, urq, cname):
        '''This function takes arguments as url and city name
        but is called by inbuilt class function mpmenu'''

        url = urq
        nameind = urq.rfind('/')
        name = urq[nameind+1:nameind+20]
        fp = fols.Folder()
        file_path = fp.getmenudb(cname, name)
        if os.path.isfile(file_path):
            print(f"{file_path} File exists!")
            return

        else:
            print(f"{file_path} does not exists")
            DI = DivFinder()
            res_info, divs = DI.div_finder(url)

            with open(file_path, 'w', encoding='utf-8') as file1:

                file1.write(res_info.text + '\n')
                for div in divs:
                    file1.write('\n'+div.get('id')+'\n'+'\n')
                    paragraphs = div.find_all('p', {'class': 'ScreenReaderOnly_screenReaderOnly___ww-V'})   # noqa

                    # Loop through the paragraphs and print their text content
                    for paragraph in paragraphs:
                        file1.write(paragraph.text.strip().replace('\n', '') + '\n')

    def mpmenu(self, crlink, city_name):
        '''This function takes argument as links array and
        city_name and calls menu function parallely'''

        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.menu, crlink, [city_name]*len(crlink))
            executor.shutdown(wait=True)
