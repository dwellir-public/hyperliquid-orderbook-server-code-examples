'use client';

import { useEffect, useState } from 'react';
import { OrderbookStats } from '@/types/orderbook';

interface LagIndicatorProps {
  dwellirStats: OrderbookStats | null;
  publicStats: OrderbookStats | null;
}

export function LagIndicator({ dwellirStats, publicStats }: LagIndicatorProps) {
  const [lag, setLag] = useState<number>(0);
  const [dwellirLastChange, setDwellirLastChange] = useState<number>(0);

  useEffect(() => {
    // When Dwellir price changes, record the time
    if (dwellirStats?.priceChanged && dwellirStats.lastPriceChangeTime > 0) {
      setDwellirLastChange(dwellirStats.lastPriceChangeTime);
    }
  }, [dwellirStats?.lastPriceChangeTime, dwellirStats?.priceChanged]);

  useEffect(() => {
    // When public API price changes, calculate lag from last Dwellir change
    if (publicStats?.priceChanged && publicStats.lastPriceChangeTime > 0 && dwellirLastChange > 0) {
      const calculatedLag = publicStats.lastPriceChangeTime - dwellirLastChange;
      if (calculatedLag > 0 && calculatedLag < 5000) { // Only show reasonable lags (< 5 seconds)
        setLag(calculatedLag);
      }
    }
  }, [publicStats?.lastPriceChangeTime, publicStats?.priceChanged, dwellirLastChange]);

  if (lag === 0) {
    return null;
  }

  return (
    <div className="mb-6 p-4 bg-gradient-to-r from-yellow-900/30 to-orange-900/30 border-2 border-yellow-500/50 rounded-lg">
      <div className="flex items-center justify-center gap-4">
        <div className="text-center">
          <div className="text-sm text-gray-400 mb-1">Public API Lag</div>
          <div className="text-3xl font-bold text-yellow-400">
            +{lag}ms
          </div>
        </div>
        <div className="text-gray-400">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </div>
        <div className="text-sm text-gray-300 max-w-md">
          Public API is receiving price updates <strong className="text-yellow-400">{lag}ms slower</strong> than Dwellir.
          In fast markets, this delay can cost you opportunities.
        </div>
      </div>
    </div>
  );
}
