# coding: utf-8
import unicodecsv as csv
from sys import argv
import os.path
import operator
from datetime import datetime
import matplotlib.pyplot as plt
import types


def calculateDictionaryAsPercent(times,totalRows):

    if(totalRows==0):
        raise ValueError("The file does not contain any rows")

    for key,val in times.items():
            times[key]=(float(val)/totalRows)*100

    return times


def readCsvAndCountPercentPerFormItemFromGoogleForms(fileName):
    times={}
    totalRows=0
    with open(fileName,'r') as csvfile:

        csvReader=csv.reader(csvfile, encoding='utf-8');
        csvReader.next()  # skip the first line
        for row in csvReader:
            value=row[1]
            value=value.replace("6","7").replace("27","28");
            if(value in times.keys()):
                times[value]+=1
            else:
                times[value]=1

            totalRows+=1

        return calculateDictionaryAsPercent(times,totalRows)

def isFile(fileName):
    if(not os.path.isfile(fileName)):
        raise ValueError("You must provide a valid filename as parameter")


def plotDataInAPie(dictionaryToPlot):

    fileToWrite=datetime.now().strftime("%f")+".png";
    valuesToDraw=dictionaryToPlot.values();
    keysToDraw=dictionaryToPlot.keys();

    plt.figure(figsize=(20, 20)) # This increases resolution
    plt.style.use('ggplot')
    plt.rcParams['font.size'] = 18.0
    plt.pie(valuesToDraw,autopct='%1.1f%%',labeldistance=0.8)
    plt.legend(keysToDraw,loc=3);
    plt.axis('equal')
    plt.savefig(fileToWrite);

fileName=None

if __name__=="__main__":
    try:
        fileName=argv[1]
        isFile(fileName)
        pass
    except Exception as e:
        print("You must provide a valid filename as parameter")
        raise

finalTimes=readCsvAndCountPercentPerFormItemFromGoogleForms(fileName)

plotDataInAPie(finalTimes);
#print finalTimes
