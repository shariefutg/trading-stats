"""
This Python script uses the yfinance, pandas, and re (Regular Expressions) libraries to analyze historical stock data from the New York Stock Exchange (NYSE). The function get_stocks_in_range returns a list of stock tickers that meet certain criteria over a specified period.

Here's the process it follows:

The get_stocks_in_range function takes six parameters:

start_date and end_date define the period for which the stock history is analyzed.
min_price and max_price set the range for the stock's closing price.
min_intraday_change is a threshold for the daily price change.
pct is a percentage that specifies the portion of trading days in which the stock's intraday price change must exceed the threshold.
The script first downloads a CSV file from a GitHub repository that contains a list of all NYSE stock symbols.

Next, it filters the list of stock symbols, keeping only those that contain only alphanumeric characters.

For each ticker in the filtered list, the script attempts to download the stock's historical data from Yahoo Finance using the yfinance library. If the data cannot be downloaded, the script moves on to the next ticker.

For each downloaded stock history, it creates a new column, intraday_change, that contains the difference between the highest and lowest price each day.

The script then checks if all of the closing prices fall within the range defined by min_price and max_price.

If the above condition is met, it then checks if the intraday_change is greater than or equal to min_intraday_change for at least a pct proportion of the trading days.

If both conditions are met, the ticker is added to the stocks_in_range list.

Finally, the function returns the stocks_in_range list.

In the last part of the script, the function get_stocks_in_range is called with parameters specifying a date range from May 10 to May 18, 2023, a closing price range from 0 to 500000, a minimum intraday change of 10, and a percentage of 1 (which means 100% of the trading days). The result is stored in the stocks variable and printed out.

Business case:

This function could be used by traders, investment firms, or financial advisors to identify stocks with significant intraday price volatility. This can be especially useful for day traders or swing traders who seek to profit from these intraday price changes. For instance, they might be looking for stocks that have shown a consistent pattern of significant intraday price changes. Furthermore, the feature that checks the closing price to remain within a certain range can help them avoid extremely high or low-priced stocks
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
  
  stocks = get_stocks_in_range("2023-05-10", "2023-05-18", 0, 500000, 10, 1)
  print(stocks)
