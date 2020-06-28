#!/bin/sh -e

cd "`dirname $0`"
MODULES="pandas numpy statsmodels zipfile37 investpy yfinance xlrd"
VENV_PATH="$PWD/venv"
SENTINEL_PATH="$VENV_PATH/.setupdone"

if [ -f "$SENTINEL_PATH" ] && [[ $(< "$SENTINEL_PATH") == "$MODULES" ]]
then
  . "$VENV_PATH/bin/activate"
else
  echo "Creating virtual environment"
  rm -rf "$VENV_PATH"
  python3 -m venv "$VENV_PATH"
  . "$VENV_PATH/bin/activate"
  pip3 install --upgrade pip
  pip3 install $MODULES
  echo "$MODULES" > "$SENTINEL_PATH"
fi

if [ ! -f "Mkt.csv" ]
then
  echo "Downloading AQR data files"
  python3 getAQR_QMJ.py
fi

python3 CDN_listed_CDN_Equity.py
