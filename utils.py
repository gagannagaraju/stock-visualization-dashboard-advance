
import yfinance as yf
import numpy as np
import pandas as pd

def fetch_stock_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    df.reset_index(inplace=True)
    return df

def calculate_rsi(df, period=14):
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(df):
    ema12 = df["Close"].ewm(span=12).mean()
    ema26 = df["Close"].ewm(span=26).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()
    return macd, signal

def calculate_beta(stock, market, start, end):
    stock_returns = yf.download(stock, start=start, end=end)["Close"].pct_change().dropna()
    market_returns = yf.download(market, start=start, end=end)["Close"].pct_change().dropna()
    cov = np.cov(stock_returns, market_returns)[0][1]
    var = np.var(market_returns)
    return cov / var

def calculate_dcf(df):
    fcf = df["Close"].pct_change().mean() * 100  # proxy cash flow growth
    discount_rate = 0.10
    terminal_growth = 0.04
    terminal_value = fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
    return terminal_value
