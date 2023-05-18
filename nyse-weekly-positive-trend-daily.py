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
