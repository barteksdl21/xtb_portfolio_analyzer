import xapi
import logging
import asyncio
from datetime import datetime as dt
import json

with open("credentials.json", "r") as f:
    CREDENTIALS = json.load(f)


START = round(dt.today().replace(month=1, day=1).timestamp() * 1000)

async def getPortfolio():
    try:
        async with await xapi.connect(**CREDENTIALS) as x:
            response = await x.socket.getTrades(True)
            if response['status'] == True:
                with open('portfolio.json', 'w') as f:
                    json.dump(response['returnData'], f)
                    return json.dumps(response['returnData'])
            else:
                print("Failed to get trades history", response)
                return json.dumps({"message": "Failed to get trades history", "error": True})

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")
        return json.dumps({"message": "Log in failed", "error": True})

    except xapi.ConnectionClosed as e:
        print(f"Connection closed: {e}")
        return json.dumps({"message": "Connection closed", "error": True})
