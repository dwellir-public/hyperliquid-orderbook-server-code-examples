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

# Global configuration
COIN = "ETH"          # Which coin to track
N_LEVELS = 100         # Number of price levels to display (1-100)
N_SIG_FIGS = 5        # Price precision/aggregation (2-5)


def display_orderbook(data):
    """Display the order book in a trading terminal style"""
    if data.get("channel") != "l2Book":
        return

    coin = data["data"]["coin"]
    levels = data["data"]["levels"]

    # Clear screen for smooth updates (optional - comment out if you want history)
    print("\033[2J\033[H", end="")

    # Calculate spread
    best_bid = float(levels[0][0]['px']) if levels[0] else 0
    best_ask = float(levels[1][0]['px']) if levels[1] else 0
    spread = best_ask - best_bid
    spread_pct = (spread / best_bid * 100) if best_bid > 0 else 0

    print(f"\n{'='*100}")
    print(f"📊 {coin} Order Book - Live Market Depth".center(100))
    print(f"{'='*100}\n")

    # Header for side-by-side display
    print(f"{'BIDS (Buyers)':^40} │ {'ASKS (Sellers)':^40}")
    print(f"{'Price':<14} {'Size':<14} {'Orders':<8} │ {'Price':<14} {'Size':<14} {'Orders':<8}")
    print(f"{'─'*40}─┼─{'─'*40}")

    # Get N_LEVELS for each side
    bids = levels[0][:N_LEVELS] if levels[0] else []
    asks = levels[1][:N_LEVELS] if levels[1] else []

    # Display rows side by side (asks reversed so best prices are in the middle)
    max_rows = max(len(bids), len(asks))

    for i in range(max_rows):
        # Bid side (left)
        if i < len(bids):
            bid = bids[i]
            bid_line = f"🟢 {bid['px']:<12} {bid['sz']:<14} {bid['n']:<8}"
        else:
            bid_line = " " * 40

        # Ask side (right) - reverse order so best ask is at top
        ask_idx = len(asks) - 1 - i
        if ask_idx >= 0:
            ask = asks[ask_idx]
            ask_line = f"🔴 {ask['px']:<12} {ask['sz']:<14} {ask['n']:<8}"
        else:
            ask_line = " " * 40

        print(f"{bid_line} │ {ask_line}")

    # Spread display
    print(f"\n{'─'*100}")
    print(f"💰 Best Bid: ${best_bid:,.2f}  |  Best Ask: ${best_ask:,.2f}  |  Spread: ${spread:.4f} ({spread_pct:.4f}%)".center(100))
    print(f"{'─'*100}\n")


async def main():
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        return

    print(f"Connecting to {ws_url}...")
    websocket = await websockets.connect(ws_url)
    print("Connected!\n")

    # Subscribe to L2 order book using global configuration
    subscribe_message = {
        "method": "subscribe",
        "subscription": {
            "type": "l2Book",
            "coin": COIN,
            "nLevels": N_LEVELS,
            "nSigFigs": N_SIG_FIGS
        }
    }
    await websocket.send(json.dumps(subscribe_message))
    print(f"📈 Subscribed to {COIN} L2 Order Book ({N_LEVELS} levels, {N_SIG_FIGS} sig figs)")
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