'''To delete and count restaurants in menus while testing
    To add functionality to locate and delete files with no data'''
import os


def get_cities_from_citycsv():
    city_csv_path = "C:/Users/tusha/Desktop/vscode/SWIGGY/city.csv"
    city_csv_arr = []
    with open(city_csv_path, 'r', encoding='utf-8') as file1:
        for line in file1:
            city_rind = line.rfind('/')
            l_city = line[city_rind+1:-1]
            u_city = l_city.capitalize()
            city_csv_arr.append(u_city)
    return city_csv_arr


def get_cities_from_dir():
    folder_path = "C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    dir_cities = os.listdir(folder_path)
    return dir_cities


class Metrics:
    """This class does not make changes, it just returns metrics from data."""
    """ # input 1 = counting menu files and outputs in processing data
        # input 2 = checks if a menu file is empty or has size == 0 bytes
        # input 3 = Checks if there are duplicates links in restaurant_links_{city_name}.csv """

    def __init__(self):
        self.city_list_from_csv = get_cities_from_citycsv()
        self.city_list_from_directory = get_cities_from_dir()
        print("Difference between count of cities from csv and director is = ",
              len(self.city_list_from_csv)-len(self.city_list_from_directory))

    def countcsv(self):
        """
        This function returns the total count of the menus in the txt_files folder.
        """
        city_list = self.city_list_from_csv
        num_files = []
        for name in city_list:
            delpath = f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{name}/menus"
            if os.path.exists(delpath):
                files = os.listdir(delpath)
                num_files.append(len(files))
            else:
                print(f"no menu folder for {name}")
        with open("processing_data.csv", 'a') as file:
            for i in range(len(num_files)):
                file.write(f"{num_files[i]} , ")
            file.write("\n")
            file.close()
        print("Check processing_data.csv")
        return sum(num_files)

    def emptymenu(self):
        """
        This functions returns the list and path of empty menu csv files.
        """
        emp_path = []
        root_path = "C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
        folderlist = os.listdir(root_path)
        count = 0
        for name in folderlist:
            menufolder = f"{root_path}/{name}/menus"
            if os.path.exists(menufolder):
                print("true")
                filelist = os.listdir(menufolder)
                for resname in filelist:
                    file_path = f"{menufolder}/{resname}"
                    if os.path.isfile(file_path):
                        file_size = os.stat(file_path).st_size
                        if file_size < 100:
                            print(f"{file_path} is empty")
                            emp_path.append(file_path)
                            count += 1
        print(count)
        return emp_path

    def total_restaurants_listed(self):
        """
        This function prints the total numbers of restaurants listed in the det_links csvs of cities
        """
        folder_path = "C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
        listed_cities = os.listdir(folder_path)
        print(f"Total listed cities are {len(listed_cities)}")
        totcnt = 0
        for city in listed_cities:
            link_path = os.path.join(folder_path, city)
            file_path = f"{link_path}/restaurant_det_links_{city}.csv"
            try:
                with open(file_path, 'r', encoding='utf-8') as file1:
                    line_count = sum(1 for line in file1)
                    totcnt += line_count-1
            except FileNotFoundError:
                print(f'File not found: {file_path}')
                continue
        print(totcnt)

    def checkdups(self):
        """Counts and removes the duplicates links present in the
        restaurant_det_links{city}.csv files in every city directory"""
        city_names = self.get_cities_from_csv
        for name in city_names:
            file_path = f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{name}/restaurant_det_links_{name}.csv" # noqa
            count = 0
            links = []
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-16') as file1:
                    for line in file1:
                        if line not in links:
                            links.append(line)
                        else:
                            count += 1
                    file1.close()
                print(f"duplicate links in {name} are {count}")
                unique = set(links)
                if count != 0:
                    testf = f"C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files/{name}/restaurant_links_{name}.csv"  # noqa
                    with open(testf, 'w', encoding='utf-16') as file2:
                        file2.writelines(unique)
