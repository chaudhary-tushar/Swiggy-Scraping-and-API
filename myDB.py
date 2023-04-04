import mysql.connector as connector
import os 
import json
class restArr:
    def __init__(self) -> None:
        self.foldpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    #foldpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
    def makear(self):
        cit=os.listdir(self.foldpath)
        kamaalarr=[]
        # arr=[city name ,restaurant name , rest url ,cuisine,ratings ,cost for two, discount ,coupon]
        for city in cit:
            pcit=[]
            detpath=f"{self.foldpath}/{city}/restaurant_details_{city}.csv"
            linkpath=f"{self.foldpath}/{city}/restaurant_links_{city}.csv"
            menpath=f"{self.foldpath}/{city}/menus"
            with open(detpath,'r',encoding='utf-8') as file1 , open(linkpath,'r',encoding='utf-16') as file2:
                lines1=file1.readlines()
                lines2=file2.readlines()
                x=0
                if(len(lines2)<20):
                    x=len(lines2)
                else:
                    x=20
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
                        pres.append("none")
                    while(len(pres)<8):
                        pres.append("none ")
                    kamaalarr.append(pres)
        return kamaalarr
        

class cityDB:
    def __init__(self):
        self.con=connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'swiggdb')
        query='CREATE TABLE if not exists citydat(cityId int PRIMARY KEY AUTO_INCREMENT, CityName varchar(50), CityUrl varchar(200))'
        cur=self.con.cursor()
        cur.execute(query)
        print("table created")
        
    def insert(self,ctname,cturl):
        query=f"insert into citydat(CityName,CityUrl) values ('{ctname}','{cturl}')"
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
    
    def delete(self):
        query="delete from citydat"
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("deleted")
        
class restDB:
    def __init__(self):
        self.con=connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'swiggdb')
        query="CREATE TABLE if not exists restaurant_dat(rest_Id int PRIMARY KEY AUTO_INCREMENT,city_name varchar(50), rest_Name varchar(50), rest_Url varchar(200),cuisine varchar(100),ratings varchar(5),cost_for_two varchar(50) , discount int , coupon varchar(20))"
        cur=self.con.cursor()
        cur.execute(query)
        print("restaurant table created")
    def res_insert(self,list):
        # arr=[city name ,restaurant name , rest url ,cuisine,ratings ,cost for two, discount ,coupon]
        query=f"insert into restaurant_dat(city_name,rest_name,rest_url,cuisine,ratings,cost_for_two,discount,coupon) values ('{list[0]}','{list[1]}','{list[2]}','{list[3]}','{list[4]}','{list[5]}','{int(list[6])}','{list[7]}')"
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
    
        
        
        
################ starting main
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
for pres in listq:
    rdb.res_insert(pres)

