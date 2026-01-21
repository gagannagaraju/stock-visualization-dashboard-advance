
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import fetch_stock_data, calculate_rsi, calculate_macd, calculate_beta, calculate_dcf

st.set_page_config(page_title="Advanced Stock Dashboard", layout="wide")
st.title("📊 Advanced Stock Analysis Dashboard")

ticker = st.text_input("Stock Ticker (AAPL, MSFT, INFY.NS)", value="AAPL")
market = st.text_input("Market Index for Beta (e.g. ^GSPC or ^NSEI)", value="^GSPC")

start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if ticker and start_date and end_date:
    df = fetch_stock_data(ticker, start_date, end_date)

    if not df.empty:
        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA50"] = df["Close"].rolling(50).mean()
        df["RSI"] = calculate_rsi(df)
        df["MACD"], df["Signal"] = calculate_macd(df)

        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df["Date"], open=df["Open"], high=df["High"],
                                     low=df["Low"], close=df["Close"], name="Price"))
        fig.add_trace(go.Scatter(x=df["Date"], y=df["MA20"], name="MA 20"))
        fig.add_trace(go.Scatter(x=df["Date"], y=df["MA50"], name="MA 50"))
        fig.update_layout(title=f"{ticker} Price & Moving Averages")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Technical Indicators")
        st.line_chart(df[["RSI"]].dropna())
        st.line_chart(df[["MACD", "Signal"]].dropna())

        returns = df["Close"].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)

        beta = calculate_beta(ticker, market, start_date, end_date)

        st.subheader("Valuation Metrics")
        st.write(f"Annualized Volatility: {volatility:.2%}")
        st.write(f"Beta vs Market: {beta:.2f}")

        st.subheader("DCF Valuation")
        intrinsic_value = calculate_dcf(df)
        st.write(f"Estimated Intrinsic Value per Share: ₹{intrinsic_value:.2f}")
