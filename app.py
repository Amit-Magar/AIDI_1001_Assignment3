from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# My Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "2ICKDAYTDCXCZ7GW"

# Route 1: Root route to return student number
@app.route("/", methods=["GET"])
def home():
    return jsonify({"student_number": "200567979"})

# Route 2: Webhook route for Dialogflow integration
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    query_result = req.get('queryResult', {})
    
    # Extract stock ticker from the request
    parameters = query_result.get('parameters', {})
    stock_ticker = parameters.get('stock_ticker', "").upper()
    
    if not stock_ticker:
        return jsonify({"fulfillmentText": "Please provide a stock ticker to get the price."})

    # Call the Alpha Vantage API
    stock_price = get_stock_price(stock_ticker)
    if stock_price is not None:
        response_text = f"The current price of {stock_ticker} is ${stock_price:.2f}."
    else:
        response_text = f"Sorry, I could not fetch the stock price for {stock_ticker}."
    
    return jsonify({"fulfillmentText": response_text})

def get_stock_price(ticker):
    try:
        url = f"https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        # Extract the stock price from the API response
        price = float(data["Global Quote"]["05. price"])
        return price
    except Exception as e:
        print(f"Error fetching stock price: {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
