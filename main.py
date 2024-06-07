import webview
import xapi_func
import asyncio
import json
import pandas as pd
from datetime import datetime as dt

class Api:    
    def getPortfolio(self):
        json_data = json.loads(asyncio.run(xapi_func.getPortfolio()))
        df = pd.DataFrame(json_data)
        df = df[['symbol', 'nominalValue', 'profit', 'volume']]
        df = df.groupby(by="symbol").agg({
            'nominalValue': 'sum',
            'profit': 'sum',
            'volume': 'sum'
        }).reset_index()
        df["currentValue"] = df["nominalValue"] + df["profit"]
        df["profitPercent"] = df["profit"] / df["nominalValue"]
        df["percentOfPortfolio"] = df["currentValue"] / df["currentValue"].sum()
        df = df.rename(columns={
            "symbol": "Symbol",
            "profit": "Profit",
            "volume" : "Volume",
            "currentValue": "Value",
            "profitPercent": "Profit (%)",
            "percentOfPortfolio": "% of portfolio"
        })
        df = df[['Symbol', 'Profit', 'Volume', 'Value', 'Profit (%)', "% of portfolio"]]
        df["% of portfolio"] = df["% of portfolio"] * 100
        df["% of portfolio"] = df["% of portfolio"].round(2)
        df["Profit (%)"] = df["Profit (%)"] * 100
        df["Profit (%)"] = df["Profit (%)"].round(2)
        df["Profit"] = df["Profit"].round(2)
        df["Volume"] = df["Volume"].round(2)
        df["Value"] = df["Value"].round(2)
        json_data = df.to_json(orient='records')
        return json_data

if __name__ == '__main__':
    api = Api()
    window = webview.create_window('XTB Portfolio Analyzer', 'index.html', js_api=api)
    webview.start(window, debug=True)