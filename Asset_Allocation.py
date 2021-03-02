#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 12:48:00 2021

@author: kelly
"""
import pandas as pd 
import quandl 
import numpy as np 
#import cvxpy as cp
import datetime as dt
#from decimal import Decimal 
import pandas_datareader.data as pdr 
import matplotlib.pyplot as plt 
quandl.ApiConfig.api_key = "PXoA79qRmDpA5sMhVmZz"


#CurrencyPairTicker =['BOE/XUDLJYD', "RBA/FXRUSD","ECB/EURUSD"]



class AssetAllocation():  
    def __init__(self, data, CurrencyPairTicker,start_date, end_date):
        #self.CurrencyPairTickerDict = { 'BOE/XUDLJYD':"USDJPY", "RBA/FXRUSD":"AUDUSD", \
        #             "ECB/EURUSD": "EURUSD" }
        
        self.df = pd.DataFrame(data) 
        self.CurrencyPairTicker =  CurrencyPairTicker
        self.start = start_date 
        self.end = end_date 
        #self.get_data()
        self.CovarianceMatrix()
        self.Weights()
        self.PortfolioSTD()
        self.RiskFreeRate()
        self.PortfolioReturn()
        self.SharpRatio()
        self.ExpectedReturn = self.AverageReturn
        
    
    def __repr__():
        return ""


   


    def CovarianceMatrix(self):
        df_ret = np.log(self.df/self.df.shift(1))
        df_ret.dropna(inplace = True)
        temp = np.array(df_ret.std(axis = 0)).reshape(len(self.CurrencyPairTicker),1)
        #Std_mat = np.dot(temp, temp.T)
        self.AverageReturn = np.array(df_ret.mean(axis = 0)).reshape(1,len(self.CurrencyPairTicker))
        self.Cov_Mat = np.cov(df_ret.values.T)
        self.Cor_Mat = df_ret.corr(method ="pearson")
        self.Port_Vol = np.sqrt(np.array(self.Cor_Mat).diagonal())
        
        
    def Weights(self):
        w = np.random.randint(10, size = len(self.CurrencyPairTicker))
        w_array = []
        [w_array.append(i/sum(w)) for i in w]
        self.WeightArray = np.array(w_array).reshape(len(self.CurrencyPairTicker),1)
        
        
    def PortfolioReturn(self):
        self.Port_ret = np.dot(self.AverageReturn,self.WeightArray) 
        

    def PortfolioSTD(self):
        self.Port_STD = np.sqrt(np.dot(np.dot(self.WeightArray.T, self.Cor_Mat), self.WeightArray))
        
        
    
    def RiskFreeRate(self):
        for i in range(10):
            df = pdr.DataReader('DGS10','fred', start = self.end, end = self.end )
            if df.empty:
                self.end = self.end + dt.timedelta(-1)
            else:     
                self.Rf = df.values 
                break 
            
    def SharpRatio(self):
        self.sharp = (self.Port_ret )/self.Port_STD
         
        
    def Simulation(self):    
        counter = 0 
        data = pd.DataFrame(columns = ["Return(%)", "Risk", "W1", "W2", "W3","Sharp" ], index =np.arange(10000))
        
        for i in range(10000):
            
            counter += 1 
            
            self.Weights()
            self.PortfolioReturn()
            self.PortfolioSTD()
            self.SharpRatio()
            w = self.WeightArray
            data["Return(%)"].iloc[i] = round(self.Port_ret[0][0], 5)*100
            data["Risk"].iloc[i] = round(self.Port_STD[0][0], 5)
            data["W1"].iloc[i] = round(w[0][0],5)
            data["W2"].iloc[i] = round(w[1][0],5)
            data["W3"].iloc[i] = round(w[2][0],5)   
            data["Sharp"].iloc[i] = round(self.sharp[0][0], 5)
        self.data = data 
        index = np.array(self.data['Sharp']).argmax()
        Result = data.iloc[index]

        return Result 
        
    
    def plotting(self):     
        plt.figure(figsize = (10,7))
        plt.scatter(self.data['Return(%)'], self.data["Risk"])
        xlabels = "Risk"
        ylabels = "Return(%)"
        
        plt.xlabel(xlabels)
        plt.ylabel(ylabels)
        plt.show()
'''        
    def get_data(self):
        data = pd.DataFrame()
        for i in self.CurrencyPairTicker:
            temp = quandl.get(i, start_date = self.start, end_date = self.end )
            data[i] = temp["Value"]
        data.columns = pd.Series(data.columns).map(self.CurrencyPairTickerDict)
        #self.df = data    
'''  

