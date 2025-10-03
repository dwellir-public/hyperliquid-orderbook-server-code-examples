'use client';

import { useState } from 'react';
import { useOrderbook } from '@/hooks/useOrderbook';
import { OrderbookDisplay } from '@/components/OrderbookDisplay';
import { StatsCard } from '@/components/StatsCard';
import { LagIndicator } from '@/components/LagIndicator';

const DWELLIR_WS = process.env.NEXT_PUBLIC_DWELLIR_WS_URL || '';
const PUBLIC_WS = process.env.NEXT_PUBLIC_PUBLIC_WS_URL || 'wss://api.hyperliquid.xyz/ws';

export default function Home() {
  const [coin] = useState('ETH');
  const [nLevels] = useState(100);

  // Dwellir connection with 100 levels
  const dwellir = useOrderbook({
    wsUrl: DWELLIR_WS,
    coin,
    nLevels,
    nSigFigs: 5,
  });

  // Public API connection (without nLevels parameter to show default behavior)
  const publicApi = useOrderbook({
    wsUrl: PUBLIC_WS,
    coin,
    nSigFigs: 5,
  });

  const dwellirLevels = dwellir.stats?.totalBids || 0;
  const publicLevels = publicApi.stats?.totalBids || 0;

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            Hyperliquid Orderbook Comparison
          </h1>
          <p className="text-gray-400">
            Real-time comparison: Dwellir&apos;s Premium Infrastructure vs Public API
          </p>
        </div>

        {/* Lag Indicator */}
        <LagIndicator dwellirStats={dwellir.stats} publicStats={publicApi.stats} />

        {/* Stats Cards */}
        <div className="mb-4 text-center">
          <p className="text-gray-400 text-sm">
            💡 Watch the price boxes flash when best bid/ask changes - Dwellir updates first, then Public API follows with a delay
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <StatsCard
            stats={dwellir.stats}
            isConnected={dwellir.isConnected}
            title="🚀 Dwellir Infrastructure"
            isPremium={true}
          />
          <StatsCard
            stats={publicApi.stats}
            isConnected={publicApi.isConnected}
            title="🌐 Public Hyperliquid API"
          />
        </div>

        {/* Orderbook Comparison */}
        <div className="mb-4 text-center">
          <h2 className="text-2xl font-bold text-purple-400 mb-2">Side-by-Side Orderbook Comparison</h2>
          <p className="text-gray-400 text-sm">
            Notice how the Dwellir side shows {dwellirLevels} levels while Public API shows only {publicLevels} levels
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-gradient-to-b from-purple-900/30 to-gray-900/50 border-2 border-purple-500 rounded-lg p-6 shadow-lg shadow-purple-500/20">
            <div className="mb-2 text-center">
              <span className="inline-block px-3 py-1 bg-purple-600 text-white text-xs font-bold rounded-full">
                ✨ PREMIUM - {dwellirLevels} LEVELS
              </span>
            </div>
            <OrderbookDisplay
              orderbook={dwellir.orderbook}
              title={`💎 Dwellir Infrastructure - ${coin}`}
              maxDisplay={100}
            />
          </div>

          <div className="bg-gray-900/50 border border-gray-700 rounded-lg p-6">
            <div className="mb-2 text-center">
              <span className="inline-block px-3 py-1 bg-gray-700 text-gray-300 text-xs font-bold rounded-full">
                📊 LIMITED - {publicLevels} LEVELS
              </span>
            </div>
            <OrderbookDisplay
              orderbook={publicApi.orderbook}
              title={`🌐 Public Hyperliquid API - ${coin}`}
              maxDisplay={100}
            />
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 p-6 bg-gray-900/50 border border-gray-700 rounded-lg text-center text-sm text-gray-400">
          <p className="mb-2">
            <strong className="text-purple-400">Dwellir Infrastructure:</strong> Configured for {nLevels} orderbook levels with guaranteed delivery
          </p>
          <p>
            <strong className="text-gray-300">Public API:</strong> Using default configuration (no nLevels parameter)
          </p>
          <p className="mt-4 text-xs">
            💡 Tip: Watch the &quot;Bid Levels&quot; and &quot;Ask Levels&quot; counters above to see the difference in real-time
          </p>
          <p className="mt-2 text-xs text-gray-500">
            Note: This demo shows the public API without the nLevels parameter to demonstrate default behavior. <br />
            Dwellir provides reliable, configurable depth with professional SLA and support.
          </p>
        </div>
      </div>
    </main>
  );
}
