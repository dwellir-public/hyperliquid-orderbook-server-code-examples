# Example 07: L4 Order Book

This example demonstrates the L4 order book subscription, which provides **the most detailed market microstructure data** available from Hyperliquid.

## What's Different About L4?

- **Individual Order Visibility**: See each order separately with full details
- **User Addresses**: Know who placed each order
- **Order IDs**: Track specific orders over time
- **No Aggregation**: Unlike L2, orders are not grouped by price level

## Use Cases

- High-frequency trading strategies
- Market making with order-level analysis
- Liquidity analysis and depth profiling
- Advanced market microstructure research

## Running the Example

```bash
python l4_orderbook.py
```

## What You'll See

The script displays:
- Individual sell orders (asks) with user addresses
- Individual buy orders (bids) with user addresses
- Order IDs for tracking specific orders
- Bid-ask spread calculation
- Block height for blockchain synchronization

## L4 vs L2

| Feature | L2 (Aggregated) | L4 (Individual) |
|---------|----------------|-----------------|
| Orders  | Grouped by price | Each order separate |
| User Info | Not shown | User addresses visible |
| Order ID | Not shown | Full order IDs |
| Data Volume | Lower | Higher |
| Use Case | General trading | HFT, market making |

## Code Highlights

```python
subscribe_message = {
    "method": "subscribe",
    "subscription": {
        "type": "l4Book",
        "coin": "BTC"
    }
}
```

L4 books include:
- `user`: Address of the order placer
- `oid`: Unique order identifier
- `px`: Price level
- `sz`: Order size
- `height`: Block height for timing
