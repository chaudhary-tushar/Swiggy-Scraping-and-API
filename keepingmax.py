from multiprocessing import Pool

def apn(lst):
    a=10
    qwer=[0,0,0,0,0,0,0,0,0,0]
    for i in range(lst):
        qwer[i]=(5*a)
    return qwer

if __name__ =="__main__":
    
    five=[1,2,3,4,5,6,7,8,9,10]
    with Pool(8) as p:
        p.map(apn,five)
        
    print(five)