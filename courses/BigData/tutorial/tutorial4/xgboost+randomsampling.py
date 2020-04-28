# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 11:49:53 2019

@author: lenovo
"""
import random
import numpy as np
import pandas as pd
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Model, load_model
import xgboost as xgb

scaler = MinMaxScaler(feature_range=(0, 1))


#def data_load(path):
   # data_train=[]
#    data_all=np.load(path)
    #data_all=data_all.astype('float')
#    return data_all

def data_load(path1,path2,path3,path4):
   # data_all=[]
   # data_train=[]
    dataset1=np.load(path1)
    dataset2=np.load(path2)
    dataset3=np.load(path3)
    dataset4=np.load(path4)
    print(len(dataset1))
    print(len(dataset2))
    print(len(dataset3))
    print(len(dataset4))
    print(np.min(dataset3[:,-1]))
    print(np.max(dataset3[:,-1]))
    print(np.average(dataset3[:,-1]))
    print(np.min(dataset2[:,-1]))
    print(np.max(dataset2[:,-1]))
    print(np.average(dataset2[:,-1]))
    #data_all=data_all.astype('float')
   # dataset=concatenate((dataset1,dataset3,dataset4,dataset2), axis=0)
    dataset=concatenate((dataset2,dataset3), axis=0)
    #print(dataset[0:10,-2])
    return np.array(dataset3)


    
def data_normalization(data_train):
    columns = [[0]*len(data_train[0])]
    index = range(0,len(data_train))
    df = pd.DataFrame(data_train,index,columns)
    print(df)
    values=df.values 
    print(values) 
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    print(scaled)
    return scaled,scaler


def data_split(data_all):
    # split into train and test sets
    #print(data_all)
    data_x = []
    data_y = []
    datalen=len(data_all)
    # 前面的资源分配信息，为feature
    # 后2位为平均ipc和ipc与自由调度时的比值，为label
    for index in range(datalen):
        data_x.append(data_all[index][0:-1])
        data_y.append(data_all[index][-1:]) 
    data_x=np.array(data_x)
    data_y=np.array(data_y)
    #print (data_x.shape,data_y.shape)
    return data_x,data_y

"""
intput:
   train_x,train_y:training set
"""
def model_train(train_x,train_y,scaler,train_percent):
    model = xgb.XGBRegressor(max_depth=5, learning_rate=0.1, n_estimators=200, silent=False, objective='reg:gamma')
    columns = train_x.shape[0]
    
    items=[i for i in range(0,columns)]
    random.shuffle(items)
    #print(items)
    test_columns = int(columns*train_percent)
    #test_columns = 2
    train_x_sample = train_x[items[0:test_columns-1],:]
    train_y_sample = train_y[items[0:test_columns-1],:]
    model.fit(train_x_sample,train_y_sample)
    #model.save_model("test")
    #model=xgb.Booster(model_file='test')
    
    train_sample= concatenate((train_x_sample,train_y_sample), axis=1)
    
    #prt=xgb.DMatrix(train_x) 
    
    yhat=model.predict(train_x)
    #print(yhat) 
    yhat=np.array(yhat)
    yhat=yhat.reshape(len(yhat),1)  
    #print((len(train_x[0])))
    zero_x = np.zeros((len(yhat),len(train_x[0])),dtype='float32')
    inv_yhat = concatenate((zero_x,yhat), axis=1)
    
    #print(inv_yhat)
    #inv_yhat = scaler.inverse_transform(inv_yhat)
    #print(inv_yhat)
     
    inv_yhat = inv_yhat[:,-1:]
    # recover the original solution
    train_y = train_y.reshape(len(train_y),1)
   # print(train_y.shape,zero_x.shape)
    inv_y = np.concatenate((zero_x,train_y), axis=1)
    #inv_y = scaler.inverse_transform(inv_y)
    inv_y = inv_y[:,-1:]
    
    
    rmse = sqrt(mean_squared_error(inv_y[items[test_columns:]], inv_yhat[items[test_columns:]]))
    #for index in range(len(yhat)):
        #print(inv_yhat[index],inv_y[index])
    
    #To find the best placement in the test set
    errorpt_list=[]
    placement_index = 0
    current_max = 0
    for index in range(test_columns,len(yhat)):
        if inv_yhat[items[index]] > current_max:
            current_max = inv_yhat[items[index]]
            placement_index = index
        errorpt_list.append(abs(inv_y[items[index]] - inv_yhat[items[index]]) / inv_y[items[index]] * 100)
    avg = np.average(inv_y[items[test_columns:]])
    
    #print(inv_yhat[placement_index])
    #print(inv_y[placement_index])
    #print(inv_yhat[1])
    #print(inv_y[1])
    
    #To find the maxium IPC in the training set
    test_data=inv_y[items[0:test_columns-1]].tolist()
    index=test_data.index(np.max(test_data))
    print(test_data[index])
    print(inv_yhat[items[index]])
    
    
    #To find the maximum ipc in the overall set
    print(np.max(inv_y))
    index_max=np.where(inv_y==np.max(inv_y))
    print(inv_yhat[index_max])
    
    
    #To justify whether the optimal is produced by the training set or the test set
    if inv_y[items[index]] > inv_yhat[items[placement_index]]:
        placement_index = index
        
    print(inv_y[items[placement_index]])
    print(inv_yhat[items[placement_index]])
        
     
    error_percentage = rmse / avg
    print('Test RMSE: %.3f' % rmse)    
    print("Test Average Error Percentage: %.2f/100.00" % (error_percentage * 100))
    print(np.average(errorpt_list))
    #print("%.8f" % current_max)
    
    return items[placement_index], error_percentage, train_sample
    #sort_inv_y=inv_y.tolist()
    #sort_inv_yhat=inv_yhat.tolist()
    #.sort()
    #sort_inv_yhat.sort()
   # for index in range(len(sort_inv_y)):
   #     a=sort_inv_y.index(inv_y[index])
   #     b=sort_inv_yhat.index(inv_yhat[index])
        #if (inv_yhat[index] > 1):
           # print(inv_y[index],inv_yhat[index])
           # print(index,a,b)
    
def main(Runnumber=100,train_percent=0.05):
    ipcall=[]
    error=[]
    trainset=[]
    for i in range(Runnumber):
        placement_index,error_percentage,train_sample = model_train(train_x,train_y,scaler,train_percent)
        print("The Best Configuration is %s " % original_data_all[placement_index,:])
        ipcall.append(original_data_all[placement_index,-1])
        error.append(error_percentage)
        trainset.append(train_sample)
    print("Average Performance is %.8f" % np.average(ipcall))
    print("The worst performance is %.8f" % np.min(ipcall))
    print("the worst performance has an index of %d" % ipcall.index(np.min(ipcall)))
    print("Avarage error is %.8f" % np.average(error))
    
    index_best_error=error.index(np.min(error))
    print("Minimum error is %.8f"% np.min(error))
    print(trainset[index_best_error])
    print("minimum error has an index of %d" % index_best_error)
    
    index_worst_error=error.index(np.max(error))
    print("Maximum error is %.8f"% np.max(error))
    print(trainset[index_worst_error])
    print("maximum error has an index of %d" % index_worst_error)
    #placement_index = model_train(train_x,train_y,scaler,train_percent)
    #print("The Best Configuration is %s " % original_data_all[placement_index,:])
    

if __name__ == '__main__':
    path1="data/dataset1.npy"
    path2="data/dataset2.npy"
    path3="data/dataset3.npy"
    path4="data/dataset4.npy"
    #pathtest="data/totaldataset.log"
    original_data_all = data_load(path1,path2,path3,path4)
    data_all,scaler = data_normalization(original_data_all)
    data_all=original_data_all                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    train_x, train_y = data_split(data_all)
    #
    main()
