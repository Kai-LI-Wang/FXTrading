#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:46:50 2021

@author: kelly
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 17:49:34 2021

@author: kelly
"""
import pandas as pd 
import numpy as np 
import warnings

warnings.simplefilter("ignore")
warnings.filterwarnings("ignore")
#pd.set_option('display.max_rows', None)

class Signal():
    def __init__(self, data,kind, ratio, indicator,BB_std , rolling_window, currencypair):
        self.data = data
        self.kind = kind
        self.Ratio = ratio 
        self.indicator = indicator
        self.BB_std = BB_std
        self.rolling_window = rolling_window
        self.CurrencyPair = currencypair
        self.TicketCounter = 0
        self.BuyPosition = 0
        self.SellPosition = 0        
        self.TradeTicket = 0
        self.dataframe = self.train_test_split()
        self.indicator_data = self.TechnicalIndicator()
        
    def __repr__(self):
        return "Indicator: [Bolliger Band, Moving Average]" 
    
    def train_test_split(self):
        t = int(self.data.shape[0]*self.Ratio)
        if self.kind == "train": 
            train = self.data.iloc[:t,:]
            return train 
        elif self.kind == "test": 
            test = self.data.iloc[t:,:]
            return test
        
    def TechnicalIndicator(self):
        IndicatorDict = {"BB":"BollingerBand", "MA": "MovingAverage"}
        df = pd.DataFrame(columns = ["Close","Open", 'BollingerUpperBand','BollingerLowerBand','Rolling Mean'])
       
        if IndicatorDict[self.indicator] == "BollingerBand":
            Rolling_mean = self.dataframe[self.CurrencyPair + "_Close"].rolling(window = self.rolling_window).mean()
            df['Rolling Mean'] = Rolling_mean
            df["Close"] = self.dataframe[self.CurrencyPair + "_Close"]
            df["Open"] = self.dataframe[self.CurrencyPair + "_Open"]
            Rolling_std = self.dataframe[self.CurrencyPair + "_Close"].rolling(window = self.rolling_window).std()
            df['BollingerUpperBand'] = Rolling_mean + (Rolling_std * self.BB_std)
            df['BollingerLowerBand'] = Rolling_mean - (Rolling_std * self.BB_std)
            df.dropna(inplace = True, axis = 0 )
            
        elif IndicatorDict[self.indicator] == "Moving Average":
            pass
        
        return df 
    
    def ProfitLoss(self,  row,indicator_data, TradeTicketDict ):
        StopLossPips = 250          
        TakeProfit = 500 
        
        if TradeTicketDict.shape[0] > 0:
            PriceDiff  = indicator_data["Close"].iloc[row] - TradeTicketDict["Price"].iloc[self.TicketCounter-1]
        else:
            PriceDiff = 0            
        if self.TicketCounter < 4:
            Minumum = 0        
        else: 
            Minumum = self.TicketCounter-4 
            
        for i in range(self.TicketCounter-1,Minumum-1,  -1):                        
            if  (TradeTicketDict["BuySell"].iloc[i] == "Buy"):    
                if (PriceDiff < -StopLossPips*0.0001) and (TradeTicketDict["OpenClose"].iloc[i] == 1): # open = 1, close = 0
                    TradeTicketDict["P&L(USD)"].iloc[i] = PriceDiff/indicator_data["Close"].iloc[row]
                    TradeTicketDict["OpenClose"].iloc[i] = 0 
                    TradeTicketDict["ClosePosPrice"].iloc[i] = indicator_data["Close"].iloc[row]
                    self.BuyPosition = 0                    
                    
                elif (PriceDiff > TakeProfit*0.0001) and (TradeTicketDict["OpenClose"].iloc[i] == 1): 
                    TradeTicketDict["P&L(USD)"].iloc[i] = PriceDiff/indicator_data["Close"].iloc[row]
                    TradeTicketDict["OpenClose"].iloc[i] = 0
                    TradeTicketDict["ClosePosPrice"].iloc[i] = indicator_data["Close"].iloc[row]
                    self.BuyPosition = 0                    
                                        
            elif (TradeTicketDict["BuySell"].iloc[i] == "Sell"):
                if (PriceDiff > StopLossPips*0.0001) and (TradeTicketDict["OpenClose"].iloc[i] == 1): # open = 1, close = 0
                    TradeTicketDict["P&L(USD)"].iloc[i] = -PriceDiff/indicator_data["Close"].iloc[row]
                    TradeTicketDict["OpenClose"].iloc[i] = 0 
                    TradeTicketDict["ClosePosPrice"].iloc[i] = indicator_data["Close"].iloc[row]                   
                    self.SellPosition = 0                    
                    
                elif (PriceDiff < -TakeProfit*0.0001) and (TradeTicketDict["OpenClose"].iloc[i] == 1): 
                    TradeTicketDict["P&L(USD)"].iloc[i] = -PriceDiff/indicator_data["Close"].iloc[row]
                    TradeTicketDict["OpenClose"].iloc[i] = 0
                    TradeTicketDict["ClosePosPrice"].iloc[i] = indicator_data["Close"].iloc[row]
                    self.SellPosition = 0
                             
        return TradeTicketDict
        
    
    def Strategy(self):
        TradeTicketDict = pd.DataFrame(columns = ["TradeTicket","BuySell","OpenClose","BollogerPosition","Price","ClosePosPrice",  "P&L(USD)"],index = np.arange(200))
        counter = 0
        
        for row in range(3,self.indicator_data.shape[0]):
            counter += 1
            Momentum = 0
            SellReversal = 0
            BuyReversal = 0
            
            CurOpenClose = abs(self.indicator_data["Close"].iloc[row] - self.indicator_data['Open'].iloc[row])
            PreOpenCloseOne = abs(self.indicator_data["Close"].iloc[row-1] - self.indicator_data['Open'].iloc[row-1])
            PreOpenCloseTwo = abs(self.indicator_data["Close"].iloc[row-2] - self.indicator_data['Open'].iloc[row-2])
            PreOpenCloseThree = abs(self.indicator_data["Close"].iloc[row-3] - self.indicator_data['Open'].iloc[row-3])
            TradeTicketDict = self.ProfitLoss(row,self.indicator_data, TradeTicketDict)
         
            if (CurOpenClose > np.mean(PreOpenCloseOne+PreOpenCloseTwo)):
                Momentum += 1 
            
            if (self.indicator_data['Close'].iloc[row] > self.indicator_data['BollingerUpperBand'].iloc[row]) \
                and (self.indicator_data['Close'].iloc[row-1] < self.indicator_data['BollingerUpperBand'].iloc[row-1]):
                SellReversal = 1
                
            elif (self.indicator_data['Close'].iloc[row] < self.indicator_data['BollingerLowerBand'].iloc[row]) \
                and (self.indicator_data['Close'].iloc[row-1] > self.indicator_data['BollingerLowerBand'].iloc[row-1]): 
                BuyReversal = 1 
                
            if  (BuyReversal+Momentum > 1) and (self.BuyPosition == 0) : 
                self.BuyPosition = 1
                self.TradeTicket += 10  
                TradeTicketDict["OpenClose"].iloc[self.TicketCounter] = 1 
                TradeTicketDict["TradeTicket"].iloc[self.TicketCounter] = self.TradeTicket
                TradeTicketDict["BuySell"].iloc[self.TicketCounter] = "Buy"
                TradeTicketDict["Price"].iloc[self.TicketCounter] = self.indicator_data["Close"].iloc[row]
                self.TicketCounter += 1 
            
            elif (SellReversal+Momentum > 1) and (self.SellPosition == 0):    
                self.ＳellPosition = 1 
                self.TradeTicket += 10   
                TradeTicketDict["OpenClose"].iloc[self.TicketCounter] = 1 
                TradeTicketDict["TradeTicket"].iloc[self.TicketCounter] = self.TradeTicket
                TradeTicketDict["BuySell"].iloc[self.TicketCounter] = "Sell"
                TradeTicketDict["Price"].iloc[self.TicketCounter] = self.indicator_data["Close"].iloc[row]
                self.TicketCounter += 1 
            
        return  TradeTicketDict                  
                     
              
                          

