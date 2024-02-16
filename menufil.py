import os, sys
import psycopg2
import makingmenu as mm
import time


class Pgdb:
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            database="swigg",
            user="postgres",
            password="root"
        )
        query = "CREATE TABLE IF not exists menudat(itemId SERIAL PRIMARY KEY,item_name varchar(150),item_type varchar(50),item_cid varchar(50),cost INTEGER,Description varchar(500),customization BOOLEAN,Bestseller BOOLEAN,City varchar(20),rest_url varchar(200))"
        cur = self.con.cursor()
        self.ins=0
        
        try:
            cur.execute(query) 
            print("Table postgres created")
        except:
            print("table missing")
            pass  
        self.con.commit()
        
        
        
        
    def insert(self,menu):
        
        query = f"INSERT INTO menudat(item_name, item_type, item_cid, cost, Description, customization, Bestseller,City, rest_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (menu.item_name, menu.item_type, menu.item_cid, menu.cost, menu.description, menu.customization, menu.bestseller, menu.city_name, menu.rest_url_link)
        
        cur = self.con.cursor()
        try:
            cur.execute(query,values)
        except psycopg2.errors.UniqueViolation as e:
            self.con.rollback()
        except psycopg2.Error as e:
            print("Error:", e)
            
            self.con.rollback()
        self.con.commit()
        
st=time.time()     
mahabaliar=mm.maker()

md=time.time()    
# sys.exit()
pgdb=Pgdb()
for menu in mahabaliar:
    pgdb.insert(menu)
ed=time.time()
print(md-st)
print(ed-st)
    