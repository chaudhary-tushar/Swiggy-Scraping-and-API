import psycopg2
import os, sys
import pandas as pd
import random
import re

class restArr:
    def __init__(self):
        self.foldpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
        
    def makear(self):
        cities=os.listdir(self.foldpath)
        kamaalarr=[]
        
        for city in cities[:100]:
            count = 0
            detpath=f"{self.foldpath}/{city}/restaurant_det_links_{city}.csv"
            if (os.path.isfile(detpath)):
                menpath=f"{self.foldpath}/{city}/menus"
                df=pd.read_csv(detpath)
                details=df["Details"]
                links=df["Links"]
                x=len(links)
                for i in range(x):
                    rind=links[i].rfind('/')
                    res_name = details[i]
                    res_url = links[i]
                    restaurantname=links[i][rind+1:rind+20]
                    menu=f"{menpath}/restaurant_{restaurantname}.csv"
                    if os.path.isfile(menu):
                        with open(menu,'r',encoding='utf-8') as fileq:
                            lines=fileq.readlines()
                            for line in lines[:10]:
                                if 'Cuisine' in line:
                                    cusind=line.rfind(':')
                                    cuisine = line[cusind+1:].strip().split(',')[:-1]
                                if 'Rating' in line:
                                    ratind=line.rfind(':')
                                    ratlind=line.rfind(',')
                                    rating = line[ratind+2:ratlind]
                                    # print(rating)
                                    if rating != 'NEW':
                                        ratings = float(rating)
                                        
                                    else:
                                        ratings = 4.0
                                if 'Cost is' in line:
                                    costind=line.rfind(':')
                                    costlind=line.rfind('f')
                                    cost_for_two=int(line[costind+3:costlind])
                            if not ratings:
                                ratings = 4.0
                            resobj = Res_Obj(city, res_name, res_url, cuisine, ratings, cost_for_two)
                            count += 1
                            kamaalarr.append(resobj)
                            
                            fileq.close()
                    else:
                        continue
            print(city, count)
        return kamaalarr

class cityDB:
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            database="swigg",
            user="postgres",
            password="root"
        )
        query = 'CREATE TABLE IF NOT EXISTS citydat(cityId SERIAL PRIMARY KEY, CityName VARCHAR(50), CityUrl VARCHAR(200), Total_Restaurants INTEGER)'
        cur = self.con.cursor()
        cur.execute(query)
        print("table created")

    def insert(self, ctname, cturl):
        try:
            query = f"INSERT INTO citydat(CityName, CityUrl) VALUES ('{ctname}', '{cturl}')"
            cur = self.con.cursor()
            cur.execute(query)
            self.con.commit()
        except psycopg2.errors.UniqueViolation as e:
        # Handle the unique constraint violation error here
            print("Error:", cturl, "is already in the database.") 
            # Rollback the transaction if needed
            self.con.rollback()
        except psycopg2.Error as e:
            # Handle other errors
            print("Error:", e)
            # Rollback the transaction if needed
            self.con.rollback()
        finally:
            # Close the cursor
            cur.close()


class restDB:
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            database="swigg",
            user="postgres",
            password="root"
        )
        query = "CREATE TABLE IF NOT EXISTS restaurant_dat(rest_Id SERIAL PRIMARY KEY, rest_Name VARCHAR(100), rest_Url VARCHAR(200), cuisine TEXT[], ratings DECIMAL(2,1), cost_for_two INTEGER, discount INTEGER, coupon VARCHAR(20), city_name VARCHAR(50))"
        cur = self.con.cursor()
        cur.execute(query)
        print("restaurant table created")

    def res_insert(self, res):
        query = "INSERT INTO restaurant_dat(rest_name, rest_url, cuisine, ratings, cost_for_two, discount, coupon, city_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    
        values = (res.name, res.url, res.cuisine, res.rating, res.cost_for_two, res.discount, res.coupon, res.city)
        cur = self.con.cursor()
        try:
            cur.execute(query, values)
        except psycopg2.errors.UniqueViolation as e:
            self.con.rollback()
        except psycopg2.Error as e:
            print("Error:", e, res.url)
            
            self.con.rollback()
        self.con.commit()


class City_Obj:
    def __init__(self, name, link):
        self.name = name
        self.link = link
    def __str__(self):
        return self.link

def disc():
    darr = [10,25,30,40,45,50,55,60]
    rd = random.choice(darr)
    return rd
def coupon():
    carr = ['STEALDEAL', 'FLATDEAL', 'JUMBO', 'GOURMETFF', 'SPECIALS', 'MATCHPARTY', 'TRYNEW', 'PARTY', 'GUILTFREE', 'SWIGGYIT']
    rc = random.choice(carr)
    return rc


class Res_Obj:
    def __init__(self, city, name, url, cusi, rat, cost):
        self.city = city
        self.name = name
        self.url = url
        self.cuisine = cusi
        self.rating = rat
        self.cost_for_two = cost
        self.discount = disc()
        self.coupon = coupon()


# ctar=[]
# with open('city.csv','r') as file:
#     lines = file.readlines()
#     for line in lines[:10]:
#         lnk=line.rstrip('\n')
#         nind=lnk.rfind('/')
#         nme=lnk[nind+1:]
#         name=nme.capitalize()
#         cityobj = City_Obj(name,lnk)
#         ctar.append(cityobj)



# dbh=cityDB()
# for i in range(len(ctar)):
#     dbh.insert(ctar[i].name,ctar[i].link)
# print("citydat filled")
# dbh.delete()
rdb=restDB()
arr=restArr()
listq=arr.makear()
print('make arr completed')
print(len(listq))

# for pres in listq:
#     rdb.res_insert(pres)






