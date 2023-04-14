import psycopg2
import os

class restArr:
    def __init__(self):
        self.foldpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    #foldpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    def makear(self):
        cit=os.listdir(self.foldpath)
        kamaalarr=[]
        # arr=[city name ,restaurant name , rest url ,cuisine,ratings ,cost for two, discount ,coupon]
        for city in cit:
            detpath=f"{self.foldpath}/{city}/restaurant_details_{city}.csv"
            linkpath=f"{self.foldpath}/{city}/restaurant_links_{city}.csv"
            if (os.path.isfile(detpath)):
                menpath=f"{self.foldpath}/{city}/menus"
                with open(detpath,'r',encoding='utf-8') as file1 , open(linkpath,'r',encoding='utf-16') as file2:
                    lines1=file1.readlines()
                    lines2=file2.readlines()
                    x=0
                    if(len(lines2)<20):
                        x=len(lines2)
                    else:
                        x=len(lines2)
                    for i in range(x):
                        pres=[]
                        pres.append(city)
                        rind=lines2[i].rfind('/')
                        # discount=""
                        # coupon=""
                        if ("%" in lines1[i]):
                            discountind=lines1[i].rfind('%')
                            discount=lines1[i][discountind-2:discountind]
                            couponind=lines1[i].rfind("Use")
                            couponlind=lines1[i].rfind("Quick")
                            coupon=lines1[i][couponind+4:couponlind]
                        restaurantname=lines2[i][rind+1:rind+20]
                        menu=f"{menpath}/restaurant_{restaurantname}.csv"
                        if os.path.isfile(menu):
                            with open(menu,'r',encoding='utf-8') as fileq:
                                lines3=fileq.readlines()
                                impdat=lines3[3:8]
                                
                                namind=impdat[0].rfind(':')
                                namelind=impdat[0].find(',',namind)
                                name=impdat[0][namind+2:namelind]
                                pres.append(name.replace("'",""))
                                
                                pres.append(lines2[i].replace('\n',''))
                                
                                cusind=impdat[1].rfind(':')
                                cuslind=impdat[1].rfind(',')
                                cuisine=impdat[1][cusind+2:cuslind]
                                if len(cuisine)>=10:
                                    cuisine=cuisine.replace(","," &")
                                pres.append(cuisine)
                                
                                ratind=impdat[2].rfind(':')
                                ratlind=impdat[2].rfind(',')
                                rating=impdat[2][ratind+2:ratlind]
                                if len(rating)<4:
                                    pres.append(rating)
                                else:
                                    pres.append("3.8")
                                
                                costind=impdat[4].rfind(':')
                                costlind=impdat[4].rfind(',')
                                costfortwo=impdat[4][costind+2:costlind]
                                pres.append(costfortwo)
                                fileq.close()
                        else:
                            pass
                        pres.append(discount)
                        if len(coupon)<=10:   
                            pres.append(coupon)
                        else:
                            pres.append(None)
                        while(len(pres)<8):
                            pres.append(None)
                        kamaalarr.append(pres)
        return kamaalarr


class cityDB:
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            database="swiggdb",
            user="postgres",
            password="root"
        )
        query = 'CREATE TABLE IF NOT EXISTS citydat(cityId SERIAL PRIMARY KEY, CityName VARCHAR(50), CityUrl VARCHAR(200))'
        cur = self.con.cursor()
        cur.execute(query)
        print("table created")

    def insert(self, ctname, cturl):
        query = f"INSERT INTO citydat(CityName, CityUrl) VALUES ('{ctname}', '{cturl}')"
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()

class restDB:
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            database="swiggdb",
            user="postgres",
            password="root"
        )
        query = "CREATE TABLE IF NOT EXISTS restaurant_dat(rest_Id SERIAL PRIMARY KEY, city_name VARCHAR(50), rest_Name VARCHAR(50), rest_Url VARCHAR(200), cuisine VARCHAR(100), ratings VARCHAR(5), cost_for_two VARCHAR(50), discount INTEGER, coupon VARCHAR(20))"
        cur = self.con.cursor()
        cur.execute(query)
        print("restaurant table created")

    def res_insert(self, lst):
        # lst = [city name, restaurant name, rest url, cuisine, ratings, cost for two, discount, coupon]
        query = f"INSERT INTO restaurant_dat(city_name, rest_name, rest_url, cuisine, ratings, cost_for_two, discount, coupon) VALUES ('{lst[0]}', '{lst[1]}', '{lst[2]}', '{lst[3]}', '{lst[4]}', '{lst[5]}', '{lst[6]}', '{lst[7]}')"
        cur = self.con.cursor()
        try:
            cur.execute(query)
            print("inserted i")
        except:
            pass
        self.con.commit()


ctar=[]
with open('city.csv','r') as file:
    i=1
    for line in file:
        perc=[]
        lnk=line.rstrip('\n')
        nind=lnk.rfind('/')
        nme=lnk[nind+1:]
        name=nme.capitalize()
        perc.append(i)
        perc.append(name)
        perc.append(lnk)
        i+=1
        ctar.append(perc)
        
dbh=cityDB()
for i in range(len(ctar)):
    dbh.insert(ctar[i][1],ctar[i][2])
print("citydat filled")
# dbh.delete()
rdb=restDB()
arr=restArr()
listq=arr.makear()
print('make arr completed')
with open("insertingd.csv",'w',encoding='utf- 16') as filew:
    for i in range(len(listq)):
        filew.write(f'{listq[i]}\n')
for pres in listq:
    rdb.res_insert(pres)






