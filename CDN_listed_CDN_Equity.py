# Perform a regression analysis.
from importCdnStock import importCdnStockData
from importCdnStocksDates import importCdnStockDataDates
from importAQR_QMJ import get_AQR_5_Factor_model, get_AQR_3_Factor_model
import statsmodels.api as sm
import pandas as pd

# Define the stock/ETF of interest
x = 'VCN.TO';

# Enter a custom start/end date (optional, if not required, set equal to zero).
# Date must be in the format 'YYYY-MM-DD'.
Custom_start_date = 0;
Custom_end_date = 0;

# Import stock/ETF data.
X_returns = importCdnStockData(x);

# Determine start and end dates.
start_date = X_returns.index[0]
end_date = X_returns.index[len(X_returns.index)-1]

# Get the AQR Factors.
AQR_factors = get_AQR_5_Factor_model(str(start_date)[0:10], str(end_date)[0:10]);
#AQR_factors = get_AQR_3_Factor_model(str(start_date)[0:10], str(end_date)[0:10]);

# Determine the AQR start and end dates.
AQR_start_date = AQR_factors.index[0] 
AQR_end_date = AQR_factors.index[len(AQR_factors.index)-1] 

# Change AQR_start_date and AQR_end_date to datetime format.
AQR_start_date = pd.to_datetime(AQR_start_date)
AQR_end_date = pd.to_datetime(AQR_end_date)


# Ensure that the AQR dates are consistent with the stock dates.
if Custom_start_date==0:
    start_date = max(str(start_date)[0:10], str(AQR_start_date)[0:10])
else:
    Custom_start_date = pd.to_datetime(Custom_start_date)    
    start_date = max(str(start_date)[0:10], str(AQR_start_date)[0:10], str(Custom_start_date)[0:10])
        
if Custom_end_date==0:
    end_date = min(str(end_date)[0:10], str(AQR_end_date)[0:10])
else:
    Custom_end_date = pd.to_datetime(Custom_end_date)
    end_date = min(str(end_date)[0:10], str(AQR_end_date)[0:10], str(Custom_end_date)[0:10])

# Retreive stock returns for the proper time interval in bps.    
X_returns = importCdnStockDataDates(x,start_date, end_date);
AQR_factors = get_AQR_5_Factor_model(str(start_date)[0:10], str(end_date)[0:10]);
#AQR_factors = get_AQR_3_Factor_model(str(start_date)[0:10], str(end_date)[0:10]);

# Eliminate weekends and holidays (excess zeros).
X_returns = X_returns[1:]
AQR_factors = AQR_factors[2:]
AQR_factors['X_returns'] = X_returns.values;
AQR_factors = AQR_factors[AQR_factors['X_returns'] !=0]

# Perform linear regression
X = AQR_factors[['Mkt-RF','SMB','HML','QMJ','UMD']]
#X = AQR_factors[['Mkt-RF','SMB','HML']]
X = sm.add_constant(X)
Y = AQR_factors['X_returns'] - AQR_factors['RF']

model = sm.OLS(Y,X).fit()

print(x)
print('Start Date:', start_date)
print('End Date:', end_date)
print(model.summary())