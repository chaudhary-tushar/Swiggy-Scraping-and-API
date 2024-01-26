import requests
import os
from bs4 import BeautifulSoup
from classes import folders as folds


class City:

    def city(self, url):
        fp = folds.Folder()
        folder_path = fp.get_folder()
        file_name = "city.csv"
        file_path = f"{folder_path}/{file_name}"
        city_links = []
        city_names = []

        if os.path.isfile(file_path):

            with open(file_path, 'r', encoding='utf-8') as file1:

                for line in file1:

                    if line not in city_links:

                        city_links.append(line[:-1])
                        ind = line.rfind('/')
                        line = line[ind+1:]
                        city = line.replace("\n", "")
                        city = city.capitalize()
                        city_names.append(city)
            print("File exists in the folder.")

        else:
            headers = {"User-Agent": "Mozilla/5.0 "
                       "(Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.3"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a')

            with open(file_path, 'w', encoding='utf-8') as file1:

                for link in links:

                    if (link.get('href') is not None and
                       link.get('href')[0:5] == "/city" and
                       link.get('href')[-11:] != "restaurants"):
                        lkd = url + link.get('href')

                        if lkd not in city_links:

                            file1.write(lkd + '\n')
                            city_links.append(lkd)
                            ind = lkd.rfind('/')
                            line = lkd[ind+1:]
                            city = line.replace("\n", "")
                            city = city.capitalize()
                            city_names.append(city)

            print(f"{file_name} is created in {folder_path}")

        return city_links, city_names
