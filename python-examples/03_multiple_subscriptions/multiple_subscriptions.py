#!/usr/bin/env python3
"""
Multiple Subscriptions Example
Subscribe to different data types and coins simultaneously
"""

import asyncio
import json
import os
import websockets
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def handle_trade(data):
    """Handle incoming trade data"""
    # trades data is a list of trade objects with coin and trades
    for trade_data in data["data"]:
        coin = trade_data.get("coin")
        trades_list = trade_data.get("trades", [])

        for trade in trades_list:
            side = trade["side"]
            price = trade["px"]
            size = trade["sz"]
            timestamp = datetime.fromtimestamp(trade["time"] / 1000)

            # Color code buy/sell
            side_icon = "🟢" if side == "B" else "🔴"

            print(f"{side_icon} {coin} Trade: {side} {size} @ ${price} | {timestamp.strftime('%H:%M:%S')}")


def handle_l2_book(data):
    """Handle incoming L2 order book data"""
    coin = data["data"]["coin"]
    levels = data["data"]["levels"]

    # Get best bid and ask
    best_bid = levels[0][0] if levels[0] else None
    best_ask = levels[1][0] if levels[1] else None

    if best_bid and best_ask:
        bid_price = best_bid['px']
        ask_price = best_ask['px']
        spread = float(ask_price) - float(bid_price)

        print(f"📊 {coin} Book: Bid ${bid_price} | Ask ${ask_price} | Spread ${spread:.2f}")


def route_message(data):
    """Route messages to appropriate handlers"""
    channel = data.get("channel")

    if channel == "trades":
        handle_trade(data)
    elif channel == "l2Book":
        handle_l2_book(data)
    elif channel == "subscriptionResponse":
        # Ignore subscription confirmation messages
        pass
    else:
        print(f"Unknown channel: {channel}")


async def main():
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        return

    print(f"Connecting to {ws_url}...")
    websocket = await websockets.connect(ws_url)
    print("Connected!\n")

    # Subscribe to BTC trades
    btc_trades = {
        "method": "subscribe",
        "subscription": {
            "type": "trades",
            "coin": "BTC"
        }
    }
    await websocket.send(json.dumps(btc_trades))
    print("✓ Subscribed to BTC trades")

    # Subscribe to ETH trades
    eth_trades = {
        "method": "subscribe",
        "subscription": {
            "type": "trades",
            "coin": "ETH"
        }
    }
    await websocket.send(json.dumps(eth_trades))
    print("✓ Subscribed to ETH trades")

    # Subscribe to SOL L2 order book
    sol_l2 = {
        "method": "subscribe",
        "subscription": {
            "type": "l2Book",
            "coin": "SOL",
            "nLevels": 5,
            "nSigFigs": 4
        }
    }
    await websocket.send(json.dumps(sol_l2))
    print("✓ Subscribed to SOL L2 book")

    print("\n" + "="*60)
    print("Watching multiple feeds...")
    print("="*60 + "\n")

    try:
        async for message in websocket:
            data = json.loads(message)
            route_message(data)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await websocket.close()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())