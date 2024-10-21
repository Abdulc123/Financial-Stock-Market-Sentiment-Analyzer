import json

# Loading the data from the stockDataFile
def load_stock_data_from_file(filename = "stockData.json"):

    try:
        # Loading the JSON Data from the stockData.json file
        with open(filename, "r") as json_file:
            data = json.load(json_file)
        return data
    
    except Exception as e:
        print(f"Error loading stock data from fiel: {e}")

# Create the dictionary from the Stock Json Data
def create_stock_dict(data):
    stock_dict = {}

    # Iterate through the Json and create Dictionary where 
    # Key: Ticker ID
    # Value: Stock Name
    for item in data.values():
        ticker = item["ticker"]
        name = item["title"]
        stock_dict[ticker] = name
    return stock_dict

# Write the dictionary to a file so it can be referenced 
def save_stock_dict(stock_dict, filename = "stock_dict.json"):
    
    with open(filename, "w") as json_file:
        json.dump(stock_dict, json_file, indent = 4)
    
    print(f"Succes: Stock Dictionary saved to {filename}")

def main():
    data = load_stock_data_from_file()
    
    # if data is not empty
    if data:
        stock_dict = create_stock_dict(data)
        save_stock_dict(stock_dict) # Saving it to a file to be referenced later

#if __name__ == "__main__":
    #main()
