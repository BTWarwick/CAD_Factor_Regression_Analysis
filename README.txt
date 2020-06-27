This module performs a factor regression analysis considering the CAD:USD exchange rate.

For Canadian Equities listed on the TSX run CDN_listed_CDN_Equity.py.
For US Equities listed on the TSX run CDN_listed_US_Equity.py.

US equities are analyzed using the Fama-French 5 factor model using the daily data.
Canadian equities are analyzed using AQR data for MKT-RF, SMB, HML(FF), QMJ, and UMD (FF data not available for Canada).

For comparative purposes, the file US_listed_US_Equity replicates the results from portfoliovisualizer.com for US listed US Equities analyzed using the FF 5-factor model with daily data.

X, Custom_start_date, and Custom_end_date can be modified as required by the user. If the user does not wish to enter a custom startor end date, a value of zero will use the longest dataset possible.

Prior to running the scripts, the following lines of code must be executed if their respective packages have yet to be installed:

pip install pandas
pip install numpy
pip install DateTime
pip install statsmodels
pip install urllib3
pip install zipfile37
pip install investpy
pip install yfinance

Prior to running the CDN_listed_CDN_Equity.py script for the first time, run getAQR_QMJ.py to download the AQR dataset onto the local hard drive.
Once the dataset is downloaded, the getAQR_QMJ.py script is not required to be executed unless updated data is required. 

CDN_Factor_Regression.py contains the functions CDN_Listed_CDN_Equity, CDN_Listed_US_Equity, and US_Listed_US_Equity if the user prefers to have everything together in one file.








