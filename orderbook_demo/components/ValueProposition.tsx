'use client';

interface ValuePropositionProps {
  dwellirLevels: number;
  publicLevels: number;
}

export function ValueProposition({ dwellirLevels, publicLevels }: ValuePropositionProps) {
  const difference = dwellirLevels - publicLevels;
  const percentageMore = publicLevels > 0 ? ((difference / publicLevels) * 100).toFixed(0) : '0';

  return (
    <div className="bg-gradient-to-r from-purple-900/30 to-blue-900/30 border-2 border-purple-500 rounded-lg p-6 mb-8">
      <h2 className="text-2xl font-bold mb-4 text-center bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
        Why Dwellir&apos;s Infrastructure Matters
      </h2>

      <div className="grid md:grid-cols-3 gap-4 mb-6">
        <div className="bg-black/40 p-4 rounded-lg text-center">
          <div className="text-3xl font-bold text-purple-400 mb-2">{dwellirLevels}</div>
          <div className="text-sm text-gray-300">Dwellir Levels</div>
        </div>

        <div className="bg-black/40 p-4 rounded-lg text-center">
          <div className="text-3xl font-bold text-red-400 mb-2">{publicLevels}</div>
          <div className="text-sm text-gray-300">Public API Levels</div>
        </div>

        <div className="bg-black/40 p-4 rounded-lg text-center">
          <div className="text-3xl font-bold text-green-400 mb-2">+{percentageMore}%</div>
          <div className="text-sm text-gray-300">More Market Depth</div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-4 text-sm">
        <div className="space-y-3">
          <h3 className="font-bold text-purple-400 mb-2">✨ Dwellir Advantages:</h3>
          <div className="flex items-start gap-2">
            <span className="text-green-500">✓</span>
            <span><strong>100 Price Levels</strong> - Full market depth visibility</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-green-500">✓</span>
            <span><strong>Configurable Levels</strong> - Request exactly what you need (1-100)</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-green-500">✓</span>
            <span><strong>Enhanced Analytics</strong> - Better trading insights with deep liquidity data</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-green-500">✓</span>
            <span><strong>Professional Infrastructure</strong> - High availability & low latency</span>
          </div>
        </div>

        <div className="space-y-3">
          <h3 className="font-bold text-red-400 mb-2">⚠️ Public API Limitations:</h3>
          <div className="flex items-start gap-2">
            <span className="text-red-500">✗</span>
            <span><strong>Default Limited Depth</strong> - Returns ~20 levels by default</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-red-500">✗</span>
            <span><strong>Unpredictable Behavior</strong> - Level control may or may not work</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-red-500">✗</span>
            <span><strong>No Infrastructure SLA</strong> - Best effort availability</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-red-500">✗</span>
            <span><strong>No Support</strong> - Community-based troubleshooting only</span>
          </div>
        </div>
      </div>

      <div className="mt-6 p-4 bg-purple-900/20 rounded-lg border border-purple-500/30">
        <h4 className="font-bold text-purple-300 mb-2">💡 Use Cases That Require Deep Orderbook Data:</h4>
        <div className="grid md:grid-cols-2 gap-2 text-sm text-gray-300">
          <div>• Market Making & Liquidity Provision</div>
          <div>• Large Order Execution (TWAP/VWAP)</div>
          <div>• Slippage Analysis & Prediction</div>
          <div>• Arbitrage Detection</div>
          <div>• Price Impact Modeling</div>
          <div>• Advanced Trading Algorithms</div>
        </div>
      </div>
    </div>
  );
}
