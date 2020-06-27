# Import Complete Historical Stock Data
import pandas as pd
import yfinance as yf

#Import stock with ticker 'X', return daily stock returns.
def importStockData(X):
    X = yf.download(X);
    X_price = X['Adj Close'];
    
    # Ensure all dates are included in both datasets
    calendar_dates = pd.date_range(start=X.index[0], end=X.index[len(X.index)-1], freq='D');
    
    X_price = X_price.reindex(calendar_dates, method='ffill');
    X_price = X_price.dropna();
    X_return = X_price.pct_change()[1:];
    
    return X_return