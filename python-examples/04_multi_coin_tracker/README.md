# 04 - Multi-Coin Trade Tracker (Advanced)

## What You'll Learn
- Track trades from multiple coins simultaneously
- Organize data per coin with separate trackers
- Calculate comparative metrics (VWAP, volume, buy/sell ratio)
- Display a real-time dashboard across multiple assets

## Key Concepts

This example demonstrates an advanced pattern for multi-coin tracking:
- **Separate trackers per coin**: Each coin gets its own `CoinTracker` instance
- **Aggregated metrics**: Calculate VWAP, volume, and buy/sell ratios per coin
- **Comparative analysis**: Sort and display metrics to compare coin performance
- **Efficient data structures**: Use deque for sliding window of recent trades

## Run the Example
```bash
python multi_coin_tracker.py
```

You'll see a dashboard every 10 trades showing:
- Latest price and VWAP for each coin
- Total volume traded
- Buy/Sell ratio (indicates buying or selling pressure)
- Number of trades tracked

This pattern is useful for:
- Building trading dashboards
- Comparing multiple assets simultaneously
- Identifying which coins are most active
- Analyzing market sentiment across coins
