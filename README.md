# Hyperliquid Order Book Server - Code Examples

Educational code examples for connecting to Hyperliquid's order book data via Dwellir's high-performance infrastructure.

## 🎯 What is This?

This repository contains **simple, pedagogical examples** designed for learning how to work with Hyperliquid WebSocket data. Each example builds on the previous one, introducing new concepts progressively.

Perfect for:
- Learning WebSocket programming
- Understanding order book data structures
- Building real-time market data applications
- Creating YouTube tutorials and educational content

## 📚 Examples

### Python Examples

Located in `python-examples/`, these examples follow a natural learning progression:

1. **[01_websocket_basics](./python-examples/01_websocket_basics/)** - Connect and subscribe to BTC trades
2. **[02_l2_orderbook_basics](./python-examples/02_l2_orderbook_basics/)** - L2 aggregated order book with spread visualization
3. **[03_multiple_subscriptions](./python-examples/03_multiple_subscriptions/)** - Handle multiple coins and data types simultaneously
4. **[04_l4_orderbook_advanced](./python-examples/04_l4_orderbook_advanced/)** - Track individual orders with L4 data
5. **[05_reconnection_handling](./python-examples/05_reconnection_handling/)** - Robust client with automatic reconnection
6. **[06_data_analysis](./python-examples/06_data_analysis/)** - Calculate market metrics (VWAP, spreads, volume)

Each example includes:
- Clean, commented code
- README with learning objectives
- Runnable examples
- Clear explanations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Access to a Dwellir Hyperliquid instance (contact [ben@dwellir.com](mailto:ben@dwellir.com))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dwellir-public/hyperliquid-orderbook-server-code-examples.git
cd hyperliquid-orderbook-server-code-examples
```

2. Set up Python environment:
```bash
cd python-examples
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure your WebSocket URL:
```bash
cp .env.example .env
# Edit .env and add your Dwellir WebSocket URL
```

4. Run any example:
```bash
cd 01_websocket_basics
python websockt_basics.py
```

## 📖 Documentation

Each example directory contains its own README with:
- **What You'll Learn** - Key concepts covered
- **Code Explanation** - Line-by-line breakdown
- **Run Instructions** - How to execute the example
- **Next Steps** - Where to go from here

Start with [python-examples/README.md](./python-examples/README.md) for a complete guide.

## 🎓 Learning Path

**Beginner** → Start with examples 01-03
- Basic WebSocket connections
- Understanding order book data
- Handling multiple data streams

**Intermediate** → Continue with examples 04-05
- Advanced order book data (L4)
- Production-ready error handling
- Reconnection strategies

**Advanced** → Finish with example 06
- Real-time data analysis
- Market metrics calculation
- Building trading indicators

## 🌟 Features

- **Simple & Clean**: Code is easy to read and understand
- **Well Documented**: Every example includes explanations
- **Progressive Learning**: Each example builds on previous concepts
- **Production Patterns**: Learn best practices for real applications
- **YouTube Ready**: Perfect for creating educational content

## 🔗 WebSocket API

All examples connect to Hyperliquid's order book data via Dwellir's infrastructure:

**Available Data Types:**
- **Trades** - Real-time trade executions
- **L2 Book** - Aggregated order book levels
- **L4 Book** - Individual order details

**Why Dwellir?**
- Ultra-low latency (median improvement of 51ms / 24.1%)
- High reliability and uptime
- Optimized for market data streaming
- Professional infrastructure

Learn more: [Dwellir Hyperliquid WebSocket API Docs](https://www.dwellir.com/docs/hyperliquid/websocket-api)

## 📞 Support

- **Dwellir Access**: Contact [ben@dwellir.com](mailto:ben@dwellir.com) for server details
- **Issues**: Open an issue on this repository
- **Hyperliquid API**: See [official Hyperliquid documentation](https://hyperliquid.gitbook.io/)

## ⚠️ Disclaimer

These examples are for **educational purposes only**. They demonstrate how to connect to and process market data, but are not intended for production trading without significant additional development.

## 📜 License

MIT License - Feel free to use these examples in your own projects and tutorials.

---

**Built with ❤️ by [Dwellir](https://www.dwellir.com)** - Professional blockchain infrastructure