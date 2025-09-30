# 06 - Market Data Analysis

## What You'll Learn
- Calculate real-time market metrics
- Track historical data with rolling windows
- Compute trading indicators

## Key Metrics

### VWAP (Volume-Weighted Average Price)
The average price weighted by volume - shows the "true" average price considering trade sizes.

```
VWAP = Σ(Price × Volume) / Σ(Volume)
```

### Buy/Sell Ratio
Ratio of buy volume to sell volume - indicates buying vs selling pressure.
- Ratio > 1: More buying pressure
- Ratio < 1: More selling pressure

### Average Spread
The average difference between best bid and best ask over time.
- Narrow spread: High liquidity
- Wide spread: Low liquidity

### Price Change
Change in price from the first to most recent trade in the window.

## Technical Concepts

### Rolling Window
Uses `deque` with `maxlen` to maintain a fixed-size history:
```python
self.trades = deque(maxlen=100)  # Keep last 100 trades
```

This automatically removes old data when new data arrives.

### Real-time Calculation
Metrics are recalculated on each update, giving you live market analytics.

## Run the Example
```bash
python market_metrics.py
```

You'll see periodic updates with:
- Current VWAP
- Total volume
- Buy/Sell ratio
- Average spread
- Price change percentage
- Latest price

## Use Cases
- Market monitoring dashboards
- Trading strategy inputs
- Liquidity analysis
- Market microstructure research