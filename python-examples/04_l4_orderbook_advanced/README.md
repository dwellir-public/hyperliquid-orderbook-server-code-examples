# 04 - L4 Order Book (Advanced)

## What You'll Learn
- Subscribe to L4 (individual order) data
- Track every single order in the book
- Understand the difference between L2 (aggregated) and L4 (individual)

## Key Concepts

### L4 vs L2 Order Book

**L2 (Aggregated)**
- Shows total size at each price level
- Multiple orders combined
- Lighter data, good for market overview

**L4 (Individual Orders)**
- Shows every single order separately
- Full order details (user, size, price)
- More data, good for detailed analysis
- Can see individual trader behavior

### L4 Order Structure
Each order includes:
- `oid`: Order ID
- `user`: Trader address
- `side`: "B" (buy) or "A" (sell)
- `limitPx`: Limit price
- `sz`: Order size
- `status`: Order status (present when order is removed/filled)

### Order Tracking
The example maintains:
- Dictionary of all active orders by ID
- Orders grouped by price level
- Real-time updates as orders are added/removed/filled

## Run the Example
```bash
python l4_orderbook.py
```

You'll see:
- Every individual order in the book
- Top 5 individual asks
- Top 5 individual bids
- Trader addresses (truncated for privacy)
- Real-time updates as orders change

**Note**: L4 data updates much more frequently than L2!