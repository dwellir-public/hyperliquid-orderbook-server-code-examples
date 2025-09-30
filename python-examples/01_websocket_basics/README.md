# 01 - WebSocket Basics

## What You'll Learn
- How to connect to a WebSocket server
- Subscribe to a data feed
- Receive and display real-time messages

## Key Concepts

### WebSocket Connection
WebSockets provide a persistent, bidirectional connection between client and server:
- Unlike HTTP (request/response), WebSockets stay open
- Server can push data to you in real-time
- Perfect for live market data

### Basic Flow
1. **Connect** - Establish WebSocket connection
2. **Subscribe** - Tell the server what data you want
3. **Listen** - Receive and process incoming messages
4. **Disconnect** - Close connection when done

### Subscription Message
```python
{
    "method": "subscribe",
    "subscription": {
        "type": "trades",
        "coin": "BTC"
    }
}
```

This tells the server: "Send me all BTC trades as they happen"

## Run the Example
```bash
python websockt_basics.py
```

You'll see:
- Connection confirmation
- Subscription confirmation
- Real-time BTC trade data streaming in
- Each trade shows: side (buy/sell), size, price, timestamp

## What's Next?
Once you understand basic WebSocket connections, move on to:
- **02_l2_orderbook_basics** - More complex data structures (order books)
- Understanding different data types
- Processing structured market data