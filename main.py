# importazione delle librerie
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime 
import calendar
import pandas as pd

# variabili da settare 
minutes=50;
startUrlString=["https://nodc.ogs.it/erddap/tabledap/CURRISO_PR.htmlTable?time%2Clatitude%2Clongitude%2Cdepth%2CVCSP%2CVCSP_QC%2CEWCT%2CEWCT_QC%2CNSCT%2CNSCT_QC&time%3E=",
                    "https://nodc.ogs.it/erddap/tabledap/CURRISO_TS.htmlTable?time%2Clatitude%2Clongitude%2CPRES%2CPRES_QC%2CTEMP%2CTEMP_QC%2CRVFL%2CRVFL_QC&time%3E="];
endUrlString=["&orderBy(%22time%2Cdepth%22)","&orderBy(%22time%22)"];
newUrlString=[]

dfList=[]
finalDf=pd.DataFrame()

# definizione del datetime corretto
currentDateTime = datetime.now() 
print(currentDateTime)


dateTimeSeconds=calendar.timegm(currentDateTime.timetuple())
dateTimeSeconds=dateTimeSeconds-minutes*60
newDateTime=datetime.fromtimestamp(dateTimeSeconds)
print(newDateTime)

# lettura dei dati web attraverso BeautifulSoup
for urlIdx in range(len(startUrlString)):
    
    #composizione della stringa per la query al sito 
    newUrlString.append(startUrlString[urlIdx]+ \
                    newDateTime.strftime("%Y-%m-%dT")+ \
                    newDateTime.strftime("%H")+ \
                    "%3A"+ \
                    newDateTime.strftime("%M")+ \
                    "%3A"+ \
                    newDateTime.strftime("%SZ") +\
                    endUrlString[urlIdx] );
    print(newUrlString[urlIdx])

    #creazione oggetto di beatifulsoup e relativo dataframe pandas
    html = urlopen(newUrlString[urlIdx]);
    soup= BeautifulSoup(html.read(),'html.parser');
    htmlTable=soup.find_all("table",{"class":"erd commonBGColor nowrap"});
    df=pd.read_html(str(htmlTable))[0];
    dfList.append(df);
    
    
# elaborazione del dataframe finale 
finalDf['tempDate'] = pd.to_datetime(dfList[1]['time','UTC'], format='%Y-%m-%dT%H:%M:%SZ');  
finalDf['date'] = finalDf['tempDate'].dt.strftime('%d/%m/%Y');
finalDf['time'] = finalDf['tempDate'].dt.strftime('%H:%M:%S');
finalDf=finalDf.drop('tempDate',axis='columns');
finalDf['latitude'] = dfList[1]['latitude','degrees_north']
finalDf['longitude'] = dfList[1]['longitude','degrees_east']


for rowIdx in range(len(dfList[0])):
    
    # prova esportare csv 
    
    # da qui è da controllare 
    tempDf=dfList[0].iloc[2:3,3:9]
    ccc=pd.concat([finalDf,tempDf],axis=0)
    finalDf=finalDf.join(tempDf)
    horizontal_concat = pd.concat([finalDf, tempDf], axis=1)
    vvv=[finalDf,tempDf]
    
print(finalDf)


# salvataggio in formato csv 
currentDateTimeString=currentDateTime.strftime("%Y-%d-%mT_%H-%M-%S")

csvFileName='ERDDAP_Curriso_Profile_'+currentDateTimeString+'.csv'
with open(csvFileName, 'w', newline='') as file: 
    writer = csv.writer(file)
    writer.writerow(soup)














