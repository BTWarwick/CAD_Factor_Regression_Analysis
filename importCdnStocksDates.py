# Import Stock Data for specific dates
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import investpy

#Import stock with ticker 'X', return daily stock returns.
def importCdnStockDataDates(X, start, end):
    safeStart = datetime.strptime(start, '%Y-%m-%d').date() - timedelta(1)
    X = yf.download(X, start=str(safeStart), end=end);
    X_price = X['Adj Close'];
      
    # Import CAD:USD exchange rate.
    CADUSD = investpy.get_currency_cross_historical_data(
        currency_cross='CAD/USD',from_date='17/10/1989',to_date='22/06/2020')
    
    CADUSD.index = pd.to_datetime(CADUSD.index)
    
    # Determine the earliest overlapping start date.
    if (str(CADUSD.index[0])[0:10] > str(safeStart)):
        start = CADUSD.index[0]; 
    
    # Ensure all dates are included in both datasets
    calendar_dates = pd.date_range(start=start, end=end, freq='D');
    
    X_price = X_price.reindex(calendar_dates, method='ffill');
    X_price = X_price.dropna();
    
    CADUSD = CADUSD.reindex(calendar_dates, method='ffill').shift(+1);
    
    X_price = X_price[:] * CADUSD['Close'];
    X_return = X_price.pct_change()[1:];
    
    X_return.to_csv('Test_XIC_USD_returns3.csv')
    
    return X_return

#importCdnStockDataDates('XIC.TO', '2003-02-01','2020-06-22')