#!/usr/bin/env python3
"""
Robust WebSocket Client with Reconnection
Handles disconnections and automatically reconnects
"""

import asyncio
import json
import os
import websockets
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class RobustWSClient:
    """WebSocket client with automatic reconnection"""

    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.websocket = None
        self.subscriptions = []  # Track active subscriptions
        self.is_running = False
        self.reconnect_delay = 1  # Start with 1 second
        self.max_reconnect_delay = 60  # Max 60 seconds

    def add_subscription(self, sub_type, coin, **kwargs):
        """Add a subscription to track"""
        sub = {
            "method": "subscribe",
            "subscription": {
                "type": sub_type,
                "coin": coin,
                **kwargs
            }
        }
        self.subscriptions.append(sub)

    async def connect(self):
        """Connect and subscribe to all tracked subscriptions"""
        try:
            self.websocket = await websockets.connect(self.ws_url)
            print(f"✅ Connected to {self.ws_url}")

            # Resubscribe to all subscriptions
            for sub in self.subscriptions:
                await self.websocket.send(json.dumps(sub))
                coin = sub["subscription"]["coin"]
                sub_type = sub["subscription"]["type"]
                print(f"✅ Subscribed to {coin} {sub_type}")

            # Reset reconnect delay on successful connection
            self.reconnect_delay = 1

        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise

    async def listen(self):
        """Listen for messages with automatic reconnection"""
        self.is_running = True

        while self.is_running:
            try:
                # Connect if not connected
                if not self.websocket:
                    await self.connect()

                # Listen for messages
                async for message in self.websocket:
                    data = json.loads(message)
                    self.handle_message(data)

            except websockets.exceptions.ConnectionClosed:
                print(f"⚠️  Connection closed. Reconnecting in {self.reconnect_delay}s...")
                await asyncio.sleep(self.reconnect_delay)

                # Exponential backoff
                self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                self.websocket = None

            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(self.reconnect_delay)
                self.websocket = None

    def handle_message(self, data):
        """Process incoming messages"""
        channel = data.get("channel")

        if channel == "trades":
            self.handle_trade(data)
        elif channel == "l2Book":
            self.handle_l2_book(data)
        else:
            print(f"Unknown channel: {channel}")

    def handle_trade(self, data):
        """Handle trade messages"""
        coin = data["data"]["coin"]
        for trade in data["data"]["trades"]:
            side_icon = "🟢" if trade["side"] == "B" else "🔴"
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"{side_icon} {coin}: {trade['side']} {trade['sz']} @ ${trade['px']} | {timestamp}")

    def handle_l2_book(self, data):
        """Handle L2 book messages"""
        coin = data["data"]["coin"]
        levels = data["data"]["levels"]

        if levels[0] and levels[1]:
            bid = levels[0][0]['px']
            ask = levels[1][0]['px']
            spread = float(ask) - float(bid)
            print(f"📊 {coin}: Bid ${bid} | Ask ${ask} | Spread ${spread:.2f}")

    async def stop(self):
        """Stop the client gracefully"""
        self.is_running = False
        if self.websocket:
            await self.websocket.close()
        print("Disconnected")


async def main():
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        return

    # Create robust client
    client = RobustWSClient(ws_url)

    # Add subscriptions
    client.add_subscription("trades", "BTC")
    client.add_subscription("l2Book", "ETH", nLevels=5, nSigFigs=4)

    print("🚀 Starting robust WebSocket client...")
    print("💡 Try disconnecting your network to see reconnection in action!\n")

    try:
        await client.listen()
    except KeyboardInterrupt:
        print("\nStopping...")
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())