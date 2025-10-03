'use client';

import { OrderbookStats } from '@/types/orderbook';

interface PerformanceComparisonProps {
  dwellirStats: OrderbookStats | null;
  publicStats: OrderbookStats | null;
}

export function PerformanceComparison({ dwellirStats, publicStats }: PerformanceComparisonProps) {
  if (!dwellirStats || !publicStats) {
    return null;
  }

  const updateSpeedDiff = dwellirStats.updatesPerSecond - publicStats.updatesPerSecond;
  const updateSpeedPercent = ((updateSpeedDiff / publicStats.updatesPerSecond) * 100).toFixed(0);

  const latencyDiff = publicStats.averageLatency - dwellirStats.averageLatency;
  const latencyPercent = ((latencyDiff / publicStats.averageLatency) * 100).toFixed(0);

  const isFasterUpdates = dwellirStats.updatesPerSecond > publicStats.updatesPerSecond;
  const isLowerLatency = dwellirStats.averageLatency < publicStats.averageLatency;

  return (
    <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 border-2 border-blue-500 rounded-lg p-6 mb-8">
      <h2 className="text-2xl font-bold mb-4 text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
        ⚡ Real-Time Performance Metrics
      </h2>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Update Frequency */}
        <div className="bg-black/40 p-4 rounded-lg">
          <h3 className="text-lg font-bold text-blue-400 mb-3 text-center">Update Frequency</h3>

          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">Dwellir:</span>
                <span className="text-green-400 font-bold">{dwellirStats.updatesPerSecond.toFixed(2)} Hz</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min((dwellirStats.updatesPerSecond / Math.max(dwellirStats.updatesPerSecond, publicStats.updatesPerSecond)) * 100, 100)}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">Public API:</span>
                <span className="text-blue-400 font-bold">{publicStats.updatesPerSecond.toFixed(2)} Hz</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min((publicStats.updatesPerSecond / Math.max(dwellirStats.updatesPerSecond, publicStats.updatesPerSecond)) * 100, 100)}%` }}
                />
              </div>
            </div>
          </div>

          {isFasterUpdates && (
            <div className="mt-4 p-3 bg-green-900/30 border border-green-500/30 rounded text-center">
              <div className="text-green-400 font-bold text-lg">+{Math.abs(parseFloat(updateSpeedPercent))}% Faster</div>
              <div className="text-xs text-gray-400">Dwellir delivers updates quicker</div>
            </div>
          )}
        </div>

        {/* Latency */}
        <div className="bg-black/40 p-4 rounded-lg">
          <h3 className="text-lg font-bold text-purple-400 mb-3 text-center">Network Latency</h3>

          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">Dwellir:</span>
                <span className="text-green-400 font-bold">{dwellirStats.averageLatency.toFixed(0)}ms</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min((dwellirStats.averageLatency / Math.max(dwellirStats.averageLatency, publicStats.averageLatency)) * 100, 100)}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">Public API:</span>
                <span className="text-yellow-400 font-bold">{publicStats.averageLatency.toFixed(0)}ms</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div
                  className="bg-yellow-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min((publicStats.averageLatency / Math.max(dwellirStats.averageLatency, publicStats.averageLatency)) * 100, 100)}%` }}
                />
              </div>
            </div>
          </div>

          {isLowerLatency && latencyDiff > 0 && (
            <div className="mt-4 p-3 bg-green-900/30 border border-green-500/30 rounded text-center">
              <div className="text-green-400 font-bold text-lg">{Math.abs(latencyDiff).toFixed(0)}ms Lower</div>
              <div className="text-xs text-gray-400">Dwellir has lower latency</div>
            </div>
          )}
        </div>
      </div>

      <div className="mt-6 p-4 bg-blue-900/20 rounded-lg border border-blue-500/30 text-center text-sm">
        <p className="text-gray-300">
          💡 <strong className="text-blue-400">Why This Matters:</strong> Higher update frequency and lower latency mean you get market changes faster,
          giving you an edge in fast-moving markets. Critical for market making, arbitrage, and algorithmic trading.
        </p>
      </div>
    </div>
  );
}
