# Import Complete Historical Stock Data
import pandas as pd
import yfinance as yf
import investpy


#Import stock with ticker 'X', return daily stock returns.
def importCdnStockData(X):
    X = yf.download(X);
    X_price = X['Adj Close'];
    start = X_price.index[0];
    end = X_price.index[len(X_price.index)-1];
    
    # Import currency data.
    CADUSD = investpy.get_currency_cross_historical_data(
        currency_cross='CAD/USD',from_date='17/10/1989',to_date='22/06/2020')
    
    CADUSD.index = pd.to_datetime(CADUSD.index)
    
    # Determine the earliest overlapping start date.
    if (CADUSD.index[0] > start):
        start = CADUSD.index[0]; 
    
    # Ensure all dates are included in both datasets
    calendar_dates = pd.date_range(start=start, end=end, freq='D');
    
    X_price = X_price.reindex(calendar_dates, method='ffill');
    X_price = X_price.dropna();
    
    CADUSD = CADUSD.reindex(calendar_dates, method='ffill').shift(+1);

    X_price = X_price[:] * CADUSD['Close'];
    X_return = X_price.pct_change()[1:];
    
    return X_return

importCdnStockData('XIC.TO')