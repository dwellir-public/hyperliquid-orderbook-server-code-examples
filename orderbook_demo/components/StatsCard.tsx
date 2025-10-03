'use client';

import { useEffect, useState } from 'react';
import { OrderbookStats } from '@/types/orderbook';

interface StatsCardProps {
  stats: OrderbookStats | null;
  isConnected: boolean;
  title: string;
  isPremium?: boolean;
}

export function StatsCard({ stats, isConnected, title, isPremium = false }: StatsCardProps) {
  const [isFlashing, setIsFlashing] = useState(false);
  const [lastUpdateTime, setLastUpdateTime] = useState(0);

  useEffect(() => {
    if (stats?.priceChanged && stats?.lastUpdate !== lastUpdateTime) {
      setIsFlashing(true);
      setLastUpdateTime(stats.lastUpdate);
      const timer = setTimeout(() => setIsFlashing(false), 80);
      return () => clearTimeout(timer);
    }
  }, [stats?.lastUpdate, stats?.priceChanged, lastUpdateTime]);

  return (
    <div className={`p-4 rounded-lg border-2 ${
      isPremium ? 'border-purple-500 bg-purple-900/10' : 'border-gray-700 bg-gray-900/50'
    }`}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-bold text-lg">{title}</h3>
        <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
      </div>

      {stats ? (
        <div className="space-y-2 font-mono text-sm">
          <div className="flex justify-between">
            <span className="text-gray-400">Bid Levels:</span>
            <span className={isPremium ? 'text-purple-400 font-bold' : 'text-green-400'}>{stats.totalBids}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Ask Levels:</span>
            <span className={isPremium ? 'text-purple-400 font-bold' : 'text-red-400'}>{stats.totalAsks}</span>
          </div>

          <div className={`border-2 rounded-lg p-3 my-2 transition-all duration-100 ${
            isFlashing
              ? (isPremium ? 'border-purple-400 bg-purple-500/25 shadow-lg shadow-purple-500/60' : 'border-blue-400 bg-blue-500/25 shadow-lg shadow-blue-500/60')
              : 'border-gray-700 bg-gray-800/30'
          }`}>
            <div className="flex justify-between mb-2">
              <span className="text-gray-400">Best Bid:</span>
              <span className="text-green-400 font-bold text-lg">
                ${stats.bestBid.toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Best Ask:</span>
              <span className="text-red-400 font-bold text-lg">
                ${stats.bestAsk.toFixed(2)}
              </span>
            </div>
          </div>

          <div className="flex justify-between">
            <span className="text-gray-400">Spread:</span>
            <span className="text-yellow-400">${stats.spread.toFixed(4)} ({stats.spreadPercent.toFixed(4)}%)</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Total Updates:</span>
            <span className="text-blue-400">{stats.updateCount}</span>
          </div>
        </div>
      ) : (
        <div className="text-gray-500 text-center py-4">Waiting for data...</div>
      )}
    </div>
  );
}
