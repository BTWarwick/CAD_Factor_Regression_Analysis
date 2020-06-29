# Import AQR Factors for Cdn data.

import pandas as pd
import datetime
import urllib.request

DATASET_FILENAME = "Quality-Minus-Junk-Factors-Daily.xlsx"

def get_AQR_DataSet():
    dataset = None

    with urllib.request.urlopen("https://images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Daily.xlsx") as dataset_file:
        with open(DATASET_FILENAME, "wb") as local_dataset_file:
            content = dataset_file.read()
            local_dataset_file.write(content)
            dataset = pd.read_excel(content,
                                    index_col=0,
                                    usecols=[0,4],
                                    sheet_name=None,
                                    header=None)

    return dataset

def get_AQR_mkt(dataset):
    Mkt = dataset["MKT"]
    Mkt = Mkt[15587:]
    
    # Convert dates to datetime format.
    Mkt.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in Mkt.index)
    
    # Save data
    Mkt.to_csv('Mkt.csv')
    return Mkt

def get_AQR_SMB(dataset):    
    SMB = dataset['SMB']
    SMB = SMB[15717:];
    
    # Convert dates to datetime format.
    SMB.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in SMB.index)
    
    # Save data
    SMB.to_csv('SMB.csv')
    return SMB

def get_AQR_HML(dataset):    
    HML = dataset['HML FF']
    HML = HML[15717:];
    
    # Convert dates to datetime format.
    HML.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in HML.index)
    
    # Save data
    HML.to_csv('HML.csv')
    return HML

def get_AQR_UMD(dataset):
    UMD = dataset['UMD']
    UMD = UMD[15698:];
    
    # Convert dates to datetime format.
    UMD.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in UMD.index)
    
    # Save data
    UMD.to_csv('UMD.csv')
    return UMD    
    
def get_AQR_QMJ(dataset):
    QMJ = dataset['QMJ Factors']
    QMJ = QMJ[8113:];
    
    # Convert dates to datetime format.
    QMJ.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in QMJ.index)
    
    # Save data
    QMJ.to_csv('QMJ.csv')
    return QMJ
    
def get_AQR_RF(dataset):
    RF = dataset['RF']
    RF = RF[19:];
    
    # Convert dates to datetime format.
    RF.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in RF.index)
    
    # Save data
    RF.to_csv('RF.csv')
    return RF

dataset = get_AQR_DataSet()
get_AQR_mkt(dataset)
get_AQR_SMB(dataset)
get_AQR_HML(dataset)
get_AQR_QMJ(dataset)
get_AQR_UMD(dataset)
get_AQR_RF(dataset)
