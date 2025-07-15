from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

FMP_API_KEY = os.getenv("T0b52Lczz6Tif0xQbMMSYKOKty9HhmTe")
FMP_BASE = "https://financialmodelingprep.com/api/v3"

def get_ps_ratio(ticker):
    url = f"{FMP_BASE}/ratios/{ticker}?apikey={FMP_API_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        app.logger.error(f"Failed to fetch PS ratio: {res.status_code} {res.text}")
        return None
    data = res.json()
    app.logger.info(f"PS Ratio API response for {ticker}: {data}")
    if isinstance(data, list) and len(data) > 0:
        ps_ratio = data[0].get("priceToSalesRatioTTM")
        if ps_ratio is not None:
            return ps_ratio
    return None

def get_sales_growth(ticker):
    url = f"{FMP_BASE}/financial-growth/{ticker}?apikey={FMP_API_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        app.logger.error(f"Failed to fetch sales growth: {res.status_code} {res.text}")
        return None
    data = res.json()
    app.logger.info(f"Sales Growth API response for {ticker}: {data}")
    if isinstance(data, list) and len(data) > 0:
        revenue_growth = data[0].get("revenueGrowth")
        if revenue_growth is not None:
            return revenue_growth
    return None

@app.route("/psg/<ticker>")
def psg(ticker):
    try:
        ps = get_ps_ratio(ticker.upper())
        growth = get_sales_growth(ticker.upper())
        if ps is None:
            return jsonify({"error": "Price-to-Sales ratio data missing or invalid"}), 400
        if growth is None or growth == 0:
            return jsonify({"error": "Sales growth data missing, invalid, or zero"}), 400

        psg_value = ps / (growth * 100)

        return jsonify({
            "ticker": ticker.upper(),
            "p/s": ps,
            "sales_growth_pct": growth * 100,
            "psg": psg_value
        })
    except Exception as e:
        app.logger.error(f"Exception in /psg/{ticker}: {str(e)}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route("/")
def home():
    return "PSG Ratio API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
