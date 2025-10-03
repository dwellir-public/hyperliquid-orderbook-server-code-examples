#!/usr/bin/env python3
"""
Simple Hyperliquid WebSocket API Example using Dwellir
Subscribes to BTC trades and displays incoming messages
"""

import asyncio
import json
import os
import websockets
from dotenv import load_dotenv

load_dotenv()


async def main():
    # Get WebSocket URL from environment
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        print("Please create a .env file and set your WebSocket URL")
        return

    # Connect to WebSocket
    print(f"Connecting to {ws_url}...")
    websocket = await websockets.connect(ws_url)
    print("Connected!")

    # Subscribe to BTC trades
    subscribe_message = {
        "method": "subscribe",
        "subscription": {
            "type": "trades",
            "coin": "BTC"
        }
    }
    await websocket.send(json.dumps(subscribe_message))
    print("Subscribed to BTC trades\n")

    # Listen for messages
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {json.dumps(data, indent=2)}\n")

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await websocket.close()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())