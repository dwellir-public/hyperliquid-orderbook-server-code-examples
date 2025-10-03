# Orderbook Comparison Demo

A Next.js application that demonstrates the real-time differences between **Dwellir's Hyperliquid orderbook infrastructure** and the **public Hyperliquid API**.

## 🎯 What This Demo Shows

This application connects to both APIs simultaneously and displays:

- **Side-by-side orderbook comparison** in real-time
- **Depth metrics** showing the number of available price levels
- **Visual value proposition** highlighting why Dwellir's infrastructure matters
- **Live statistics** including spreads, updates, and market depth

## 🚀 Key Differences Highlighted

### Dwellir Infrastructure ✨
- **100 Price Levels** - Full market depth visibility
- **Configurable Levels** - Request exactly what you need (1-100)
- **Enhanced Analytics** - Better trading insights with deep liquidity data
- **Professional Infrastructure** - High availability & low latency

### Public API Limitations ⚠️
- **Limited Depth** - Typically only ~20 levels available
- **No Level Control** - Can't specify number of levels
- **Shallow Insights** - Missing deep liquidity information
- **Best Effort Service** - No SLA guarantees

## 📋 Prerequisites

- Node.js 18+
- npm or yarn
- A Dwellir API key (get one at [dwellir.com](https://dwellir.com))

## 🛠️ Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.local.example .env.local
   ```

3. **Edit `.env.local` and add your Dwellir WebSocket URL:**
   ```env
   NEXT_PUBLIC_DWELLIR_WS_URL=wss://api-hyperliquid-mainnet-orderbook.n.dwellir.com/YOUR-API-KEY/ws
   NEXT_PUBLIC_PUBLIC_WS_URL=wss://api.hyperliquid.xyz/ws
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📊 What You'll See

### Real-time Comparison
- **Left Panel:** Dwellir's orderbook with up to 100 price levels
- **Right Panel:** Public API orderbook with limited levels
- **Stats Cards:** Live metrics showing the exact difference in data availability

### Value Proposition Display
The app clearly shows:
- Number of levels from each API
- Percentage difference in market depth
- Use cases that require deep orderbook data
- Advantages of Dwellir's infrastructure

## 🎨 Features

- **Live WebSocket Connections** to both APIs
- **Real-time Updates** showing orderbook changes
- **Connection Status Indicators** (green = connected, red = disconnected)
- **Responsive Design** works on desktop and mobile
- **Dark Mode UI** optimized for trading environments

## 💡 Use Cases Demonstrated

This depth of data is critical for:

- **Market Making & Liquidity Provision** - Need to see deep book to place competitive orders
- **Large Order Execution** - Calculate optimal TWAP/VWAP strategies
- **Slippage Analysis** - Predict price impact of large trades
- **Arbitrage Detection** - Find opportunities across different price levels
- **Price Impact Modeling** - Understand how orders affect the market
- **Advanced Trading Algorithms** - Build sophisticated strategies with full market view

## 🏗️ Project Structure

```
orderbook_demo/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx            # Root layout
│   └── page.tsx              # Main comparison page
├── components/
│   ├── OrderbookDisplay.tsx  # Orderbook visualization
│   ├── StatsCard.tsx         # Statistics display
│   └── ValueProposition.tsx  # Value prop section
├── hooks/
│   └── useOrderbook.ts       # WebSocket hook for both APIs
├── types/
│   └── orderbook.ts          # TypeScript interfaces
└── .env.local                # Environment variables
```

## 🔧 Customization

You can modify the comparison by editing `app/page.tsx`:

```typescript
// Change the coin
const [coin] = useState('BTC'); // or 'SOL', 'AVAX', etc.

// Change the number of levels requested
const [nLevels] = useState(50); // 1-100

// Change price precision
nSigFigs: 5  // 2-5
```

## 📈 Build for Production

```bash
npm run build
npm start
```

## 🤝 Get Dwellir Access

To get your own Dwellir API key for production use:

- **Email:** [ben@dwellir.com](mailto:ben@dwellir.com)
- **Website:** [dwellir.com](https://dwellir.com)
- **Docs:** [dwellir.com/docs/hyperliquid](https://dwellir.com/docs/hyperliquid)

## 📝 License

MIT

## 🙋 Support

For issues or questions:
- Open an issue on GitHub
- Contact Dwellir at [ben@dwellir.com](mailto:ben@dwellir.com)

---

**Built with Next.js 14, React 18, TypeScript, and Tailwind CSS**
