#!/usr/bin/env python3
"""
Multi-Coin Trade Tracker - Advanced Pattern
Track trades from multiple coins simultaneously and compare metrics
"""

import asyncio
import json
import os
import websockets
from collections import deque
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class CoinTracker:
    """Track trading metrics for a specific coin"""

    def __init__(self, coin):
        self.coin = coin
        self.trades = deque(maxlen=50)  # Last 50 trades
        self.total_volume = 0
        self.buy_volume = 0
        self.sell_volume = 0

    def add_trade(self, trade):
        """Add a trade and update metrics"""
        price = float(trade["px"])
        size = float(trade["sz"])
        side = trade["side"]

        self.trades.append({
            "price": price,
            "size": size,
            "side": side,
            "timestamp": datetime.now()
        })

        self.total_volume += size
        if side == "B":
            self.buy_volume += size
        else:
            self.sell_volume += size

    def get_vwap(self):
        """Calculate Volume-Weighted Average Price"""
        if not self.trades:
            return 0
        total_value = sum(t["price"] * t["size"] for t in self.trades)
        total_volume = sum(t["size"] for t in self.trades)
        return total_value / total_volume if total_volume > 0 else 0

    def get_buy_sell_ratio(self):
        """Calculate buy/sell volume ratio"""
        if self.sell_volume == 0:
            return float('inf') if self.buy_volume > 0 else 0
        return self.buy_volume / self.sell_volume

    def get_latest_price(self):
        """Get most recent trade price"""
        return self.trades[-1]["price"] if self.trades else 0


class MultiCoinTracker:
    """Track multiple coins simultaneously"""

    def __init__(self):
        self.trackers = {}  # coin -> CoinTracker
        self.total_trades = 0

    def handle_trade(self, data):
        """Process incoming trade data"""
        for trade in data["data"]:
            coin = trade.get("coin")
            if not coin:
                continue

            # Initialize tracker if new coin
            if coin not in self.trackers:
                self.trackers[coin] = CoinTracker(coin)

            self.trackers[coin].add_trade(trade)
            self.total_trades += 1

            # Display summary every 10 trades
            if self.total_trades % 10 == 0:
                self.display_summary()

    def display_summary(self):
        """Display trading metrics for all coins"""
        if not self.trackers:
            return

        print(f"\n{'='*80}")
        print(f"📊 Multi-Coin Trading Dashboard - Total Trades: {self.total_trades}")
        print(f"{'='*80}")
        print(f"{'Coin':<8} {'Latest $':<12} {'VWAP $':<12} {'Volume':<10} {'B/S Ratio':<10} {'Trades':<8}")
        print(f"{'-'*80}")

        # Sort by total volume
        sorted_coins = sorted(
            self.trackers.items(),
            key=lambda x: x[1].total_volume,
            reverse=True
        )

        for coin, tracker in sorted_coins[:10]:  # Show top 10
            vwap = tracker.get_vwap()
            latest = tracker.get_latest_price()
            ratio = tracker.get_buy_sell_ratio()
            ratio_str = f"{ratio:.2f}" if ratio != float('inf') else "∞"

            print(
                f"{coin:<8} "
                f"${latest:<11,.2f} "
                f"${vwap:<11,.2f} "
                f"{tracker.total_volume:<10.2f} "
                f"{ratio_str:<10} "
                f"{len(tracker.trades):<8}"
            )

        if len(self.trackers) > 10:
            print(f"\n... and {len(self.trackers) - 10} more coins")

        print(f"{'='*80}\n")


async def main():
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        return

    print(f"Connecting to {ws_url}...")
    websocket = await websockets.connect(ws_url)
    print("Connected!\n")

    # Subscribe to trades for multiple major coins
    coins = ["BTC", "ETH", "SOL"]

    for coin in coins:
        subscribe_message = {
            "method": "subscribe",
            "subscription": {
                "type": "trades",
                "coin": coin
            }
        }
        await websocket.send(json.dumps(subscribe_message))
        print(f"✓ Subscribed to {coin} trades")

    print(f"\n{'='*80}")
    print("📈 Tracking trades across multiple coins...")
    print("💡 Displaying dashboard every 10 trades")
    print(f"{'='*80}\n")

    # Create tracker
    tracker = MultiCoinTracker()

    try:
        async for message in websocket:
            data = json.loads(message)
            if data.get("channel") == "trades":
                tracker.handle_trade(data)

    except KeyboardInterrupt:
        print("\nStopping...")
        tracker.display_summary()  # Final summary
    finally:
        await websocket.close()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())