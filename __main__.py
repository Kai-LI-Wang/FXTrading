#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:55:59 2021

@author: kelly
"""
from RetreiveData import GetData
from _strategy_ import Signal 
import datetime as dt 
import pandas as pd 
from Asset_Allocation import AssetAllocation
import numpy as np 
import time 
import os 
from decimal import Decimal 
pd.set_option('display.max_columns', None)

def CheckPath():
    filepath = "/Users/kelly/Desktop/kaggle_data/python_package/ResultData.csv" 
    if os.path.exists(filepath):
        print("Exists!")
    else: 
        ResultData.to_csv("/Users/kelly/Desktop/kaggle_data/python_package/ResultData.csv")


if __name__=='__main__':
    
    TimeStart = time.time()
    
    start = dt.datetime(2018,1,1)
    end = dt.datetime(2021,2,20)
    
    CurrencyPairList = ["USDJPY","AUDUSD","EURUSD"]    
    DataClass = GetData(start ,end, CurrencyPairList, "Yahoo", "assetallocation")
    AssetAllocateData = DataClass.CurrencyPairTicker()
    AllocationClass = AssetAllocation(AssetAllocateData,CurrencyPairList,start , end )
    Weight = AllocationClass.Simulation()         
    #AllocationClass.plotting()     
    
    StrategyDataClass = GetData(start ,end, CurrencyPairList, "Yahoo", "strategy")
    StrategyData = pd.DataFrame(StrategyDataClass.CurrencyPairTicker())
    
    CurPortRetList = []
    kind = "train"
    TrainTestRatio = 1
    indicator = "BB"
    BB_std = 1.2 
    rolling_window = 20 
    ResultData = pd.DataFrame()
    lotsize = 0.01 
    
    for currencypair in CurrencyPairList:
        SignalClass =Signal(StrategyData, kind, TrainTestRatio, indicator,BB_std , rolling_window, currencypair, lotsize )
        Result = SignalClass.Strategy()
        
        Result.dropna(axis = 0, inplace = True)
        if ResultData.empty:
            ResultData = Result
        else:
            ResultData = pd.concat([ResultData,Result ], axis = 0, ignore_index = True)

        temp = Result["P&L(USD)"].dropna(axis = 0)
        CurPortRetList.append(sum(temp))
   
    CurPortWeightedRet = np.dot(Weight[2:5],np.array(CurPortRetList).reshape(3,1))
    CheckPath()
    
    
    print(ResultData)
    print("+-----------------------------------------------------------+")
    print("Portfolio return = USD${} ".format( CurPortWeightedRet[0]))
    print("Portfolio Weight = ", Weight[2:5])
    print("Expected return = ", Decimal(Weight[0]).quantize(Decimal('0.00001'), rounding='ROUND_UP'))
    print("Portfolio Risk = ", Decimal(Weight[1]).quantize(Decimal('0.00001'), rounding='ROUND_UP'))   
    TimeEnd = time.time()
    print("It took {} Seconds.".format(TimeEnd - TimeStart))
    print("+-----------------------------------------------------------+")
    
    
    

    

   