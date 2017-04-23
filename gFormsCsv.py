# coding: utf-8
import unicodecsv as csv
from sys import argv
import os.path
import operator
from datetime import datetime
import matplotlib.pyplot as plt
import types
import json
import argparse

def isFile(fileName):
    if(not os.path.isfile(fileName)):
        raise ValueError("You must provide a valid filename as parameter")




def loadReplacementStrings(fileName):
    try:
        isFile(fileName)
        with open(fileName,'r') as jsonFile:
            try:
                jsonReader=json.load(jsonFile)
                return jsonReader;
            except Exception as e:
                raise
        pass
    except Exception as e:
        return {}


def calculateDictionaryAsPercent(times,totalRows):

    if(totalRows==0):
        raise ValueError("The file does not contain any rows")

    for key,val in times.items():
            times[key]=(float(val)/totalRows)*100

    return times

'''
    @parameter fileName a csv file that each row haw a specific value we want to count

    @return dictionary with the following format
    {
        'csvValue1':how_parcent_found1,
        'csvValue2':how_percent_found2,
        ...
        'csvValuen':how_percent_foundn
    }
'''
def readCsvAndCountPercentPerFormItemFromGoogleForms(fileName):
    times={}
    totalRows=0
    with open(fileName,'r') as csvfile:

        csvReader=csv.reader(csvfile, encoding='utf-8');
        csvReader.next()  # skip the first line
        for row in csvReader:
            value=row[1]

            '''
             Because I did some mistakes and fixed later on google forms
             I replace the 6 with 7 and 27 with 28 because I mistoon the dates
             of the sundays.
            '''
            value=value.replace("6","7").replace("27","28");
            if(value in times.keys()):
                times[value]+=1
            else:
                times[value]=1

            totalRows+=1

        return calculateDictionaryAsPercent(times,totalRows)


'''
    @parameter dictionary dictionaryToPlot a dictionary that has values in the following format:
    {
     "key1": numeric_value1,
     "key2": numeric_value2,
     ...
     "keyn": numeric_valuen
    }
'''
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
replacements=None

# if __name__=="__main__":
#     try:
#         fileName=argv[1]
#         isFile(fileName)
#         pass
#     except Exception as e:
#         print("You must provide a valid filename as parameter")
#         raise

parser=argparse.ArgumentParser(description='Script that reads the files from google forms csv plotsd into a pie')
parser.add_argument('csv_file',metavar="FILENAME", type=str,help="The google's csv file")
parser.add_argument('--replacements',type=str,help="Optional json file that allows you to create replacements for csv's values")
args=parser.parse_args()

replacements=loadReplacementStrings(args.replacements)
print replacements
finalTimes=readCsvAndCountPercentPerFormItemFromGoogleForms(args.csv_file)


plotDataInAPie(finalTimes);
#print finalTimes
