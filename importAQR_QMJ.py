# Import AQR Factors for Cdn data.

import pandas as pd 
import datetime

def get_AQR_mkt():
    Mkt = pd.read_excel("https://images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Daily.xlsx",
                        index_col=0,
                        usecols=[0,4],
                        sheet_name='MKT',
                        header=None)
    Mkt = Mkt[15587:];
    
    # Convert dates to datetime format.
    Mkt.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in Mkt.index)
    
    # Save data
    Mkt.to_csv('Mkt.csv')
    return Mkt

def get_AQR_SMB():    
    SMB = pd.read_excel("https://images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Daily.xlsx",
                        index_col=0,
                        usecols=[0,4],
                        sheet_name='SMB',
                        header=None)
    SMB = SMB[15717:];
    
    # Convert dates to datetime format.
    SMB.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in SMB.index)
    
    # Save data
    SMB.to_csv('SMB.csv')
    return SMB

def get_AQR_HML():    
    HML = pd.read_excel("https://images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Daily.xlsx",
                        index_col=0,
                        usecols=[0,4],
                        sheet_name='HML FF',
                        header=None)
    HML = HML[15717:];
    
    # Convert dates to datetime format.
    HML.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in HML.index)
    
    # Save data
    HML.to_csv('HML.csv')
    return HML

def get_AQR_UMD():
    UMD = pd.read_excel("https://images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Daily.xlsx",
                        index_col=0,
                        usecols=[0,4],
                        sheet_name='UMD',
                        header=None)
    UMD = UMD[15698:];
    
    # Convert dates to datetime format.
    UMD.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in UMD.index)
    
    # Save data
    UMD.to_csv('UMD.csv')
    return UMD    
    
def get_AQR_QMJ():
    QMJ = pd.read_excel("https://images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Daily.xlsx",
                        index_col=0,
                        usecols=[0,4],
                        sheet_name='QMJ Factors',
                        header=None)
    QMJ = QMJ[8113:];
    
    # Convert dates to datetime format.
    QMJ.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in QMJ.index)
    
    # Save data
    QMJ.to_csv('QMJ.csv')
    return QMJ
    
def get_AQR_RF():
    RF = pd.read_excel("https://images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Daily.xlsx",
                        index_col=0,
                        usecols=[0,1],
                        sheet_name='RF',
                        header=None)
    RF = RF[19:];
    
    # Convert dates to datetime format.
    RF.index = (datetime.datetime.strptime(str(i),"%m/%d/%Y").date() for i in RF.index)
    
    # Save data
    RF.to_csv('RF.csv')
    return RF
    
def get_AQR_3_Factor_model(start_date, end_date):
    MKT = pd.read_csv('Mkt.csv',index_col=0,skiprows=1,header=None)
    SMB = pd.read_csv('SMB.csv',index_col=0,skiprows=1,header=None)
    HML = pd.read_csv('HML.csv',index_col=0,skiprows=1,header=None)
    RF = pd.read_csv('RF.csv',index_col=0,skiprows=1,header=None)
    
    # Choose start date and end date such that there is complete overlap.
    start_date = max(MKT.index[0],SMB.index[0],HML.index[0],RF.index[0],start_date)
    end_date = min(MKT.index[len(MKT.index)-1],SMB.index[len(SMB.index)-1],HML.index[len(HML.index)-1],RF.index[len(RF.index)-1],end_date)
    
    MKT = MKT[1][start_date:end_date]
    SMB = SMB[1][start_date:end_date]
    HML = HML[1][start_date:end_date]
    RF = RF[1][start_date:end_date]
    
    # Ensure all dates are included in both datasets
    calendar_dates = pd.date_range(start=start_date, end=end_date, freq='D');
    
    calendar_dates = calendar_dates.strftime("%Y-%m-%d")

    MKT = MKT.reindex(calendar_dates);
    SMB = SMB.reindex(calendar_dates);
    HML = HML.reindex(calendar_dates);
    RF = RF.reindex(calendar_dates);
    
    MKT = MKT.fillna(0)
    SMB = SMB.fillna(0)
    HML = HML.fillna(0)
    RF = RF.fillna(method='bfill')
    
    AQR_factors = pd.concat([MKT, SMB, HML, RF], axis=1, sort=False);
    AQR_factors.columns = ['Mkt-RF', 'SMB', 'HML', 'RF']
    
    return AQR_factors

    
def get_AQR_5_Factor_model(start_date, end_date):
    MKT = pd.read_csv('Mkt.csv',index_col=0,skiprows=1,header=None)
    SMB = pd.read_csv('SMB.csv',index_col=0,skiprows=1,header=None)
    HML = pd.read_csv('HML.csv',index_col=0,skiprows=1,header=None)
    QMJ = pd.read_csv('QMJ.csv',index_col=0,skiprows=1,header=None)
    UMD = pd.read_csv('UMD.csv',index_col=0,skiprows=1,header=None)
    RF = pd.read_csv('RF.csv',index_col=0,skiprows=1,header=None)
    
    # Choose start date and end date such that there is complete overlap.
    start_date = max(MKT.index[0],SMB.index[0],HML.index[0],RF.index[0],QMJ.index[0],UMD.index[0],start_date)
    end_date = min(MKT.index[len(MKT.index)-1],SMB.index[len(SMB.index)-1],HML.index[len(HML.index)-1],QMJ.index[len(QMJ.index)-1],UMD.index[len(UMD.index)-1],RF.index[len(RF.index)-1],end_date)
    
    MKT = MKT[1][start_date:end_date]
    SMB = SMB[1][start_date:end_date]
    HML = HML[1][start_date:end_date]
    QMJ = QMJ[1][start_date:end_date]
    UMD = UMD[1][start_date:end_date]
    RF = RF[1][start_date:end_date]
    
    # Ensure all dates are included in both datasets
    calendar_dates = pd.date_range(start=start_date, end=end_date, freq='D');
    
    calendar_dates = calendar_dates.strftime("%Y-%m-%d")

    MKT = MKT.reindex(calendar_dates);
    SMB = SMB.reindex(calendar_dates);
    HML = HML.reindex(calendar_dates);
    QMJ = QMJ.reindex(calendar_dates);
    UMD = UMD.reindex(calendar_dates);
    RF = RF.reindex(calendar_dates);
    
    MKT = MKT.fillna(0)
    SMB = SMB.fillna(0)
    HML = HML.fillna(0)
    QMJ = QMJ.fillna(0)
    UMD = UMD.fillna(0)
    RF = RF.fillna(method='bfill')
    
    AQR_factors = pd.concat([MKT, SMB, HML, QMJ, UMD, RF], axis=1, sort=False);
    AQR_factors.columns = ['Mkt-RF', 'SMB', 'HML', 'QMJ', 'UMD', 'RF']
    
    return AQR_factors
    

#get_AQR_5_Factor_model('1972-01-01','2020-04-30')


