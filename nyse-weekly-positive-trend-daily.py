"""
This Python script uses the yfinance, pandas, and re (Regular Expressions) libraries to analyze historical stock data from the New York Stock Exchange (NYSE). The function get_stocks_in_range returns a list of stock tickers that meet certain criteria over a specified period.

Here's the process it follows:

The get_stocks_in_range function takes five parameters:

start_date and end_date define the period for which the stock history is analyzed.
min_price and max_price set the range for the stock's closing price.
pct is a percentage that specifies the portion of trading days in which the stock's closing price must exceed its opening price.
The script first downloads a CSV file from a GitHub repository that contains a list of all NYSE stock symbols.

Next, it filters the list of stock symbols, keeping only those that contain only alphanumeric characters.

For each ticker in the filtered list, the script attempts to download the stock's historical data from Yahoo Finance using the yfinance library. If the data cannot be downloaded, the script moves on to the next ticker.

For each downloaded stock history, it creates a new column, open_close_change, that contains the difference between the opening and closing price each day.

The script then checks if all of the closing prices fall within the range defined by min_price and max_price.

If the above condition is met, it then checks if the open_close_change is positive (i.e., the stock's price increased during the day) for at least a pct proportion of the trading days.

If both conditions are met, the ticker is added to the stocks_in_range list.

Finally, the function returns the stocks_in_range list.

Business case:

This function could be used by an investment firm or a financial advisor to filter out stocks that meet certain criteria for their clients or strategies. For instance, it can identify stocks that have consistently closed within a specific price range and demonstrated a certain level of growth (defined as the closing price being higher than the opening price) over a defined period. This can be useful for investors looking for stable stocks that show steady growth over time.
"""

import yfinance as yf
import pandas as pd
import re


def get_stocks_in_range(
    start_date, end_date, min_price, max_price, pct
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
            
            hist["open_close_change"] = hist["Close"] - hist["Open"]

            # check if all close prices are in the desired range
            if (hist["Close"] > min_price).all() and (hist["Close"] < max_price).all():
              # check if open close change is above the zero at least given pct of the time
              if(hist["open_close_change"] > 0).mean() >= pct:
                stocks_in_range.append(ticker)
        except:
            pass

    return stocks_in_range
  
  # This function can be called like this:
  stocks = get_stocks_in_range("2023-05-10", "2023-05-18", 0, 5000000, 1)

  print(f"Stocks which are in positive trend for the last 1 week are, ")
  print(stocks)
