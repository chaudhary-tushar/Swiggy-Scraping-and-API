import os
import csv
import shutil



def check(file_dest):
    cities = os.listdir(file_dest)
    absent = []
    for city in cities[:10]:
        name_set = set()
        menu_path = f"{file_dest}/{city}/menus"
        if not os.path.exists(menu_path):
            print(city)
            continue
        details_path = f"{file_dest}/{city}/restaurant_det_links_{city}.csv"
        with open(details_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    link = row[1].strip()
                    nameind=link.rfind('/')
                    name=link[nameind+1:nameind+20]
                    det_name = f"restaurant_{name}.csv"
                    name_set.add(det_name)
        menu_list = os.listdir(menu_path)
        for item in menu_list:
            if item not in name_set:
                print(item)
                absent.append(item)
        print('work done for ', city)
    print(len(absent))


def correct_city_relations(file_dest):
    cities = os.listdir(file_dest)
    count = 0
    city_dict = {}
    for city in cities:
        details_path = f"{file_dest}/{city}/restaurant_det_links_{city}.csv"
        city_dict[city] = []
        with open(details_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    link = row[1].strip()
                    nameind=link.rfind('/')
                    name=link[nameind+1:nameind+20]
                    det_name = f"restaurant_{name}.csv"
                    city_dict[city].append(det_name)
    men_set = set()
    for city in cities:
        menu_path = f"{file_dest}/{city}/menus"
        menu_list = os.listdir(menu_path)
        for item in menu_list:
            if item in city_dict[city]:
                city_dict[city].remove(item)
                men_set.add(item)

    print(len(men_set))
    found = 0
    count = 0
    with open('correct_relation.csv', 'w', encoding='utf-8')as file1:
        for city in cities:
            menu_path = f"{file_dest}/{city}/menus"
            menu_list = os.listdir(menu_path)
            for item in menu_list:
                if item in men_set:
                    continue
                else:
                    for key, value in city_dict.items():
                        if item  in value:
                            if key != city:
                                file1.write(f"{key}     :   {menu_path}/{item}\n")
                                found += 1
                                source = os.path.join(menu_path,item)
                                destination = os.path.join(file_dest,key,"menus",item)
                                print(source)
                                print(destination)
                                shutil.move(source, destination)
                                break
                    count += 1
            
    print("total lavaris restaurants found in different city = ",found)
    print("total lavaris restaurants with no city = ",count)


def transfer(source, destination):
    entries = os.listdir(source)
    source_city = [entry for entry in entries if os.path.isdir(os.path.join(source, entry))]
    entries = os.listdir(destination)
    destination_city = [entry for entry in entries if os.path.isdir(os.path.join(destination, entry))]
    for i in range(len(source_city)):
        if source_city[i] not in destination_city:
            print(source_city[i])
            continue
        print("working on copying menu files from", source_city[i])
        source_menu_folder = f"{source}/{source_city[i]}/menus"
        destination_menu_folder = f"{destination}/{source_city[i]}/menus"
        source_menu_file = [f for f in os.listdir(source_menu_folder) if os.path.isfile(os.path.join(source_menu_folder, f))]
        for file_name in source_menu_file:
            source_path = os.path.join(source_menu_folder, file_name)
            target_path = os.path.join(destination_menu_folder, file_name)
            if not os.path.exists(target_path):
                shutil.copy2(source_path, target_path)


def build_dictionary(file_dest):
    cities = os.listdir(file_dest)
    rev_dict = {}
    count = 0
    for city in cities:
        menu_path = f"{file_dest}/{city}/menus"
        menu_list = os.listdir(menu_path)
        for item in menu_list:
            count += 1
            rev_dict[item] = city
    print(count)
    print(len(rev_dict))
    print("reverse menu dictionary \n*******************")
    return rev_dict


def rev_city(file_dest):
    cities = os.listdir(file_dest)
    count = 0
    city_dict = {}
    for city in cities:
        details_path = f"{file_dest}/{city}/restaurant_det_links_{city}.csv"
        
        with open(details_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    link = row[1].strip()
                    nameind=link.rfind('/')
                    name=link[nameind+1:nameind+20]
                    det_name = f"restaurant_{name}.csv"
                    city_dict[det_name] = city
                    count += 1
    print(count)
    print(len(city_dict))
    print("reverse city dictionary \n***********")
    return city_dict


def findout(file_dest):
    rev_dict = rev_city(file_dest)
    ver_dict = build_dictionary(file_dest)

    count = 0 
    mismatch = 0
    for key, value in ver_dict.items():
        if key not in rev_dict:
            count += 1
    print(mismatch)
    print(count)

def check_if_menu_in_det(file_dest):
    cities = os.listdir(file_dest)
    count = 0
    absent = []
    for city in cities:
        city_set = set ()
        details_path = f"{file_dest}/{city}/restaurant_det_links_{city}.csv"
        
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

        menu_path = f"{file_dest}/{city}/menus"
        menu_list = os.listdir(menu_path)
        for item in menu_list:
            if item not in city_set:
                count +=1
    print(count)



if __name__ == "__main__":
    file_dest = "C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    file_source = "C:/Users/tusha/Desktop/vscode/txt_files"
    
    check_if_menu_in_det(file_dest)
    