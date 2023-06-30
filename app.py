import datetime
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews

st.title("Stock Dash Board")
ticker = st.sidebar.text_input("ticker","AAPL")
start_date = st.sidebar.date_input("Start date",datetime.date(2023,6, 1))
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker,start=start_date,end=end_date)
fig = px.line(data,x=data.index,y=data["Adj Close"],title=ticker)
st.plotly_chart(fig)

pricing_data,fundamental_data,news = st.tabs(["Pricing Data","Fundamental Data","News"])

with pricing_data:
    st.header("Price Movement")
    data2 = data
    data2["% Change"] = data["Adj Close"]/data["Adj Close"].shift(1)-1
    data2.dropna(inplace=True)
    st.write(data2)
    ann_return = data2["% Change"].mean()*252*100
    st.write("Annual Return is ",ann_return.round(2),"%")
    stdv = np.std(data2["% Change"])*np.sqrt(252)*100
    st.write("Annual Standard Deviation is ",stdv.round(2),"%")
    st.write("Risk adj Return is ",ann_return/(stdv*100))

with fundamental_data:
    key = "GADGCICEU79YLO1R"
    fd = FundamentalData(key,output_format="pandas")
    st.subheader("Balance Sheet")
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader("Income Statement")
    income_statement = fd.get_income_statement_annual(ticker)[0]
    ins = income_statement.T[2:]
    ins.columns = list(income_statement.T.iloc[0])
    st.write(ins)
    st.subheader("Cash Flow  Statement")
    cashflow_statement = fd.get_cash_flow_annual(ticker)[0]
    csh = cashflow_statement.T[2:]
    csh.columns = list(cashflow_statement.T.iloc[0])
    st.write(csh)

with news:
    st.header(f'News Of {ticker}')
    sn = StockNews(ticker,save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader("News "+str(i+1))
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        st.write(df_news['title'][i])
        title_sentiment = df_news["sentiment_title"][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news["sentiment_summary"][i]
        st.write(f'News Sentiment {news_sentiment}')
