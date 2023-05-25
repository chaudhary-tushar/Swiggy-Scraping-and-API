import os 
import mysql.connector as connector
import pymongo
import psycopg2
import makingmenu as mm
import time

class Msql:
    def __init__(self):
        self.con=connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'swiggdb')
        query="CREATE TABLE if not exists menudat(itemId int PRIMARY KEY AUTO_INCREMENT,City varchar(20),rest_name varchar(50),rest_url varchar(200),item_name varchar(500),item_type varchar(50),item_cid varchar(50),cost varchar(50),Description varchar(500),customization varchar(50),Bestseller varchar(50))"
        cur=self.con.cursor()
        cur.execute(query)
        self.ins=0
        
        
    def insert(self,list):
        query = f'''INSERT INTO menudat (City, rest_name, rest_url, item_name, item_type, item_cid, cost, Description, customization, Bestseller) VALUES (\"{list[0]}\", \"{list[1]}\", \"{list[2]}\", \"{list[3].replace('"', '""')}\", \"{list[4]}\", \"{list[5]}\", \"{list[6].strip()}\", \"{list[7]}\", \"{list[8]}\", \"{list[9]}\")'''

        cur=self.con.cursor()
        
        try:
            cur.execute(query)
        except:
            self.ins+=1
            
        self.con.commit()
 
class Mngdb:
    def __init__(self):
        self.client=pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['swiggdb']
        db=self.db
        self.ins=0

      
    
    def insert(self,list):
        db=self.db
        Menu_details=[{'City': f'{list[0]}','RestaurantName': f'{list[1]}','Rest_Url': f'{list[2]}','Item-name': f'{list[3]}','Item-Type': f'{list[4]}','Item-section': f'{list[5]}','Cost': f'{list[6]}','Description': f'{list[7]}','Customization': f'{list[8]}','Bestseller': f'{list[9]}'}]
        
        try:
            db.Menu.insert_many(Menu_details)
        except:
            self.ins+=1

class Pgdb:
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            database="swiggdb",
            user="postgres",
            password="root"
        )
        query = "CREATE TABLE IF not exists menudat(itemId SERIAL PRIMARY KEY,City varchar(20),rest_name varchar(50),rest_url varchar(200),item_name varchar(500),item_type varchar(50),item_cid varchar(50),cost varchar(50),Description varchar(500),customization varchar(50),Bestseller varchar(50))"
        cur = self.con.cursor()
        self.ins=0
        
        try:
            cur.execute(query) 
            print("Table postgres created")
        except:
            print("table missing")
            pass  
        self.con.commit()
        
        
        
        
    def insert(self,list):
        
        query = f'''INSERT INTO menudat(City, rest_name, rest_url, item_name, item_type, item_cid, cost, Description, customization, Bestseller) VALUES ('{list[0]}', '{list[1]}', '{list[2]}', '{list[3].replace("'", "''")}', '{list[4]}', '{list[5]}', '{list[6].strip()}', '{list[7]}', '{list[8]}', '{list[9]}')'''
        cur=self.con.cursor()
        
        
        try:
            cur.execute(query)
        except:
            self.ins+=1
            pass
        self.con.commit()
        
st=time.time()     
mahabaliar=mm.maker()

md=time.time()    
# msql=Msql()
mngdb=Mngdb()
#pgdb=Pgdb()
for list in mahabaliar:
    # msql.insert(list)
    mngdb.insert(list)
    # pgdb.insert(list)
print(mngdb.ins)
ed=time.time()
print(md-st)
print(ed-st)
    