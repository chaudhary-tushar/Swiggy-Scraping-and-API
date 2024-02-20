import os 
import shutil
import csv


def link_to_name(details_path):
    """
    Converts Links to csv names.
    """
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


def find_remaining_restaurants(folder_path):
    """counts the remaining restaurants left in the det_links.csv to scrape"""
    cities = os.listdir(folder_path)
    count = 0
    links_dict = set()
    files_in_menu = set()
    for city in cities:
        file_path = os.path.join(folder_path, city, f"restaurant_det_links_{city}.csv")
        links_dict.update(link_to_name(file_path))
        menu_path = os.path.join(folder_path, city, "menus")
        files_in_menu.update(set(os.listdir(menu_path)))
        # diff = len(links_set) - len(files_in_menu)
        # count += diff
    count = len(links_dict) - len(files_in_menu) 
    return count

def find_extra_menus(folder_path):
    """returns a list of extra menus that are not linked to any restaurant"""
    cities = os.listdir(folder_path)
    count = 0
    extras = set()
    for city in cities:
        file_path = os.path.join(folder_path, city, f"restaurant_det_links_{city}.csv")
        links_dict = link_to_name(file_path)
        menu_path = os.path.join(folder_path, city, "menus")
        files_in_menu = set(os.listdir(menu_path))
        diff = files_in_menu - links_dict
        extras.update(files_in_menu - links_dict)
        count += len(diff)
    print(len(extras) , "set extras")
    return count, extras


def find_home_of_ext_csv(folder_path,ext_csv):
    cities = os.listdir(folder_path)
    count = 0
    for city in cities:
        file_path = os.path.join(folder_path, city, f"restaurant_det_links_{city}.csv")
        links_dict = link_to_name(file_path)
        menu_path = os.path.join(folder_path, city, "menus")
        files_in_menu = set(os.listdir(menu_path))
        diff = links_dict - files_in_menu
        commons = ext_csv & diff
        count += len(commons)
    return count

def rev_dict_metrics(folder_path):
    cities = os.listdir(folder_path)
    count = 0
    links_dict = {}
    files_in_menu = {}
    for city in cities:
        file_path = os.path.join(folder_path, city, f"restaurant_det_links_{city}.csv")
        got_set = link_to_name(file_path)
        for key in got_set:
            links_dict[key] = city
        menu_path = os.path.join(folder_path, city, "menus")
        menu_set = set(os.listdir(menu_path))
        for yek in menu_set:
            files_in_menu[yek] = city
    print(len(links_dict))
    print(len(files_in_menu))
    common_dict = {key: links_dict[key] for key in links_dict if key in files_in_menu}
    print(len(common_dict)) 
    return (len(links_dict) - len(files_in_menu))


def menus_5608_dict(folder_path):
    """Returns a dictionary of the extra menu csv's that are missing from the det_links_csv
    and their corresponding city
    in the form of key = (csv name <restaurant_(restaurant_name)>.csv) and
    value = <csv path>"""
    cities = os.listdir(folder_path)
    count = 0
    menu_dict = {}
    for city in cities:
        file_path = os.path.join(folder_path, city, f"restaurant_det_links_{city}.csv")
        got_set = set(link_to_name(file_path))
        menu_path = os.path.join(folder_path, city, "menus")
        menu_list = set(os.listdir(menu_path))
        for menu in menu_list:
            menu_file_path = os.path.join(menu_path, menu)
            menu_dict[menu] = menu_file_path
    print(len(menu_dict))
    return menu_dict


def rest_name_occurences(menu_dict, folder_path):
    cities = os.listdir(folder_path)
    city_res_dict = {}
    for city in cities:
        file_path = os.path.join(folder_path, city, f"restaurant_det_links_{city}.csv")
        got_set = set(link_to_name(file_path))
        for item in got_set:
            if item in city_res_dict:
                city_res_dict[item] += 1
            else:
                city_res_dict[item] = 1
    tots = 0
    for key, value in city_res_dict.items():
        if key in menu_dict:
            continue
        if value > 2:
            print(key," : ", value)
            tots += 1
    print(tots)

        

def count_copied_menus(menu_dict, folder_path):
    cities = os.listdir(folder_path)
    count = 0
    for city in cities:
        file_path = os.path.join(folder_path, city, f"restaurant_det_links_{city}.csv")
        got_set = link_to_name(file_path)
        menu_path = os.path.join(folder_path, city, "menus")
        menu_list = set(os.listdir(menu_path))
        got_set.difference_update(menu_list)
        for resto, path in menu_dict.items():
            if resto in got_set:
                count += 1
                shutil.copy(path, menu_path)
    return count
        
        



if __name__ == "__main__":
    current_dir = os.getcwd()
    folder = 'txt_files'
    txt_files_path = os.path.join(current_dir, folder)
    print(find_remaining_restaurants(txt_files_path))
    # cnt, ext_set = find_extra_menus(txt_files_path)
    # print(cnt)
    # print(len(ext_set))
    # print(find_home_of_ext_csv(txt_files_path, ext_set))
    # print(rev_dict_metrics(txt_files_path))
    # menu_dict = menus_5608_dict(txt_files_path)
    # print(count_copied_menus(menu_dict, txt_files_path))
    # rest_name_occurences(menu_dict, txt_files_path)






