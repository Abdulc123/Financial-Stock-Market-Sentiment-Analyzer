from config import AWSHost, AWSPassword
import sqlite3
import mysql.connector
import json


def get_my_sql_connection():
    # conn = connection
    conn = mysql.connector.connect(
        host= AWSHost,
        user='admin',
        password= AWSPassword,
        database='stock4sight_data'
    )
    return conn

# Creates the stock database using SQLite3
def create_stock_db(): 
    # Connect to the SQLite database. If 'stock.db' does not exist in the 'data' directory, it will be created.
    # 'conn' is the connection object used to interact with the database.
    conn = get_my_sql_connection()
    # Create a cursor object, which allows us to execute SQL queries on the connected database.
    cursor = conn.cursor()

    # Drop the existing stock_data table if it exists (use this to reset)
    #cursor.execute('DROP TABLE IF EXISTS stock_data')

    # Create table for historical stock data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ticker VARCHAR(10) NOT NULL,
            current_price DECIMAL(10, 2),
            open_price DECIMAL(10, 2),
            high_price DECIMAL(10, 2),
            low_price DECIMAL(10, 2),
            previous_close DECIMAL(10, 2),
            volume BIGINT,
            market_cap BIGINT,
            pe_ratio DECIMAL(10, 2),
            eps DECIMAL(10, 2),
            dividend_yield DECIMAL(5, 2),
            year_high DECIMAL(10, 2),
            year_low DECIMAL(10, 2),
            beta DECIMAL(5, 2),
            news TEXT,  -- Store news articles as text
            dates TEXT, -- Store dates as JSON string
            prices TEXT, -- Store historical prices as JSON string
            date_fetched DATETIME NOT NULL -- Timestamp for when the data was fetched
        )
    ''')
    # Commit the changes to the database. This ensures that the table creation is saved in 'stock.db'.
    conn.commit()
    # Close the connection to the database to free up resources
    cursor.close()
    conn.close()

# Takes a stock response data parameter and saves the information to the MySQL database stock4sight_data in the in a table called stock_data
def save_stock_data_to_db(stock_data):
    # Connect to the MySQL database
    conn = get_my_sql_connection()
    cursor = conn.cursor()

    # Inserting the stock data into the MySQL database
    cursor.execute('''
        INSERT INTO stock_data (
            ticker, current_price, open_price, high_price, low_price, previous_close,
            volume, market_cap, pe_ratio, eps, dividend_yield, year_high, year_low, 
            beta, news, dates, prices, date_fetched
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        stock_data["ticker"],
        stock_data["current_price"],
        stock_data["open_price"],
        stock_data["high_price"],
        stock_data["low_price"],
        stock_data["previous_close"],
        stock_data["volume"],
        stock_data["market_cap"],
        stock_data["pe_ratio"],
        stock_data["eps"],
        stock_data["dividend_yield"],
        stock_data["year_high"],
        stock_data["year_low"],
        stock_data["beta"],
        json.dumps(stock_data["news"]),  # Convert list to JSON string
        json.dumps(stock_data["dates"]),  # Convert list to JSON string
        json.dumps(stock_data["prices"]),  # Convert list to JSON string
        stock_data["date_fetched"]
    ))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

def check_table_schema():
    conn = sqlite3.connect('data/stocks.db')
    cursor = conn.cursor()

    # Query to check the schema of stock_data table
    cursor.execute("PRAGMA table_info(stock_data);")
    columns = cursor.fetchall()
    
    for column in columns:
        print(column)

    conn.close()



if __name__ == "__main__":
    create_stock_db()
    check_table_schema()

