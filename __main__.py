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

if __name__=='__main__':
    
    TimeStart = time.time()
    
    start = dt.datetime(2019,1,1)
    end = dt.datetime(2021,2,20)
    
    CurrencyPairList = ["USDJPY","AUDUSD","EURUSD"]    
    DataClass = GetData(start ,end, CurrencyPairList, "Yahoo", "assetallocation")
    AssetAllocateData = DataClass.CurrencyPairTicker()
    AllocationClass = AssetAllocation(AssetAllocateData,CurrencyPairList,start , end )
    result = AllocationClass.Simulation()         
    #AllocationClass.plotting()     
    
    StrategyDataClass = GetData(start ,end, CurrencyPairList, "Yahoo", "strategy")
    StrategyData = pd.DataFrame(StrategyDataClass.CurrencyPairTicker())
    
    CurPortRetList = []
    kind = "train"
    TrainTestRatio = 0.8
    indicator = "BB"
    BB_std = 1.2 
    rolling_window = 20 
    
    for currencypair in CurrencyPairList:
        b =Signal(StrategyData, kind, TrainTestRatio, indicator,BB_std , rolling_window, currencypair )
        g = b.Strategy()
        print(g.head(15))
        k = g["P&L(USD)"].dropna(axis = 0)
        CurPortRetList.append(sum(k))
   
    CurPortWeightedRet = np.dot(result[2:5],np.array(CurPortRetList).reshape(3,1))

    print("+-----------------------------------------------------------+")
    print("Portfolio return = ", CurPortWeightedRet[0])

    TimeEnd = time.time()
    print("It took {} Seconds.".format(TimeEnd - TimeStart))
    print("+-----------------------------------------------------------+")