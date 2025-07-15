from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

FMP_API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE = "https://financialmodelingprep.com/api/v3"

def get_ps_ratio(ticker):
    url = f"{FMP_BASE}/ratios/{ticker}?apikey={FMP_API_KEY}"
    res = requests.get(url).json()
    return res[0]["priceToSalesRatioTTM"] if res else None

def get_sales_growth(ticker):
    url = f"{FMP_BASE}/financial-growth/{ticker}?apikey={FMP_API_KEY}"
    res = requests.get(url).json()
    return res[0]["revenueGrowth"] if res else None

@app.route("/psg/<ticker>")
def psg(ticker):
    ps = get_ps_ratio(ticker)
    growth = get_sales_growth(ticker)
    if ps is None or growth is None or growth == 0:
        return jsonify({"error": "Data missing"}), 400
    psg_value = ps / (growth * 100)
    return jsonify({
        "ticker": ticker.upper(),
        "p/s": ps,
        "sales_growth_pct": growth * 100,
        "psg": psg_value
    })

@app.route("/")
def home():
    return "PSG Ratio API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
