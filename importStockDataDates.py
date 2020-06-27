# Import Stock Data for specific dates
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


#Import stock with ticker 'X', return daily stock returns.
def importStockDataDates(X, start, end):
    safeStart = datetime.strptime(start, '%Y-%m-%d').date() - timedelta(1)
    X = yf.download(X, start=str(safeStart), end=end);
    X_price = X['Adj Close'];
    
    # Ensure all dates are included in both datasets
    calendar_dates = pd.date_range(start=start, end=end, freq='D');
    
    X_price = X_price.reindex(calendar_dates, method='ffill');
    X_price = X_price.dropna();
    X_return = X_price.pct_change()[1:];
    
    return X_return
