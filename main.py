# importazione delle librerie
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime 
import calendar
import pandas as pd

#url originali 
urlStringList=["https://nodc.ogs.it/erddap/tabledap/CURRISO_PR.csv?time%2Clatitude%2Clongitude%2Cdepth%2CVCSP%2CVCSP_QC%2CEWCT%2CEWCT_QC%2CNSCT%2CNSCT_QC&time%3E=2024-02-08T16%3A30%3A00Z&orderBy(%22time%22)"];
           #"https://nodc.ogs.it/erddap/tabledap/CURRISO_TS.htmlTable?time%2Clatitude%2Clongitude%2CPRES%2CPRES_QC%2CTEMP%2CTEMP_QC%2CRVFL%2CRVFL_QC&time%3E=2024-07-15T12%3A30%3A00Z&orderBy(%22time%22)"];
df=[]
# definizione del datetime corretto
currentDateTime = datetime.now() 
print(currentDateTime)
dateTimeSeconds=calendar.timegm(currentDateTime.timetuple())
dateTimeSeconds=dateTimeSeconds-20*60
newDateTime=datetime.fromtimestamp(dateTimeSeconds)
print(newDateTime)

# lettura dei dati web attraverso BeautifulSoup
for urlString in urlStringList:
    #urlString="https://nodc.ogs.it/erddap/tabledap/CURRISO_PR.csv?time%2Clatitude%2Clongitude%2Cdepth%2CVCSP%2CVCSP_QC%2CEWCT%2CEWCT_QC%2CNSCT%2CNSCT_QC&time%3E=2024-02-08T16%3A30%3A00Z&orderBy(%22time%22)"

    #composizione della stringa per la query al sito 
    newUrlString=   urlString[:146]+ \
                    newDateTime.strftime("%Y-%m-%dT")+ \
                    newDateTime.strftime("%H")+ \
                    "%3A"+ \
                    newDateTime.strftime("%M")+ \
                    "%3A"+ \
                    newDateTime.strftime("%SZ") +\
                    urlString[170:];

html = urlopen(newUrlString);
Obj = BeautifulSoup(html.read(),'lxml');
df[1]=pd.DataFrame(Obj)

currentDateTimeString=currentDateTime.strftime("%Y-%d-%mT_%H-%M-%S")

csvFileName='ERDDAP_Curriso_Profile_'+currentDateTimeString+'.csv'
with open(csvFileName, 'w', newline='') as file: 
    writer = csv.writer(file)
    writer.writerow(Obj)

print(urlString)
print(newUrlString)
print(Obj)
