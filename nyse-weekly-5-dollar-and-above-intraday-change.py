"""
This Python script uses the yfinance, pandas, and re (Regular Expressions) libraries to analyze historical stock data from the New York Stock Exchange (NYSE). The function get_stocks_in_range now returns a list of stock tickers that not only meet specific closing price criteria over a specified period, but also have a certain minimum intraday price change.

Here's the process it follows:

The get_stocks_in_range function now takes six parameters:

start_date and end_date to define the period for which the stock history is analyzed.
min_price and max_price to set the range for the stock's closing price.
min_intraday_change sets the minimum difference between the stock's highest and lowest price within a single day.
pct is a percentage that specifies the portion of trading days where the intraday change must be at least min_intraday_change.
The script first downloads a CSV file from a GitHub repository that contains a list of all NYSE stock symbols.

Next, it filters the list of stock symbols, keeping only those that contain only alphanumeric characters.

For each ticker in the filtered list, the script attempts to download the stock's historical data from Yahoo Finance using the yfinance library. If the data cannot be downloaded, the script moves on to the next ticker.

For each downloaded stock history, it creates a new column, intraday_change, that contains the difference between the highest and lowest price each day.

The script then checks if all of the closing prices fall within the range defined by min_price and max_price.

If the above condition is met, it then checks if the intraday_change is at least min_intraday_change for a pct proportion of the trading days.

If both conditions are met, the ticker is added to the stocks_in_range list.

Finally, the function returns the stocks_in_range list.

The last two lines of the code call the get_stocks_in_range function with specific parameters and print the resulting list of tickers.

Business case:

This function could be used by a trader or a trading firm to filter out stocks that show a certain level of volatility (measured by intraday price change) and also have closing prices within a certain range. This might be useful for strategies that aim to profit from intraday price movements. For instance, the code looks for stocks where the intraday price change is at least $5 for all trading days in the defined period, and the closing price has always been between $0 and $500,000 during the same period. The identified stocks may be suitable for certain types of intraday trading strategies, such as day trading or swing trading.
"""

import yfinance as yf
import pandas as pd
import re


def get_stocks_in_range(
    start_date, end_date, min_price, max_price, min_intraday_change, pct
):
    # NYSE listings can be obtained from a CSV file available online. The URL will need to be replaced with the correct URL for the CSV file.
    url = "https://raw.githubusercontent.com/datasets/nyse-other-listings/master/data/nyse-listed.csv"

    # Use pandas to read the CSV file
    data = pd.read_csv(url)

    tickers = data["ACT Symbol"].tolist()
    # This regular expression matches any string that contains only letters and numbers
    regex = re.compile("^[a-zA-Z0-9]+$")

    # Filter the list of tickers
    filtered_tickers = [ticker for ticker in tickers if regex.match(ticker)]

    stocks_in_range = []

    for ticker in filtered_tickers:
        try:
            stock = yf.Ticker(ticker)
            try:
                hist = stock.history(start=start_date, end=end_date, raise_errors=True)
            except:
                continue

            # calculate intraday price change
            hist["intraday_change"] = hist["High"] - hist["Low"]

            # check if all close prices are in the desired range
            if (hist["Close"] > min_price).all() and (hist["Close"] < max_price).all():
                # check if intraday change is above the threshold at least given pct of the time
                if (hist["intraday_change"] >= min_intraday_change).mean() >= pct:
                    stocks_in_range.append(ticker)
        except:
            pass

    return stocks_in_range
  
  stocks = get_stocks_in_range("2023-05-10", "2023-05-18", 0, 500000, 5, 1)
  print(stocks)
