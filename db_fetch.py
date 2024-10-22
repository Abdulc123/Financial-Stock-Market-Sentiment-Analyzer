import mysql.connector
from config import AWSHost, AWSPassword  # Import your host and password from config

def grab_stock_data_from_db():
    try:
        # Establish connection to the AWS MySQL database
        conn = mysql.connector.connect(
            host=AWSHost,        # AWS RDS endpoint
            user='admin',        # Username you use for AWS RDS
            password=AWSPassword, # Your AWS RDS password
            database='stock4sight_data' # The name of your database
        )

        # Create a cursor object using the connection
        cursor = conn.cursor()

        # Write your query to fetch data from the stock_data table
        query = "SELECT * FROM stock_data"

        # Execute the query
        cursor.execute(query)

        # Fetch all the rows returned by the query
        rows = cursor.fetchall()

        # Print out each row
        for row in rows:
            print(row)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    grab_stock_data_from_db()
