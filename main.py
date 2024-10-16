"""
Author: Lorenzo Ferri   09/08/2024

Questo è un programma che estrapola automaticamente i dati dal database ERDDAP 
e crea un csv con, in ogni singola riga, un record di tempo seguito da longitudine
latitudine, i parametri dei vari profili (sempre sulla stessa riga) e i valori 
di time series.
Se il server su cui gira questo script si blocca, esso automaticamente tiene 
conto dell'ultima data effettiva di acquisizione e riprende da quel punto
NB assolutamente non cancellare il file "dateList.txt" o cancellarne il contenuto.

"""

# %% importazione delle librerie

from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime 
import pandas as pd
import sys
from io import StringIO

from dfModifier import noHeaderDf, dfToOneRow

 # %% variabili da settare 

startUrlString=["https://nodc.ogs.it/erddap/tabledap/CURRISO_PR.htmlTable?time%2Clatitude%2Clongitude%2Cdepth%2CVCSP%2CVCSP_QC%2CEWCT%2CEWCT_QC%2CNSCT%2CNSCT_QC&time%3E",
                "https://nodc.ogs.it/erddap/tabledap/CURRISO_TS.htmlTable?time%2Clatitude%2Clongitude%2CPRES%2CPRES_QC%2CTEMP%2CTEMP_QC%2CRVFL%2CRVFL_QC&time%3E"];
endUrlString=["&orderBy(%22time%2Cdepth%22)","&orderBy(%22time%22)"];

# %% controllo dateList per definizione datetime

tempTimeObj=open("dateList.txt",'r')
tempTime=tempTimeObj.read()
tempTimeObj.close()

if tempTime =="":
    print("\nil file dateList deve contenere la data da cui si vuole far partire l'acquisizione del record\n")
    sys.exit()  
    
newDateTime=datetime.strptime(tempTime, "%d-%m-%Y %H:%M:%S")

# %% lettura dei dati web attraverso BeautifulSoup

newUrlString=[]
dfList=[]

try:
    for urlIdx in range(len(startUrlString)):
    
    #-------------------------composizione della stringa per la query al sito 
    
        newUrlString.append(startUrlString[urlIdx]+ \
                    newDateTime.strftime("%Y-%m-%dT")+ \
                    newDateTime.strftime("%H")+ \
                    "%3A"+ \
                    newDateTime.strftime("%M")+ \
                    "%3A"+ \
                    newDateTime.strftime("%SZ") +\
                    endUrlString[urlIdx] );

    # -- creazione oggetto di beatifulsoup e relativo dataframe pandas
        
        html = urlopen(newUrlString[urlIdx]);
        soup= BeautifulSoup(html.read(),'html.parser');
        htmlTable=soup.find_all("table",{"class":"erd commonBGColor nowrap"});
        df=pd.read_html(StringIO(str(htmlTable)))[0];
        dfList.append(df);
except:  
    print("\nnon ci sono nuovi record\n")
    sys.exit()
    
# %% creazione finalDf con data e ora

finalDf=pd.DataFrame()

finalDf['tempDate'] = pd.to_datetime(dfList[1]['time','UTC'], format='%Y-%m-%dT%H:%M:%SZ');
finalDf['date'] = finalDf['tempDate'].dt.strftime('%d/%m/%Y');
finalDf['time'] = finalDf['tempDate'].dt.strftime('%H:%M:%S');
finalDf=finalDf.drop('tempDate',axis='columns');
finalDf['latitude'] = dfList[1]['latitude','degrees_north']
finalDf['longitude'] = dfList[1]['longitude','degrees_east']

#%% elaborazione dataframe con profili  

dfList[0]=dfList[0].drop(['latitude','longitude','VCSP_QC','EWCT_QC','NSCT_QC'],axis='columns');

dfList[0]=noHeaderDf(dfList[0])

profileColoumnName=["time","depth", "VCSP", "EWCT", "NSCT"]
dfList[0]= dfList[0].set_axis(profileColoumnName, axis=1)

gr=dfList[0].groupby('time')
keys=list(gr.groups.keys())
finalProfileDf=pd.DataFrame() 

dfProfile=[]

for keyIdx in range (len(keys)):  
    dfProfile.append(gr.get_group(keys[keyIdx]))
    dfProfile[keyIdx]=dfProfile[keyIdx].drop('time',axis='columns');
    dfProfile[keyIdx].insert(0,"#",list(range(1,len(dfProfile[keyIdx])+1)))

    dfProfile[keyIdx]=dfToOneRow(dfProfile[keyIdx])
    
    finalProfileDf=pd.concat([finalProfileDf,dfProfile[keyIdx]],ignore_index=True)

#%% elaborazione dataframe con timeseries

dfList[1]=dfList[1].drop(['time','latitude','longitude','PRES_QC','TEMP_QC','RVFL_QC'],axis='columns');

dfList[1]=noHeaderDf(dfList[1])

#%% concatenazione diversi dataframe in quello finale

finalDf=pd.concat([finalDf,dfList[1], finalProfileDf],axis=1)    
    
# %% set coloumn name 

startColoumnName=["date","time", "latitude", "longitude"]  
profileColoumnName=[]
for rowIdx in range(int(len(finalProfileDf.columns)/5)):
    profileColoumnName=profileColoumnName+["PROFILE #","DEPTH", "VCSP", "EWCT", "NSCT"]
tsColoumnName=["PRES","TEMP","RVFL"]
finalColoumnName=startColoumnName+tsColoumnName+profileColoumnName
finalDf = finalDf.set_axis(finalColoumnName, axis=1)   

    #%% scrittura del dataframe finale su file

currentDateTimeString=datetime.now().strftime("%m-%d-%Y_%H-%M-%S")    
csvFileName='csv/ERDDAP_CurrIso_'+currentDateTimeString+'.csv'  
  
finalDf.to_csv(csvFileName,index=False)    

endTime=dfList[0].time[len(dfList[0])-1]
endTime=datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%SZ')
timeString=datetime.strftime(endTime, '%d-%m-%Y %H:%M:%S')

tempTimeObj=open("dateList.txt", "w")
tempTimeObj.write(timeString)
tempTimeObj.close() 

