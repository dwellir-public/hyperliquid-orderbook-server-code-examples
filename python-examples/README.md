# Python Examples - Hyperliquid WebSocket API

Educational Python examples for working with Hyperliquid order book data via Dwellir's infrastructure.

## 📚 Example Progression

These examples follow a natural learning path from simple to advanced:

### [01 - WebSocket Basics](./01_websocket_basics/)
**Concepts**: Basic WebSocket connection, subscribing to trades

Simple example showing how to:
- Connect to the WebSocket API
- Subscribe to a single data feed (BTC trades)
- Listen for and display incoming messages
- Handle disconnection gracefully

**Start here** if you're new to WebSockets or the Hyperliquid API.

### [02 - L2 Order Book Basics](./02_l2_orderbook_basics/)
**Concepts**: Aggregated order books, bid/ask spreads, price levels

Learn about:
- L2 (aggregated) order book structure
- Understanding bids vs asks
- Calculating spreads
- Price aggregation parameters (`nLevels`, `nSigFigs`)

### [03 - Multiple Subscriptions](./03_multiple_subscriptions/)
**Concepts**: Multi-coin tracking, message routing, concurrent streams

Build on basics to:
- Subscribe to multiple coins simultaneously
- Handle different message types (trades + L2 books)
- Route messages to appropriate handlers
- Process multiple data streams efficiently

### [04 - L4 Order Book Advanced](./04_l4_orderbook_advanced/)
**Concepts**: Individual orders, L4 vs L2 data, order tracking

Deep dive into:
- L4 (individual order) data structure
- Difference between L2 and L4 order books
- Tracking individual orders and order IDs
- Managing order state (adds, updates, removes)

### [05 - Reconnection Handling](./05_reconnection_handling/)
**Concepts**: Production reliability, error handling, exponential backoff

Learn production-ready patterns:
- Automatic reconnection on failures
- Exponential backoff strategy
- Subscription restoration after reconnect
- Graceful error handling

### [06 - Data Analysis](./06_data_analysis/)
**Concepts**: Market metrics, VWAP, trading indicators

Calculate real-time metrics:
- Volume-Weighted Average Price (VWAP)
- Buy/Sell volume ratios
- Average spreads over time
- Price change percentages
- Rolling window analysis

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Access to a Dwellir Hyperliquid instance

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure your environment:**
```bash
cp .env.example .env
```

Edit `.env` and add your WebSocket URL:
```
WEBSOCKET_URL=wss://your-instance.dwellir.com/ws
```

Contact [ben@dwellir.com](mailto:ben@dwellir.com) to get your specific server details.

3. **Run any example:**
```bash
cd 01_websocket_basics
python websockt_basics.py
```

## 📖 How to Use These Examples

### For Learning
1. **Read the README** in each example directory first
2. **Review the code** - it's heavily commented
3. **Run the example** and observe the output
4. **Modify parameters** and see what changes
5. **Move to the next** example when comfortable

### For YouTube/Tutorials
Each example is designed to be explainable in 5-10 minutes:
- Clear, focused scope
- One or two main concepts
- Visual output that's easy to demonstrate
- Natural progression between examples

### For Building Your Own App
- Start with example 01 for basic connection
- Add example 05 for production reliability
- Choose the data type you need (L2 or L4)
- Adapt example 06 for your analytics needs

## 🔧 Code Structure

Each example follows this structure:
```
XX_example_name/
├── README.md          # Learning objectives and concepts
├── script_name.py     # Runnable code with comments
```

All examples are:
- **Self-contained** - can be run independently
- **Simple** - focus on teaching one concept well
- **Commented** - explain what's happening and why
- **Practical** - real, working code you can build on

## 📊 Available Data Types

### Trades Stream
```python
{
    "method": "subscribe",
    "subscription": {
        "type": "trades",
        "coin": "BTC"
    }
}
```
Real-time trade executions with price, size, side, and timestamp.

### L2 Order Book (Aggregated)
```python
{
    "method": "subscribe",
    "subscription": {
        "type": "l2Book",
        "coin": "ETH",
        "nLevels": 20,
        "nSigFigs": 5
    }
}
```
Aggregated price levels showing total size at each price point.

### L4 Order Book (Individual Orders)
```python
{
    "method": "subscribe",
    "subscription": {
        "type": "l4Book",
        "coin": "ETH"
    }
}
```
Every individual order with full details (user, price, size, order ID).

## 🎯 Common Patterns

### Basic Connection Pattern
```python
import asyncio
import websockets
import json

async def main():
    websocket = await websockets.connect(ws_url)
    await websocket.send(json.dumps(subscription))
    async for message in websocket:
        data = json.loads(message)
        # Process data
```

### Message Routing Pattern
```python
def route_message(data):
    channel = data.get("channel")
    if channel == "trades":
        handle_trades(data)
    elif channel == "l2Book":
        handle_l2_book(data)
```

### Reconnection Pattern
```python
while is_running:
    try:
        await connect_and_listen()
    except ConnectionClosed:
        await asyncio.sleep(reconnect_delay)
        reconnect_delay *= 2  # Exponential backoff
```

## 💡 Tips

- **Start simple**: Don't skip to advanced examples
- **Understand the data**: Print messages to see structure
- **Experiment**: Change parameters and subscriptions
- **Handle errors**: Network issues happen, plan for them
- **Rate limits**: Be respectful with subscriptions
- **Log everything**: Helps with debugging

## 🔗 Additional Resources

- [Dwellir Hyperliquid WebSocket API Docs](https://www.dwellir.com/docs/hyperliquid/websocket-api)
- [Hyperliquid Official Documentation](https://hyperliquid.gitbook.io/)
- [WebSocket Protocol (RFC 6455)](https://datatracker.ietf.org/doc/html/rfc6455)

## 📞 Support

- **Dwellir Infrastructure**: [ben@dwellir.com](mailto:ben@dwellir.com)
- **Issues with Examples**: Open an issue on GitHub
- **Feature Requests**: Pull requests welcome!

## ⚠️ Notes

- These are **educational examples**, not production code
- Focus is on **clarity and learning**, not optimization
- Always **test thoroughly** before using in production
- Add proper **error handling** and **logging** for real applications

---

Happy learning! 🚀