# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import xlwt
import numpy as np

path="./data/parsec_2.log"
kvmcpu=16
kvmmem=16
nodecore=32
nodemem=1
cache_l3=1
imp1=225
imp2=113

def kvmvec(place,kvm):
    vec=[]
    placement = []
    vmnumber=int(len(place)/2)
    nodelist=place[:vmnumber]
    memlist=place[vmnumber:]
    vec.append(kvmcpu)
    
    if kvm in place[0] and kvm in place[1]:
        placement.append(2)
    elif kvm in place[0]:
        placement.append(0)
    else:
        placement.append(1)
        
        
    if kvm in place[2] and kvm in place[3]:
        placement.append(2)
    elif kvm in place[2]:
        placement.append(0)
    else:
        placement.append(1)
        
        
    for item in nodelist:
        if kvm in item:
            vec.append(nodecore)
        else:
            vec.append(0)
            
    vec.append(kvmmem)
    for item in memlist:
        if kvm in item:
            vec.append(nodemem/(len(item)-1))
        else:
            vec.append(0)   

    for item in memlist:
        if kvm in item:
            vec.append(cache_l3/(len(item)-1))
        else:
            vec.append(0)
    #print(vec)
    return vec, placement

def kvmipc(counters):
    ipc=0.0
    vmnumber=int(len(counters)/2)
    cyl=counters[:vmnumber]
    ins=counters[vmnumber:]
    for index in range(len(cyl)):
        cylnum=cyl[index].replace(',','')
        insnum=ins[index].replace(',','')
        #print(insnum)
        #ipc+= float(insnum)/float(cylnum)
        ipc+=float(insnum)/3
    return ipc/3

def main():
    try:
    
        file = open(path, 'r') 
    
    except:
        print("open error")
  
    data=[]
    placement = []
    num=0
    numline = 0
    for line in file.readlines():
        # 处理资源向量
        if len(line) == 1:
            break
        if num==0:
            ipc=0
            place=line.split('-')
            print(place)
            del place[0]
            #print(len(line))
            #print(place)
            vec_a,place_a=kvmvec(place,'A')
            vec_b,place_b=kvmvec(place,'B')
            vec_c,place_c=kvmvec(place,'C')
            num=num+ 1
        # 处理ipc
        else:
            counters=line.split(' ')
            #print(counters)
            ipc+= kvmipc(counters)
            if numline == 729:
                print(ipc)
            num=num+1
        if num==6:
            numline =  numline + 1
            vec=vec_a+vec_b+vec_c
            place = place_a + place_b + place_c
            #print(ipc/5)
            vec.append(ipc/5)
            #place.append(ipc/5)
            data.append(vec)
            placement.append(place)
            num=0
    #处理icp与自由调度的比值，以及2个重要placement
    # ipc_imp1=data[imp1][-1]
    # ipc_imp2=data[imp2][-1]
    for index in range(len(data)):
        ipc_raito=data[index][-1]/data[-1][-1]
        # important1_ipc=ipc_imp1/data[-1][-1]
        # important2_ipc=ipc_imp2/data[-1][-1]
        del data[index][-1]
        # data[index].append(important1_ipc)
        # data[index].append(important2_ipc)
        data[index].append(ipc_raito)
        placement[index].append(ipc_raito)
        # print(placement[index])
    data_train=np.array(data)

    
    f1 = open('./data/placementlog.txt','w')
    
    for fp in placement:
        f1.write(str(fp))
        f1.write('\n')

   # f1.write(placement)
    f1.close()

    placement_train=np.array(placement)
    print(placement_train)
    np.save('./data/train2',data_train)
    np.save('./data/placement_train',placement_train)

    
if __name__ == '__main__':
    main()
