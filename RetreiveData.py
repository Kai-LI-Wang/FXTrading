#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:30:11 2021

@author: kelly
"""
import pandas_datareader.data as pdr 
import quandl 
import pandas as pd 

quandl.ApiConfig.api_key = "PXoA79qRmDpA5sMhVmZz"

class GetData():
    
    def __init__(self, start_date, end_date, currency_pair, api, application):
        self.StartDate = start_date
        self.EndDate = end_date 
        self.CurrencyPair = currency_pair
        self.api = api 
        self.application = application 
        
    def CurrencyPairTicker(self):
    
        CurrencyPairTickerQuandl = { "USDJPY":'BOE/XUDLJYD', "AUDUSD":"RBA/FXRUSD", "EURUSD":"ECB/EURUSD" }
        CurrencyPairTickerYahoo = {"USDJPY":'USDJPY=X', "AUDUSD":"AUDUSD=X", "EURUSD":"EURUSD=X"}
        data = pd.DataFrame()
        
        for i in self.CurrencyPair:
            if self.api == "Quandl":  
                df = quandl.get(CurrencyPairTickerQuandl[i], start_date = self.StartDate, end_date = self.EndDate) 
                data = pd.concat([data, df[['Value']]], axis = 1)
                data.rename(columns = {"Value":i}, inplace = True)
            elif self.api == "Yahoo":
                df = pdr.DataReader(CurrencyPairTickerYahoo[i],"yahoo" ,self.StartDate, self.EndDate)    
                if self.application == "strategy":
                    data = pd.concat([data, df[['Open', 'Adj Close']]], axis = 1)
                    data.rename(columns = {"Open":i+"_Open", "Adj Close": i+"_Close"}, inplace = True)
                elif self.application == "assetallocation":
                    data = pd.concat([data, df[ 'Adj Close']], axis = 1)
                    data.rename(columns = {"Adj Close": i}, inplace = True)
        

        return pd.DataFrame(data)
       
        
        
   
'''  
import datetime as dt 
start = dt.datetime(2019,1,1)
end = dt.datetime(2021,2,20)
currencypair = ["USDJPY","AUDUSD","EURUSD"]

a = GetData(start ,end, currencypair, "Yahoo", "assetallocation")
a.CurrencyPairTicker()
'''        

