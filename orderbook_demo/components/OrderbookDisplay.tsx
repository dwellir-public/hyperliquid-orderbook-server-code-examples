'use client';

import { OrderbookData } from '@/types/orderbook';

interface OrderbookDisplayProps {
  orderbook: OrderbookData | null;
  title: string;
  maxDisplay?: number;
}

export function OrderbookDisplay({ orderbook, title, maxDisplay = 100 }: OrderbookDisplayProps) {
  if (!orderbook) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Connecting...</div>
      </div>
    );
  }

  const bids = orderbook.levels[0] || [];
  const asks = orderbook.levels[1] || [];

  // Display all available levels (don't limit artificially)
  const displayBids = bids;
  const displayAsks = asks;
  const maxRows = Math.max(displayBids.length, displayAsks.length);

  return (
    <div className="font-mono text-sm">
      <h3 className="text-lg font-bold mb-4 text-center">{title}</h3>

      {/* Header */}
      <div className="flex justify-between border-b border-gray-700 pb-2 mb-2 sticky top-0 bg-gray-900 z-10">
        <div className="flex-1 text-center">
          <div className="text-green-500 font-bold mb-1">BIDS</div>
          <div className="flex justify-between text-xs text-gray-400 px-2">
            <span>Price</span>
            <span>Size</span>
          </div>
        </div>
        <div className="w-px bg-gray-700 mx-4"></div>
        <div className="flex-1 text-center">
          <div className="text-red-500 font-bold mb-1">ASKS</div>
          <div className="flex justify-between text-xs text-gray-400 px-2">
            <span>Price</span>
            <span>Size</span>
          </div>
        </div>
      </div>

      {/* Orderbook rows - scrollable container */}
      <div className="space-y-0.5 max-h-[600px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-gray-900">
        {Array.from({ length: maxRows }).map((_, i) => {
          const bid = displayBids[i];
          const ask = displayAsks[maxRows - 1 - i];

          return (
            <div key={i} className="flex justify-between text-xs">
              {/* Bid side */}
              <div className="flex-1">
                {bid ? (
                  <div className="flex justify-between px-2 py-0.5 bg-green-900/20 hover:bg-green-900/30 rounded">
                    <span className="text-green-400">{parseFloat(bid.px).toFixed(2)}</span>
                    <span className="text-green-300">{parseFloat(bid.sz).toFixed(4)}</span>
                  </div>
                ) : (
                  <div className="h-6"></div>
                )}
              </div>

              <div className="w-px bg-gray-800 mx-4"></div>

              {/* Ask side */}
              <div className="flex-1">
                {ask ? (
                  <div className="flex justify-between px-2 py-0.5 bg-red-900/20 hover:bg-red-900/30 rounded">
                    <span className="text-red-400">{parseFloat(ask.px).toFixed(2)}</span>
                    <span className="text-red-300">{parseFloat(ask.sz).toFixed(4)}</span>
                  </div>
                ) : (
                  <div className="h-6"></div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Show total count at bottom */}
      <div className="mt-4 pt-2 border-t border-gray-700 text-center text-xs text-gray-400">
        Showing {displayBids.length} bid levels & {displayAsks.length} ask levels
      </div>
    </div>
  );
}
