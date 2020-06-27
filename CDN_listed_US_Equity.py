# Perform a regression analysis.
from importCdnStock import importCdnStockData
from importCdnStocksDates import importCdnStockDataDates
from importFF import get_fama_french
import statsmodels.api as sm
import datetime
import pandas as pd

# Define stock/ETF.
x = 'VFV.TO'

# Enter a custom start/end date (optional, if not required, set equal to zero).
# Date must be in the format 'YYYY-MM-DD'.
Custom_start_date = 0;
Custom_end_date = '2020-04-30';

# Import stock/ETF data.
X_returns = importCdnStockData(x);

# Determine start and end dates.
X_start_date = X_returns.index[0]
X_end_date = X_returns.index[len(X_returns.index)-1]

#Convert the date format to be consistent with FF dataset.
start_date = X_start_date.strftime("%Y%m%d")
end_date = X_end_date.strftime("%Y%m%d")

# Get the FF Factors.
ff_factors = get_fama_french(int(start_date), int(end_date));

# Make indices consistent.
ff_factors.index = (datetime.datetime.strptime(str(i),"%Y%m%d").date() for i in ff_factors.index)

# Determine the FF start and end dates.
ff_start_date = ff_factors.index[0] 
ff_end_date = ff_factors.index[len(ff_factors.index)-1] 

# Change ff_start_date and ff_end_date to datetime format.
ff_start_date = pd.to_datetime(ff_start_date)
ff_end_date = pd.to_datetime(ff_end_date)

# Ensure that the AQR dates are consistent with the stock dates.
if Custom_start_date==0:
    start_date = max(str(X_start_date)[0:10], str(ff_start_date)[0:10])
else:
    Custom_start_date = pd.to_datetime(Custom_start_date)    
    start_date = max(str(X_start_date)[0:10], str(ff_start_date)[0:10], str(Custom_start_date)[0:10])
        
if Custom_end_date==0:
    end_date = min(str(X_end_date)[0:10], str(ff_end_date)[0:10])
else:
    Custom_end_date = pd.to_datetime(Custom_end_date)
    end_date = min(str(X_end_date)[0:10], str(ff_end_date)[0:10], str(Custom_end_date)[0:10])

# Retreive stock returns for the proper time interval in bps.    
X_returns = importCdnStockDataDates(x,start_date, end_date)*100;
ffstart_date = pd.to_datetime(start_date)
ffend_date = pd.to_datetime(end_date)
ffstart_date = ffstart_date.strftime("%Y%m%d")
ffend_date = ffend_date.strftime("%Y%m%d")
ff_factors = get_fama_french(int(ffstart_date), int(ffend_date));

X_returns = X_returns[1:]
ff_factors = ff_factors[2:]

ff_factors['X_returns'] = X_returns.values
ff_factors = ff_factors[ff_factors['X_returns'] !=0]

# Perform linear regression
X = ff_factors[['Mkt-RF','SMB','HML','RMW','CMA']]
X = sm.add_constant(X)
Y = ff_factors['X_returns'] - ff_factors['RF']

model = sm.OLS(Y,X).fit()

print(x)
print('Start Date:', start_date)
print('End Date:', end_date)
print(model.summary())