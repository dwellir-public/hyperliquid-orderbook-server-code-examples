#!/usr/bin/env python3
"""
L4 Order Book Example - Individual Order Tracking
Shows every individual order in the book with full details
"""

import asyncio
import json
import os
import websockets
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()


class L4OrderBook:
    """Track individual orders in the L4 order book"""

    def __init__(self):
        self.orders = {}  # oid -> order details
        self.price_levels = defaultdict(list)  # price -> list of oids

    def handle_update(self, data):
        """Process L4 book updates"""
        coin = data["data"]["coin"]

        # Process order updates
        for order in data["data"]["orders"]:
            oid = order["oid"]

            if "status" in order:
                # Order removed/filled
                self._remove_order(oid)
            else:
                # New or updated order
                self._add_order(order)

        self.display_summary(coin)

    def _add_order(self, order):
        """Add or update an order"""
        oid = order["oid"]
        price = order["limitPx"]

        # Remove from old price level if exists
        if oid in self.orders:
            old_price = self.orders[oid]["limitPx"]
            if oid in self.price_levels[old_price]:
                self.price_levels[old_price].remove(oid)

        # Add to new price level
        self.orders[oid] = order
        if oid not in self.price_levels[price]:
            self.price_levels[price].append(oid)

    def _remove_order(self, oid):
        """Remove an order"""
        if oid in self.orders:
            price = self.orders[oid]["limitPx"]
            del self.orders[oid]
            if oid in self.price_levels[price]:
                self.price_levels[price].remove(oid)

    def display_summary(self, coin):
        """Display current order book state"""
        # Separate bids and asks
        bids = []
        asks = []

        for oid, order in self.orders.items():
            if order["side"] == "B":
                bids.append(order)
            else:
                asks.append(order)

        # Sort: bids descending, asks ascending
        bids.sort(key=lambda x: float(x["limitPx"]), reverse=True)
        asks.sort(key=lambda x: float(x["limitPx"]))

        print(f"\n{'='*70}")
        print(f"📋 {coin} L4 Order Book - Individual Orders")
        print(f"{'='*70}")
        print(f"Total Orders: {len(self.orders)} (Bids: {len(bids)}, Asks: {len(asks)})")
        print(f"{'='*70}\n")

        # Show top 5 asks
        print("🔴 TOP ASKS (Individual Orders)")
        print(f"{'Price':<15} {'Size':<15} {'User (truncated)':<20}")
        print("-" * 70)
        for ask in asks[:5]:
            user_short = ask["user"][:16] + "..."
            print(f"{ask['limitPx']:<15} {ask['sz']:<15} {user_short:<20}")

        # Show best bid/ask
        if bids and asks:
            spread = float(asks[0]["limitPx"]) - float(bids[0]["limitPx"])
            print(f"\n{'─'*70}")
            print(f"💰 Spread: ${spread:.2f}")
            print(f"{'─'*70}\n")

        # Show top 5 bids
        print("🟢 TOP BIDS (Individual Orders)")
        print(f"{'Price':<15} {'Size':<15} {'User (truncated)':<20}")
        print("-" * 70)
        for bid in bids[:5]:
            user_short = bid["user"][:16] + "..."
            print(f"{bid['limitPx']:<15} {bid['sz']:<15} {user_short:<20}")


async def main():
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        return

    print(f"Connecting to {ws_url}...")
    websocket = await websockets.connect(ws_url)
    print("Connected!\n")

    # Subscribe to ETH L4 order book
    subscribe_message = {
        "method": "subscribe",
        "subscription": {
            "type": "l4Book",
            "coin": "ETH"
        }
    }
    await websocket.send(json.dumps(subscribe_message))
    print("📈 Subscribed to ETH L4 Order Book (Individual Orders)")
    print("⚠️  Note: L4 data is much more detailed and updates frequently")
    print("Watching for updates...\n")

    # Create order book tracker
    orderbook = L4OrderBook()

    try:
        async for message in websocket:
            data = json.loads(message)
            if data.get("channel") == "l4Book":
                orderbook.handle_update(data)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await websocket.close()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())