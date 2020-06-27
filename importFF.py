# Import FF Factors

# Pandas to read csv file and other things
import pandas as pd
# Datareader to download price data from Yahoo Finance
# To download the Fama French data from the web
import urllib.request
# To unzip the ZipFile 
import zipfile

def get_fama_french(start_date, end_date):
    # Web url
    ff_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip"
    
    # Download the file and save it
    # We will name it fama_french.zip file
    urllib.request.urlretrieve(ff_url,'fama_french_daily.zip')
    zip_file = zipfile.ZipFile('fama_french_daily.zip', 'r')
    
    # Next we extact the file data
    zip_file.extractall()
    
    # Make sure you close the file after extraction
    zip_file.close()
    
    # Now open the CSV file
    ff_factors = pd.read_csv('F-F_Research_Data_5_Factors_2x3_daily.csv', skiprows = 3, index_col = 0)
    ff_factors = ff_factors.loc[start_date:end_date]
  
    if (ff_factors.index[len(ff_factors.index)-1] < end_date):
        end_date = ff_factors.index[len(ff_factors.index)-1]; 

    ff_start_date = str(start_date)
    ff_end_date = str(end_date)

    ff_start_date = ff_start_date[0:4] + '-'+ff_start_date[4:6]+'-'+ff_start_date[6:8]
    ff_end_date = ff_end_date[0:4] + '-'+ff_end_date[4:6]+'-'+ff_end_date[6:8]
    
    # Ensure all dates are included in both datasets
    calendar_dates = pd.date_range(start=ff_start_date, end=ff_end_date, freq='D');
    
    calendar_dates = calendar_dates.strftime("%Y%m%d")
    calendar_dates = calendar_dates.astype(int)
    

    #ff_factors = ff_factors.reindex(calendar_dates, method='ffill');
    ff_factors = ff_factors.reindex(calendar_dates);
    ff_Factors = ff_factors.loc[:, 'Mkt-RF':'CMA'].fillna(0)
    ff_RF = ff_factors.loc[:, 'RF'].fillna(method='bfill')
    ff_factors = ff_Factors
    ff_factors['RF'] = ff_RF
    
    return ff_factors

#ff_data = get_fama_french(20100630,20200630)

