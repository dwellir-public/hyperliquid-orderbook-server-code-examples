# 03 - Multiple Subscriptions

## What You'll Learn
- Subscribe to multiple coins simultaneously
- Handle different message types (trades + order books)
- Route messages to appropriate handlers

## Key Concepts

### Multiple Subscriptions
You can subscribe to as many data feeds as needed:
- Different coins (BTC, ETH, SOL, etc.)
- Different data types (trades, l2Book, l4Book)
- Mix and match as needed

### Message Routing
Since all messages come through one WebSocket connection, you need to:
1. Check the `channel` field to identify the message type
2. Route to the appropriate handler function
3. Process each message type differently

### Pattern Structure
```python
def route_message(data):
    channel = data.get("channel")
    if channel == "trades":
        handle_trade(data)
    elif channel == "l2Book":
        handle_l2_book(data)
```

## Run the Example
```bash
python multiple_subscriptions.py
```

You'll see:
- BTC trade updates (when trades occur)
- ETH trade updates (when trades occur)
- SOL L2 order book updates (frequent, real-time)
- All streaming simultaneously

This demonstrates:
- **Mixed data types**: Trades (BTC, ETH) + Order book (SOL)
- **Different update frequencies**: Trades are sporadic, L2 updates constantly
- **Message routing**: Handling multiple channels in one connection

**Note**: Trades happen every few seconds to minutes. The SOL order book provides continuous updates so you see immediate activity.