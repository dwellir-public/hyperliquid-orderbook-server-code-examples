#!/usr/bin/env python3
"""
L2 Order Book Example - Aggregated Price Levels
Shows bid/ask spreads with price aggregation
"""

import asyncio
import json
import os
import websockets
from dotenv import load_dotenv

load_dotenv()


def display_orderbook(data):
    """Display the order book in a simple format"""
    if data.get("channel") != "l2Book":
        return

    coin = data["data"]["coin"]
    levels = data["data"]["levels"]

    print(f"\n{'='*50}")
    print(f"📊 {coin} Order Book")
    print(f"{'='*50}")

    # Display asks (sellers) - reverse order so highest price is on top
    print("\n🔴 ASKS (Sellers)")
    print(f"{'Price':<15} {'Size':<15} {'Orders':<10}")
    print("-" * 50)
    for ask in reversed(levels[1][:5]):  # Show top 5 asks
        print(f"{ask['px']:<15} {ask['sz']:<15} {ask['n']:<10}")

    # Calculate spread
    best_bid = float(levels[0][0]['px']) if levels[0] else 0
    best_ask = float(levels[1][0]['px']) if levels[1] else 0
    spread = best_ask - best_bid
    spread_pct = (spread / best_bid * 100) if best_bid > 0 else 0

    print(f"\n{'─'*50}")
    print(f"💰 Spread: ${spread:.2f} ({spread_pct:.3f}%)")
    print(f"{'─'*50}\n")

    # Display bids (buyers)
    print("🟢 BIDS (Buyers)")
    print(f"{'Price':<15} {'Size':<15} {'Orders':<10}")
    print("-" * 50)
    for bid in levels[0][:5]:  # Show top 5 bids
        print(f"{bid['px']:<15} {bid['sz']:<15} {bid['n']:<10}")


async def main():
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        return

    print(f"Connecting to {ws_url}...")
    websocket = await websockets.connect(ws_url)
    print("Connected!\n")

    # Subscribe to ETH L2 order book
    # nLevels: how many price levels (default 20, max 100)
    # nSigFigs: price aggregation (2-5, more = more precise)
    subscribe_message = {
        "method": "subscribe",
        "subscription": {
            "type": "l2Book",
            "coin": "ETH",
            "nLevels": 10,
            "nSigFigs": 5
        }
    }
    await websocket.send(json.dumps(subscribe_message))
    print("📈 Subscribed to ETH L2 Order Book")
    print("Watching for updates...\n")

    try:
        async for message in websocket:
            data = json.loads(message)
            display_orderbook(data)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await websocket.close()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())