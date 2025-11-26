import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np


## Define the object of the stock return calculator
class StockReturnCalculator:
    def __init__(self, ticker_symbol, start_date, end_date):
        self.ticker_symbol = ticker_symbol
        self.start_date = start_date
        self.end_date = end_date
        self.price_data = None
        self.close_prices = None
        self.returns = None

    def fetch_price_data(self):
        self.price_data = yf.download(
            self.ticker_symbol,
            start=self.start_date,
            end=self.end_date,
            auto_adjust=False,
        )
        self.close_prices = self.price_data["Adj Close"].iloc[:, 0]

    def calculate_returns(self):
        price_list = self.close_prices.tolist()
        trading_days = len(price_list)
        price_new = price_list[1:trading_days]
        price_old = price_list[0 : trading_days - 1]
        self.returns = [(new - old) / old for new, old in zip(price_new, price_old)]
        return self.returns


## Initial lise the objects for S&P 500, AAPL, and NVDA
snp500 = StockReturnCalculator("^GSPC", "2015-10-01", "2025-09-30")
aapl = StockReturnCalculator("AAPL", "2015-10-01", "2025-09-30")
nvda = StockReturnCalculator("NVDA", "2015-10-01", "2025-09-30")

## Fetch the price of the stocks from 2015-10-01 to 2025-09-30
## Set auto_adjust=False to maintain compatibility with older code structure
snp500.fetch_price_data()
aapl.fetch_price_data()
nvda.fetch_price_data()

## Calculate the returns of the stocks
snp500_daily_return = snp500.calculate_returns()
aapl_daily_return = aapl.calculate_returns()
nvda_daily_return = nvda.calculate_returns()


## Calculate cumulative returns
def calculate_cumulative_returns(daily_returns):
    cumulative = [1.0]  # Start with 100% (0% cumulative return)
    for ret in daily_returns:
        cumulative.append(cumulative[-1] * (1 + ret))
    return cumulative  # Keep the initial 1.0 to include starting point


snp500_cumulative = calculate_cumulative_returns(snp500_daily_return)
aapl_cumulative = calculate_cumulative_returns(aapl_daily_return)
nvda_cumulative = calculate_cumulative_returns(nvda_daily_return)

## Create line plots for cumulative returns
plt.figure(figsize=(12, 8))

## Get all dates (include starting date for cumulative return baseline)
dates = snp500.close_prices.index

## Plot cumulative returns for each stock (convert to percentage)
plt.plot(dates, [(x-1)*100 for x in snp500_cumulative], label="S&P 500 (^GSPC)", alpha=0.8, linewidth=2)
plt.plot(dates, [(x-1)*100 for x in aapl_cumulative], label="Apple (AAPL)", alpha=0.8, linewidth=2)
plt.plot(dates, [(x-1)*100 for x in nvda_cumulative], label="NVIDIA (NVDA)", alpha=0.8, linewidth=2)

## Add horizontal line at y=0 for reference (0% return)
plt.axhline(y=0, color="black", linestyle="--", alpha=0.5, linewidth=1)

## Customize the plot
plt.title(
    "Cummulative Returns Graph (2015-10-01 to 2025-09-30)",
    fontsize=16,
    fontweight="bold",
)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Cummulative Return (%)", fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

## Add average daily returns in the top-right corner
textstr = f"Average Daily Returns:\nS&P 500: {np.mean(snp500_daily_return)*100:.4f}%\nAAPL: {np.mean(aapl_daily_return)*100:.4f}%\nNVDA: {np.mean(nvda_daily_return)*100:.4f}%"
props = dict(boxstyle="round", facecolor="wheat", alpha=0.8)
plt.text(
    0.98,
    0.98,
    textstr,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="top",
    horizontalalignment="right",
    bbox=props,
)

## Format the x-axis to show dates properly
plt.xticks(rotation=45)

## Adjust layout to prevent label cutoff
plt.tight_layout()

## Show the plot
plt.show()
