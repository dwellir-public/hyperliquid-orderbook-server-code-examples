#!/usr/bin/env python3
"""
L4 Order Book Example - Individual Order Visibility
Shows the most detailed market microstructure data with individual orders
"""

import asyncio
import json
import os
import websockets
from dotenv import load_dotenv
from pathlib import Path

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


def display_l4_orderbook(data):
    """Display the L4 order book with individual orders"""
    if data.get("channel") != "l4Book":
        return

    # L4 book has Snapshot wrapper (initial) or Updates (incremental)
    # For this simple example, we only display Snapshots
    snapshot = data["data"].get("Snapshot")
    if not snapshot:
        # Skip Updates for this basic example
        return

    coin = snapshot["coin"]
    height = snapshot.get("height", "N/A")

    # L4 book structure: {"levels": [[bids], [asks]]}
    levels = snapshot.get("levels", [[], []])
    bids = levels[0] if len(levels) > 0 else []
    asks = levels[1] if len(levels) > 1 else []

    print(f"\n{'='*70}")
    print(f"📋 {coin} L4 Order Book (Block Height: {height})")
    print(f"{'='*70}")

    # Display asks (sellers) - reverse order so highest price is on top
    print("\n🔴 ASKS (Individual Sell Orders)")
    print(f"{'Price':<12} {'Size':<12} {'Order ID':<20} {'User':<20}")
    print("-" * 70)

    # Show top 5 asks (reversed for display)
    for ask in reversed(asks[:5]):
        user_addr = ask.get("user", "unknown")[:10] + "..."
        order_id = str(ask.get("oid", ""))[:16]
        price = ask.get("limitPx", "0")
        size = ask.get("sz", "0")

        print(f"{price:<12} {size:<12} {order_id:<20} {user_addr:<20}")

    # Calculate spread
    if bids and asks:
        best_bid = float(bids[0].get('limitPx', 0))
        best_ask = float(asks[0].get('limitPx', 0))
        spread = best_ask - best_bid
        spread_pct = (spread / best_bid * 100) if best_bid > 0 else 0

        print(f"\n{'─'*70}")
        print(f"💰 Spread: ${spread:.4f} ({spread_pct:.4f}%)")
        print(f"{'─'*70}\n")

    # Display bids (buyers)
    print("🟢 BIDS (Individual Buy Orders)")
    print(f"{'Price':<12} {'Size':<12} {'Order ID':<20} {'User':<20}")
    print("-" * 70)

    # Show top 5 bids
    for bid in bids[:5]:
        user_addr = bid.get("user", "unknown")[:10] + "..."
        order_id = str(bid.get("oid", ""))[:16]
        price = bid.get("limitPx", "0")
        size = bid.get("sz", "0")

        print(f"{price:<12} {size:<12} {order_id:<20} {user_addr:<20}")

    print(f"\n{'='*70}\n")


async def main():
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        return

    print(f"Connecting to {ws_url}...")
    # Increase max_size to handle large L4 orderbook messages (default is 1MB)
    websocket = await websockets.connect(ws_url, max_size=10 * 1024 * 1024)  # 10MB
    print("Connected!\n")

    # Subscribe to BTC L4 order book
    # L4 shows individual orders with full details
    subscribe_message = {
        "method": "subscribe",
        "subscription": {
            "type": "l4Book",
            "coin": "BTC"
        }
    }
    await websocket.send(json.dumps(subscribe_message))
    print("📋 Subscribed to BTC L4 Order Book")
    print("This shows individual orders with user addresses and order IDs")
    print("Watching for updates...\n")

    try:
        async for message in websocket:
            data = json.loads(message)
            display_l4_orderbook(data)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await websocket.close()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())
