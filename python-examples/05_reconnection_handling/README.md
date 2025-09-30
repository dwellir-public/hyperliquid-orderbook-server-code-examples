# 05 - Reconnection Handling

## What You'll Learn
- Handle connection failures gracefully
- Implement automatic reconnection with exponential backoff
- Maintain subscriptions across reconnections

## Key Concepts

### Why Reconnection Matters
WebSocket connections can drop due to:
- Network issues
- Server maintenance
- Timeout from inactivity
- Internet connectivity problems

A production-ready client must handle these gracefully.

### Exponential Backoff
Instead of hammering the server with reconnection attempts:
1. Start with short delay (1 second)
2. Double the delay after each failure (2s, 4s, 8s...)
3. Cap at maximum delay (60 seconds)
4. Reset delay on successful connection

This is respectful to the server and efficient.

### Subscription Tracking
The client tracks all subscriptions and automatically resubscribes when reconnecting:
```python
client.add_subscription("trades", "BTC")
client.add_subscription("l2Book", "ETH", nLevels=5)
```

If connection drops, all subscriptions are restored automatically.

## Run the Example
```bash
python robust_client.py
```

**Try this**: While the client is running, disconnect your network or WiFi. Watch it automatically reconnect and resume when connectivity returns!

## Production Tips
- Always implement reconnection logic
- Track and restore subscriptions
- Use exponential backoff
- Log connection events
- Consider adding health checks