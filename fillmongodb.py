import pymongo
import os
import pandas as pd
class restArr:
    def __init__(self):
        self.foldpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
        
    def makear(self):
        cit=os.listdir(self.foldpath)
        kamaalarr=[]
        
        for city in cit:
            detpath=f"{self.foldpath}/{city}/restaurant_det_links_{city}.csv"
            if (os.path.isfile(detpath)):
                menpath=f"{self.foldpath}/{city}/menus"
                df=pd.read_csv(detpath)
                details=df["Details"]
                links=df["Links"]
                x=len(links)
                for i in range(x):
                    pres=[]
                    pres.append(city)
                    rind=links[i].rfind('/')
                        
                    if ("%" in details[i]):
                        discountind=details[i].rfind('%')
                        discount=details[i][discountind-2:discountind]
                        couponind=details[i].rfind("Use")
                        couponlind=details[i].rfind("Quick")
                        coupon=details[i][couponind+4:couponlind]
                    restaurantname=links[i][rind+1:rind+20]
                    menu=f"{menpath}/restaurant_{restaurantname}.csv"
                    if os.path.isfile(menu):
                        with open(menu,'r',encoding='utf-8') as fileq:
                            lines3=fileq.readlines()
                            impdat=lines3[3:8]
                            
                            namind=impdat[0].rfind(':')
                            namelind=impdat[0].find(',',namind)
                            name=impdat[0][namind+2:namelind]
                            pres.append(name.replace("'",""))
                            
                            pres.append(links[i].replace('\n',''))
                                
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

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['swiggdb']

with open('city.csv','r',encoding='utf-8') as file1:
    lines=file1.readlines()
    for line in lines:
        url=line[:-1]
        nameind=line.rfind('/')
        name=line[nameind+1:-1].capitalize()
        citydata=[{'CityName':f'{name}','CityUrl':f'{url}'}]
        db.Cities.insert_many(citydata)

fill=restArr()
data=fill.makear()
print(len(data))
for rest in data:
    Restaurant_details=[{'City': f'{rest[0]}','RestaurantName': f'{rest[1]}','Rest_Url': f'{rest[2]}','Cuisine': f'{rest[3]}','Ratings': f'{rest[4]}','Cost_Two': f'{rest[5]}','Discount': f'{rest[6]}','Coupon': f'{rest[7]}'}]
    db.Restaurants.insert_many(Restaurant_details)

client.close()
