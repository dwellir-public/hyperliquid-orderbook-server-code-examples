#!/usr/bin/env python3
"""
Market Metrics and Data Analysis
Calculate real-time market statistics from order book data
"""

import asyncio
import json
import os
import websockets
from collections import deque
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class MarketAnalyzer:
    """Analyze market data and calculate metrics"""

    def __init__(self, history_size=100):
        self.trades = deque(maxlen=history_size)
        self.spreads = deque(maxlen=history_size)
        self.prices = deque(maxlen=history_size)
        self.volumes = deque(maxlen=history_size)

    def add_trade(self, price, size, side):
        """Add a trade and calculate metrics"""
        self.trades.append({
            'price': float(price),
            'size': float(size),
            'side': side,
            'timestamp': datetime.now()
        })
        self.prices.append(float(price))
        self.volumes.append(float(size))

    def add_spread(self, spread):
        """Track spread over time"""
        self.spreads.append(float(spread))

    def get_vwap(self):
        """Calculate Volume-Weighted Average Price"""
        if not self.trades:
            return 0

        total_value = sum(t['price'] * t['size'] for t in self.trades)
        total_volume = sum(t['size'] for t in self.trades)

        return total_value / total_volume if total_volume > 0 else 0

    def get_avg_spread(self):
        """Calculate average spread"""
        if not self.spreads:
            return 0
        return sum(self.spreads) / len(self.spreads)

    def get_total_volume(self):
        """Get total volume"""
        return sum(self.volumes)

    def get_buy_sell_ratio(self):
        """Calculate buy/sell volume ratio"""
        buy_volume = sum(t['size'] for t in self.trades if t['side'] == 'B')
        sell_volume = sum(t['size'] for t in self.trades if t['side'] == 'A')

        if sell_volume == 0:
            return float('inf')
        return buy_volume / sell_volume

    def get_price_change(self):
        """Calculate price change from first to last trade"""
        if len(self.prices) < 2:
            return 0

        first_price = self.prices[0]
        last_price = self.prices[-1]
        change = last_price - first_price
        change_pct = (change / first_price * 100) if first_price > 0 else 0

        return change, change_pct

    def display_stats(self, coin):
        """Display current market statistics"""
        if not self.trades:
            return

        print(f"\n{'='*60}")
        print(f"📈 {coin} Market Analytics")
        print(f"{'='*60}")

        # VWAP
        vwap = self.get_vwap()
        print(f"💰 VWAP: ${vwap:.2f}")

        # Volume
        total_vol = self.get_total_volume()
        print(f"📊 Volume: {total_vol:.2f} (last {len(self.trades)} trades)")

        # Buy/Sell Ratio
        ratio = self.get_buy_sell_ratio()
        print(f"⚖️  Buy/Sell Ratio: {ratio:.2f}")

        # Average Spread
        avg_spread = self.get_avg_spread()
        print(f"📉 Avg Spread: ${avg_spread:.2f}")

        # Price Change
        change, change_pct = self.get_price_change()
        change_icon = "📈" if change >= 0 else "📉"
        print(f"{change_icon} Price Change: ${change:.2f} ({change_pct:+.2f}%)")

        # Latest Price
        if self.prices:
            print(f"💵 Latest Price: ${self.prices[-1]:.2f}")

        print(f"{'='*60}\n")


async def main():
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        return

    print(f"Connecting to {ws_url}...")
    websocket = await websockets.connect(ws_url)
    print("Connected!\n")

    # Subscribe to BTC trades
    trades_sub = {
        "method": "subscribe",
        "subscription": {
            "type": "trades",
            "coin": "BTC"
        }
    }
    await websocket.send(json.dumps(trades_sub))

    # Subscribe to BTC L2 book for spread tracking
    book_sub = {
        "method": "subscribe",
        "subscription": {
            "type": "l2Book",
            "coin": "BTC",
            "nLevels": 5,
            "nSigFigs": 5
        }
    }
    await websocket.send(json.dumps(book_sub))

    print("✓ Subscribed to BTC trades and order book")
    print("📊 Calculating market metrics...\n")

    analyzer = MarketAnalyzer(history_size=100)
    trade_count = 0
    display_interval = 5  # Display stats every 5 trades

    print("💭 Waiting for market data...\n")

    try:
        async for message in websocket:
            data = json.loads(message)
            channel = data.get("channel")

            if channel == "trades":
                # Process trades - data is a list of trade objects
                for trade in data["data"]:
                    analyzer.add_trade(
                        trade["px"],
                        trade["sz"],
                        trade["side"]
                    )
                    trade_count += 1

                    # Show trade
                    side_icon = "🟢" if trade["side"] == "B" else "🔴"
                    print(f"{side_icon} Trade: {trade['side']} {trade['sz']} @ ${trade['px']}")

                    # Display stats periodically
                    if trade_count % display_interval == 0:
                        analyzer.display_stats("BTC")

            elif channel == "l2Book":
                # Track spread
                levels = data["data"]["levels"]
                if levels[0] and levels[1]:
                    bid = float(levels[0][0]['px'])
                    ask = float(levels[1][0]['px'])
                    spread = ask - bid
                    analyzer.add_spread(spread)

    except KeyboardInterrupt:
        print("\nStopping...")
        analyzer.display_stats("BTC")  # Final stats
    finally:
        await websocket.close()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())