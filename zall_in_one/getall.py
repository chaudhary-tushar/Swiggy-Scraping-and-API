import os
import sys
import csv


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


def find_remaining_restaurants(folder_path):
    """counts the remaining restaurants left in the det_links.csv to scrape"""
    cities = os.listdir(folder_path)
    count = 0
    links_dict = {}
    files_in_menu = set()
    for city in cities:
        file_path = os.path.join(folder_path, city, f"restaurant_det_links_{city}.csv")
        links_dict.update(link_to_name(file_path))
        menu_path = os.path.join(folder_path, city, "menus")
        files_in_menu.update(set(os.listdir(menu_path)))
        
    diff  = set(links_dict.keys()) - files_in_menu
    
    return diff, links_dict


def get_links(folder_path):
    pass


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
    result = set()
    for key, value in city_res_dict.items():
        if key in menu_dict:
            continue
        if value >= 2:
            result.add(key)
            tots += 1
    print(tots)
    return result


if __name__ == "__main__":
    txt_files = "C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    diff, links_csv = find_remaining_restaurants(txt_files)
    
    # res_links = get_links(txt_files)
    menu_dict = menus_5608_dict(txt_files)
    get_set = rest_name_occurences(menu_dict, txt_files)
    with open('missngres.csv', 'w', encoding='utf-8') as file:
        for key, value in links_csv.items():
            if key in diff and key in get_set:
                file.write(f'{value}\n')