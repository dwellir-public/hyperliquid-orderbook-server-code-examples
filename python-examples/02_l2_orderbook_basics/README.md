# 02 - L2 Order Book Basics

## What You'll Learn
- How to subscribe to L2 (aggregated) order book data
- Understanding bid/ask spreads
- Price aggregation with `nSigFigs` and `nLevels`

## Key Concepts

### L2 Order Book
- **Aggregated view**: Multiple orders at the same price level are combined
- Shows total size at each price level
- Number of orders at that level

### Parameters
- `nLevels`: How many price levels to receive (1-100, default 20)
- `nSigFigs`: Price aggregation precision (2-5)
  - Lower = more aggregation (broader view)
  - Higher = more precision (detailed view)

### Spread
The difference between the best bid (highest buy price) and best ask (lowest sell price)
- Narrow spread = liquid market
- Wide spread = less liquid market

## Run the Example
```bash
python l2_orderbook.py
```

You'll see:
- Top 5 ask levels (sellers)
- Current spread in $ and %
- Top 5 bid levels (buyers)
- Real-time updates as the order book changes