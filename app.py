from flask import Flask, render_template, request, jsonify
from db_setup import save_stock_data_to_db
import yfinance as yf # Yahoo Finance
import pandas as pd # Pandas
import sqlite3 # SQLite
from datetime import datetime 
import json


app = Flask(__name__)

def fetch_stock_data(ticker, time_period, time_interval):
    try:
        # Fetch historical stock data for the past month
        stock_data = yf.download(ticker, period=time_period, interval=time_interval)
        
        # Check if the stock data is empty
        if stock_data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def generate_stock_history_dict(ticker, time_period, time_interval, stock_history):
    # Create Ticker for Specific Stock
    stock = yf.Ticker(ticker)
    
    # Check if stock_history is empty
    if stock_history.empty:
        return jsonify({"error": "No data found for the requested ticker."}), 404
    # Ensure the index is a datetime index
    try:
        stock_history.index = pd.to_datetime(stock_history.index)
    except Exception as e:
        return jsonify({"error": f"Failed to convert index to datetime: {str(e)}"}), 500

    # Getting the daily data for the stock
    try:
        daily_data = stock.history(period="5d")
        if daily_data.empty or len(daily_data) < 2:
            print(daily_data)
            return jsonify({"error": "Not enough data available for the requested ticker."}), 404

        print("Daily Data:", daily_data)
        # Replaced negative indexing with .iloc[] for accessing elements in the daily_data, so no errors are run into
        
        # Convert numpy types to native Python types
        current_price = float(daily_data['Close'].iloc[-1]) # Last Closing Price
        open_price = float(daily_data['Open'].iloc[-1])
        high_price = float(daily_data['High'].iloc[-1])
        low_price = float(daily_data['Low'].iloc[-1])
        previous_close = float(daily_data['Close'].iloc[-2]) if len(daily_data) > 1 else None  # Previous day's close
        volume = int(daily_data['Volume'].iloc[-1]) if not daily_data['Volume'].empty else 0
        market_cap = stock.info.get('marketCap', 0)
        pe_ratio = stock.info.get('forwardPE', None)  # You can also use 'trailingPE'
        eps = stock.info.get('trailingEps', None)
        dividend_yield = stock.info.get('dividendYield', None)
        year_high = stock.info.get('fiftyTwoWeekHigh', None)
        year_low = stock.info.get('fiftyTwoWeekLow', None)
        beta = stock.info.get('beta', None)
        news = stock.news  # This returns recent news articles related to the stock

        # Prepare the response data
        stock_history_data = {
            "ticker": ticker, 
            "current_price": current_price,
            "open_price": open_price,
            "high_price": high_price,
            "low_price": low_price,
            "previous_close": previous_close,
            "volume": volume,
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "eps": eps,
            "dividend_yield": dividend_yield,
            "year_high": year_high,
            "year_low": year_low,
            "beta": beta,
            #"recommendation_trend": recommendation_trend,
            "news": news,
            "dates": stock_history.index.strftime('%Y-%m-%d').tolist(),  # Format dates
            "prices": stock_history['Close'].tolist(),  # Historical closing prices
            "dates": stock_history.index.strftime('%Y-%m-%d').tolist(),  # Converts the dates to strings
            "prices": stock_history['Close'].tolist(), # Gets the closing prices
            "date_fetched": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Capture the current time
        }

        return stock_history_data

    except Exception as e:
        print(f"Error in analyze_stock: {e}")  # Print the error for debugging
        return jsonify({"error": str(e)}), 500  

# Route for the home page/ ticker data page 
@app.route('/')
def home():
    return render_template('stock_data.html')

# Route to handle stock analysis and fetch data using Yahoo Finance
@app.route('/analyze_stock', methods=['POST'])
def analyze_stock():
    data = request.json
    ticker = data.get("ticker")

    # Fetch stock data (this is just a placeholder for your data fetching logic)
    time_period = '2y'
    time_interval = '1wk'
    stock_history = fetch_stock_data(ticker, time_period, time_interval)  # Your function to fetch data

    # Creates the stock_history response data
    stock_history_data = generate_stock_history_dict(ticker, time_period, time_interval, stock_history)

    # Saving the stock history data to the stock databse
    save_stock_data_to_db(stock_history_data)

    #print("Stock History Data", stock_history_data)
    return jsonify(stock_history_data), 200

# Route for the stock report page
@app.route('/daily_stock_report')
def daily_stock_report():
    return render_template('daily_stock_report.html')

if __name__ == '__main__':
    app.run(debug=True)
