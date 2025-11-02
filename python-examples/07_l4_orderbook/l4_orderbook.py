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
        # Track changes for display
        self.last_changes = {"added": [], "removed": [], "modified": []}

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
        """Process incremental updates from book_diffs"""
        self.height = update.get("height", self.height)
        self.last_update = datetime.now()

        # Clear previous changes
        self.last_changes = {"added": [], "removed": [], "modified": []}

        # Build a map of oid -> order info from order_statuses to get the side
        order_info_map = {}
        for order_status in update.get("order_statuses", []):
            order = order_status.get("order", {})
            oid = order.get("oid")
            if oid:
                order_info_map[oid] = order

        # Process book_diffs - this is where the actual orderbook changes are
        for diff in update.get("book_diffs", []):
            oid = diff.get("oid")
            px = diff.get("px")
            user = diff.get("user")
            raw_diff = diff.get("raw_book_diff")

            if not oid:
                continue

            # Handle removal
            if raw_diff == "remove":
                if oid in self.orders:
                    order_info = self.orders[oid].copy()
                    order_info["oid"] = oid
                    self.last_changes["removed"].append(order_info)
                    self._remove_order(oid)

            # Handle new order
            elif isinstance(raw_diff, dict) and "new" in raw_diff:
                sz = raw_diff["new"]["sz"]

                # Get side from order_statuses
                side = None
                if oid in order_info_map:
                    side_code = order_info_map[oid].get("side")
                    side = "bid" if side_code == "B" else "ask" if side_code == "A" else None

                if not side:
                    # Fallback: Can't determine side, skip this update
                    continue

                # Add order to orderbook
                self.orders[oid] = {
                    "user": user,
                    "limitPx": px,
                    "sz": sz,
                    "side": side
                }

                # Add to appropriate price level
                if side == "bid":
                    if oid not in self.bids[px]:
                        self.bids[px].append(oid)
                else:  # ask
                    if oid not in self.asks[px]:
                        self.asks[px].append(oid)

                # Track change for display
                self.last_changes["added"].append({
                    "oid": oid,
                    "user": user,
                    "limitPx": px,
                    "sz": sz,
                    "side": side
                })

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

    def get_sorted_levels(self, max_orders=100):
        """Get sorted bid/ask levels for display - returns up to max_orders on each side"""
        # Sort bids descending (highest first)
        sorted_bid_prices = sorted(self.bids.keys(), key=float, reverse=True)
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
                    if len(bid_levels) >= max_orders:
                        break
            if len(bid_levels) >= max_orders:
                break

        # Sort asks ascending (lowest first)
        sorted_ask_prices = sorted(self.asks.keys(), key=float)
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
                    if len(ask_levels) >= max_orders:
                        break
            if len(ask_levels) >= max_orders:
                break

        return bid_levels, ask_levels


def display_changes(orderbook):
    """Display only the changes that occurred in the last update"""
    changes = orderbook.last_changes

    total_changes = len(changes["added"]) + len(changes["modified"]) + len(changes["removed"])

    if total_changes == 0:
        return  # Don't print anything if no changes

    print(f"\n{'='*100}")
    print(f"📋 {orderbook.coin} L4 Updates (Height: {orderbook.height}) - {orderbook.last_update.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"📊 Total Orders: {len(orderbook.orders)} | Changes: ➕{len(changes['added'])} ✏️{len(changes['modified'])} ❌{len(changes['removed'])}")
    print(f"{'='*100}")

    # Display added orders
    if changes["added"]:
        print(f"\n➕ NEW ORDERS ({len(changes['added'])})")
        print(f"{'Side':<6} {'Price':<12} {'Size':<12} {'Order ID':<20} {'User':<20}")
        print("-" * 100)
        for order in changes["added"][:20]:  # Show up to 20
            side_emoji = "🔴" if order["side"] == "ask" else "🟢"
            side_text = "ASK" if order["side"] == "ask" else "BID"
            user_addr = order.get("user", "unknown")[:12] + "..."
            order_id = str(order.get("oid", ""))[:18]
            print(f"{side_emoji} {side_text:<4} {order['limitPx']:<12} {order['sz']:<12} {order_id:<20} {user_addr:<20}")

    # Display modified orders
    if changes["modified"]:
        print(f"\n✏️  MODIFIED ORDERS ({len(changes['modified'])})")
        print(f"{'Side':<6} {'Price':<12} {'Size':<12} {'Order ID':<20} {'User':<20}")
        print("-" * 100)
        for order in changes["modified"][:20]:  # Show up to 20
            side_emoji = "🔴" if order["side"] == "ask" else "🟢"
            side_text = "ASK" if order["side"] == "ask" else "BID"
            user_addr = order.get("user", "unknown")[:12] + "..."
            order_id = str(order.get("oid", ""))[:18]
            print(f"{side_emoji} {side_text:<4} {order['limitPx']:<12} {order['sz']:<12} {order_id:<20} {user_addr:<20}")

    # Display removed orders
    if changes["removed"]:
        print(f"\n❌ REMOVED ORDERS ({len(changes['removed'])})")
        print(f"{'Side':<6} {'Price':<12} {'Size':<12} {'Order ID':<20} {'User':<20}")
        print("-" * 100)
        for order in changes["removed"][:20]:  # Show up to 20
            side_emoji = "🔴" if order["side"] == "ask" else "🟢"
            side_text = "ASK" if order["side"] == "ask" else "BID"
            user_addr = order.get("user", "unknown")[:12] + "..."
            order_id = str(order.get("oid", ""))[:18]
            print(f"{side_emoji} {side_text:<4} {order['limitPx']:<12} {order['sz']:<12} {order_id:<20} {user_addr:<20}")

    print(f"\n{'='*100}\n")


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
                print(f"✅ Snapshot loaded: {len(orderbook.orders)} orders")
                continue

            # Process updates - Updates is a single dict with book_diffs
            updates = data["data"].get("Updates")
            if updates:
                orderbook.process_update(updates)
                update_count += 1
                # Display changes
                display_changes(orderbook)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await websocket.close()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())
