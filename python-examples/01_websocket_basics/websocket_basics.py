#!/usr/bin/env python3
"""
Simple Hyperliquid WebSocket API Example using Dwellir
Subscribes to BTC trades and displays incoming messages

Supports curl-like --resolve behavior via env vars:

  WEBSOCKET_URL=wss://example.com/ws
  RESOLVE_HOST=example.com
  RESOLVE_IP=1.2.3.4
  RESOLVE_PORT=443   # optional, defaults to 443
"""

import asyncio
import json
import os
import socket

import websockets
from dotenv import load_dotenv

load_dotenv()


def apply_dns_override_from_env():
    """
    If RESOLVE_HOST and RESOLVE_IP are set, override DNS resolution
    for that host (and optional port) to the given IP.

    Returns a restore() function that will undo the override.
    If nothing is overridden, returns a no-op restore().
    """
    resolve_host = os.getenv("RESOLVE_HOST")
    resolve_ip = os.getenv("RESOLVE_IP")
    resolve_port_str = os.getenv("RESOLVE_PORT")

    if not (resolve_host and resolve_ip):
        # Nothing to override
        return lambda: None

    # Default port if not provided; adjust if you mostly use ws:// (80)
    resolve_port = int(resolve_port_str) if resolve_port_str else None

    original_getaddrinfo = socket.getaddrinfo

    def custom_getaddrinfo(host, port, *args, **kwargs):
        # Match host + (optionally) port
        if host == resolve_host and (resolve_port is None or port == resolve_port):
            return original_getaddrinfo(resolve_ip, port, *args, **kwargs)
        return original_getaddrinfo(host, port, *args, **kwargs)

    socket.getaddrinfo = custom_getaddrinfo

    def restore():
        socket.getaddrinfo = original_getaddrinfo

    return restore


async def main():
    # Get WebSocket URL from environment
    ws_url = os.getenv("WEBSOCKET_URL")

    if not ws_url:
        print("Error: WEBSOCKET_URL not found in .env file")
        print("Please create a .env file and set your WebSocket URL")
        return

    # Optionally override DNS for one host, curl --resolve style
    restore_dns = apply_dns_override_from_env()

    try:
        # Connect to WebSocket
        print(f"Connecting to {ws_url}...")
        websocket = await websockets.connect(ws_url)
        print("Connected!")

    except Exception as e:
        print(f"Failed to connect: {e}")
        # Restore DNS before exiting
        restore_dns()
        return

    # DNS is only needed during connect, safe to restore now
    restore_dns()

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
