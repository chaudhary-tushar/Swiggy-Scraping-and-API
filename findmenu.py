import os
path="C:/Users/tusha/Desktop/vscode/placement 100/txt_files"
ctfd=os.listdir(path)
# print(ctfd)
for city in ctfd:
    menpath=f"{path}/{city}/menus"
    if os.path.exists(menpath):
        print(city)
        print("entered here\n")
    # else:
    #     print(f'no menu for {city} , ',end='')