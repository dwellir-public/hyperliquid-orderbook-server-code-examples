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
from collections import defaultdict
from datetime import datetime

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


class L4OrderBook:
    """Maintains L4 orderbook state with individual orders"""

    def __init__(self):
        # Store orders by order ID: {oid: {user, limitPx, sz, side}}
        self.orders = {}
        # Store bids and asks separately for quick access: {price: [oid1, oid2, ...]}
        self.bids = defaultdict(list)
        self.asks = defaultdict(list)
        self.coin = None
        self.height = None
        self.last_update = None

    def process_snapshot(self, snapshot):
        """Process a full snapshot"""
        self.coin = snapshot["coin"]
        self.height = snapshot.get("height", "N/A")
        self.last_update = datetime.now()

        # Clear existing state
        self.orders.clear()
        self.bids.clear()
        self.asks.clear()

        # L4 book structure: {"levels": [[bids], [asks]]}
        levels = snapshot.get("levels", [[], []])
        bids_list = levels[0] if len(levels) > 0 else []
        asks_list = levels[1] if len(levels) > 1 else []

        # Add all bid orders
        for bid in bids_list:
            oid = bid.get("oid")
            if oid:
                price = bid.get("limitPx")
                self.orders[oid] = {
                    "user": bid.get("user"),
                    "limitPx": price,
                    "sz": bid.get("sz"),
                    "side": "bid"
                }
                self.bids[price].append(oid)

        # Add all ask orders
        for ask in asks_list:
            oid = ask.get("oid")
            if oid:
                price = ask.get("limitPx")
                self.orders[oid] = {
                    "user": ask.get("user"),
                    "limitPx": price,
                    "sz": ask.get("sz"),
                    "side": "ask"
                }
                self.asks[price].append(oid)

    def process_update(self, update):
        """Process incremental updates"""
        self.height = update.get("height", self.height)
        self.last_update = datetime.now()

        # Updates structure: {"levels": [[bid_updates], [ask_updates]]}
        levels = update.get("levels", [[], []])
        bid_updates = levels[0] if len(levels) > 0 else []
        ask_updates = levels[1] if len(levels) > 1 else []

        # Process bid updates
        for bid in bid_updates:
            oid = bid.get("oid")
            if not oid:
                continue

            # If size is "0" or empty, remove the order
            size = bid.get("sz", "0")
            if size == "0" or size == "":
                self._remove_order(oid)
            else:
                # Check if this is an update to an existing order
                if oid in self.orders:
                    # Remove from old price level
                    old_price = self.orders[oid]["limitPx"]
                    if old_price in self.bids and oid in self.bids[old_price]:
                        self.bids[old_price].remove(oid)
                        if not self.bids[old_price]:
                            del self.bids[old_price]

                # Add or update order
                price = bid.get("limitPx")
                self.orders[oid] = {
                    "user": bid.get("user"),
                    "limitPx": price,
                    "sz": size,
                    "side": "bid"
                }
                if oid not in self.bids[price]:
                    self.bids[price].append(oid)

        # Process ask updates
        for ask in ask_updates:
            oid = ask.get("oid")
            if not oid:
                continue

            # If size is "0" or empty, remove the order
            size = ask.get("sz", "0")
            if size == "0" or size == "":
                self._remove_order(oid)
            else:
                # Check if this is an update to an existing order
                if oid in self.orders:
                    # Remove from old price level
                    old_price = self.orders[oid]["limitPx"]
                    if old_price in self.asks and oid in self.asks[old_price]:
                        self.asks[old_price].remove(oid)
                        if not self.asks[old_price]:
                            del self.asks[old_price]

                # Add or update order
                price = ask.get("limitPx")
                self.orders[oid] = {
                    "user": ask.get("user"),
                    "limitPx": price,
                    "sz": size,
                    "side": "ask"
                }
                if oid not in self.asks[price]:
                    self.asks[price].append(oid)

    def _remove_order(self, oid):
        """Remove an order from the book"""
        if oid not in self.orders:
            return

        order = self.orders[oid]
        price = order["limitPx"]
        side = order["side"]

        # Remove from price level
        if side == "bid" and price in self.bids:
            if oid in self.bids[price]:
                self.bids[price].remove(oid)
            if not self.bids[price]:
                del self.bids[price]
        elif side == "ask" and price in self.asks:
            if oid in self.asks[price]:
                self.asks[price].remove(oid)
            if not self.asks[price]:
                del self.asks[price]

        # Remove from orders
        del self.orders[oid]

    def get_sorted_levels(self, max_levels=100):
        """Get sorted bid/ask levels for display"""
        # Sort bids descending (highest first)
        sorted_bid_prices = sorted(self.bids.keys(), key=float, reverse=True)[:max_levels]
        bid_levels = []
        for price in sorted_bid_prices:
            for oid in self.bids[price]:
                if oid in self.orders:
                    order = self.orders[oid]
                    bid_levels.append({
                        "oid": oid,
                        "limitPx": price,
                        "sz": order["sz"],
                        "user": order["user"]
                    })

        # Sort asks ascending (lowest first)
        sorted_ask_prices = sorted(self.asks.keys(), key=float)[:max_levels]
        ask_levels = []
        for price in sorted_ask_prices:
            for oid in self.asks[price]:
                if oid in self.orders:
                    order = self.orders[oid]
                    ask_levels.append({
                        "oid": oid,
                        "limitPx": price,
                        "sz": order["sz"],
                        "user": order["user"]
                    })

        return bid_levels, ask_levels


def display_orderbook(orderbook, max_display=100):
    """Display the current orderbook state"""
    bids, asks = orderbook.get_sorted_levels(max_levels=max_display)

    # Clear screen for cleaner updates
    print("\033[2J\033[H")  # ANSI escape codes to clear screen

    print(f"{'='*90}")
    print(f"📋 {orderbook.coin} L4 Order Book (Height: {orderbook.height}) - Updated: {orderbook.last_update.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"📊 Total Orders: {len(orderbook.orders)} | Bid Levels: {len(orderbook.bids)} | Ask Levels: {len(orderbook.asks)}")
    print(f"{'='*90}")

    # Display asks (sellers) - reverse order so highest price is on top
    print(f"\n🔴 ASKS (Individual Sell Orders) - Showing top {min(len(asks), max_display)}")
    print(f"{'Price':<12} {'Size':<12} {'Order ID':<20} {'User':<20}")
    print("-" * 90)

    # Show asks reversed (highest to lowest)
    for ask in reversed(asks[:max_display]):
        user_addr = ask.get("user", "unknown")[:12] + "..."
        order_id = str(ask.get("oid", ""))[:18]
        price = ask.get("limitPx", "0")
        size = ask.get("sz", "0")
        print(f"{price:<12} {size:<12} {order_id:<20} {user_addr:<20}")

    # Calculate spread
    if bids and asks:
        best_bid = float(bids[0].get('limitPx', 0))
        best_ask = float(asks[0].get('limitPx', 0))
        spread = best_ask - best_bid
        spread_pct = (spread / best_bid * 100) if best_bid > 0 else 0

        print(f"\n{'─'*90}")
        print(f"💰 Spread: ${spread:.4f} ({spread_pct:.4f}%) | Best Bid: ${best_bid} | Best Ask: ${best_ask}")
        print(f"{'─'*90}\n")

    # Display bids (buyers)
    print(f"🟢 BIDS (Individual Buy Orders) - Showing top {min(len(bids), max_display)}")
    print(f"{'Price':<12} {'Size':<12} {'Order ID':<20} {'User':<20}")
    print("-" * 90)

    # Show bids (highest to lowest)
    for bid in bids[:max_display]:
        user_addr = bid.get("user", "unknown")[:12] + "..."
        order_id = str(bid.get("oid", ""))[:18]
        price = bid.get("limitPx", "0")
        size = bid.get("sz", "0")
        print(f"{price:<12} {size:<12} {order_id:<20} {user_addr:<20}")

    print(f"\n{'='*90}\n")


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

    # Create orderbook instance
    orderbook = L4OrderBook()
    update_count = 0

    try:
        async for message in websocket:
            data = json.loads(message)

            # Only process l4Book channel messages
            if data.get("channel") != "l4Book":
                continue

            # Process snapshots
            snapshot = data["data"].get("Snapshot")
            if snapshot:
                orderbook.process_snapshot(snapshot)
                display_orderbook(orderbook, max_display=100)
                continue

            # Process updates
            updates = data["data"].get("Updates")
            if updates:
                orderbook.process_update(updates)
                update_count += 1

                # Display every update (change to % 10 or % 5 if too frequent)
                display_orderbook(orderbook, max_display=100)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await websocket.close()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())
