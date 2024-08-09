# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 07:32:30 2024

@author: Lorenzo
"""
import pandas as pd
import os

def dfToOneRow (df):
    
    df.to_csv("temp.csv", index=False, header=False)
    
    tempStringObj=open("temp.csv",'r')
    tempString=tempStringObj.read()
    tempStringObj.close()
    
    tempStringMod = tempString.replace("\n", ",")
    tempStringMod=tempStringMod[:-1]
    
    tempStringObj=open("temp.csv",'w')
    tempStringObj.write(tempStringMod)
    tempStringObj.close()
    df=pd.read_csv("temp.csv",header=None)
    os.remove("temp.csv")
    return df


def noHeaderDf(df):
    
    df.to_csv("temp.csv",index=False,header=False)
    df=pd.read_csv("temp.csv",header=None)
    os.remove("temp.csv")
    return df