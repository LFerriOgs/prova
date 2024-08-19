# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:24:22 2024

@author: Lorenzo

"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime 
import pandas as pd
import sys
from io import StringIO
import os

a=os.listdir("csv/")
csvDf=pd.read_csv("csv/"+a[-1])

avrgDf=csvDf.iloc[:,0:6]


vcspDf=csvDf.filter(like='VCSP', axis=1)



# sono arrivato al punto di creare una lista di dataframe con all'interno 
#una sola riga contenente una sola data


gr=csvDf.groupby('dateTime')
keys=list( gr.groups.keys())
finalProfileDf=pd.DataFrame() 

dfProfile=[]

for keyIdx in range (len(keys)):  
    dfProfile.append(gr.get_group(keys[keyIdx]))
    dfProfile[keyIdx]=dfProfile[keyIdx].drop('dateTime',axis='columns'); 
    
    #finalProfileDf=pd.concat([finalProfileDf,dfProfile[keyIdx]],ignore_index=True)
    
    
