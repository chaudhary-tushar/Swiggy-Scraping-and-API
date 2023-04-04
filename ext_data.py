import os 
import json
foldpath="C:/Users/tusha/Desktop/vscode/SWIGGY/txt_files"
cit=os.listdir(foldpath)
kamaalarr=[]
# arr=[city name ,restaurant name , rest url ,cuisine,ratings ,cost for two, discount ,coupon]
for city in cit:
    pcit=[]
    detpath=f"{foldpath}/{city}/restaurant_details_{city}.csv"
    linkpath=f"{foldpath}/{city}/restaurant_links_{city}.csv"
    menpath=f"{foldpath}/{city}/menus"
    with open(detpath,'r',encoding='utf-8') as file1 , open(linkpath,'r',encoding='utf-16') as file2:
        lines1=file1.readlines()
        lines2=file2.readlines()
        for i in range(20):
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
                    pres.append(name)
                    
                    pres.append(lines2[i].replace('\n','').replace("'",""))
                    
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
        
#print(kamaalarr)
with open("ext.csv",'w',encoding='utf=16') as file3:
    for i in range(len(kamaalarr)):
        print(len(kamaalarr[i]))
        for j in range(len(kamaalarr[i])):
            file3.write(kamaalarr[i][j])
            file3.write(" ,")
        file3.write("\n")
            
    
 