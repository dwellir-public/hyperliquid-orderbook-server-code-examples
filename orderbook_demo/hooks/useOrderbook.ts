'use client';

import { useEffect, useState, useRef } from 'react';
import { OrderbookData, OrderbookStats } from '@/types/orderbook';

interface UseOrderbookProps {
  wsUrl: string;
  coin: string;
  nLevels?: number;
  nSigFigs?: number;
  includeNLevels?: boolean; // Whether to include nLevels in subscription
}

export function useOrderbook({ wsUrl, coin, nLevels, nSigFigs = 5, includeNLevels = true }: UseOrderbookProps) {
  const [orderbook, setOrderbook] = useState<OrderbookData | null>(null);
  const [stats, setStats] = useState<OrderbookStats | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const updateCountRef = useRef(0);
  const lastBestBidRef = useRef<number>(0);
  const lastBestAskRef = useRef<number>(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const isManualCloseRef = useRef(false);

  useEffect(() => {
    let ws: WebSocket;
    isManualCloseRef.current = false;

    const connect = () => {
      try {
        ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
          console.log(`Connected to ${wsUrl}`);
          setIsConnected(true);
          setError(null);
          reconnectAttemptsRef.current = 0; // Reset reconnect attempts on successful connection

          // Subscribe to L2 orderbook
          const subscription: any = {
            method: 'subscribe',
            subscription: {
              type: 'l2Book',
              coin,
              nSigFigs,
            },
          };

          // Only include nLevels if requested (for comparison purposes)
          if (includeNLevels && nLevels) {
            subscription.subscription.nLevels = nLevels;
          }

          ws.send(JSON.stringify(subscription));
        };

        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);

            if (message.channel === 'l2Book') {
              const data: OrderbookData = message.data;
              setOrderbook(data);
              updateCountRef.current += 1;

              // Calculate stats
              const bids = data.levels[0] || [];
              const asks = data.levels[1] || [];

              if (bids.length > 0 && asks.length > 0) {
                const bestBid = parseFloat(bids[0].px);
                const bestAsk = parseFloat(asks[0].px);
                const spread = bestAsk - bestBid;
                const spreadPercent = (spread / bestBid) * 100;

                // Check if best bid or ask changed (only true when there's an actual change)
                const priceChanged =
                  (lastBestBidRef.current !== 0 && bestBid !== lastBestBidRef.current) ||
                  (lastBestAskRef.current !== 0 && bestAsk !== lastBestAskRef.current);

                lastBestBidRef.current = bestBid;
                lastBestAskRef.current = bestAsk;

                const now = Date.now();

                setStats({
                  totalBids: bids.length,
                  totalAsks: asks.length,
                  bestBid,
                  bestAsk,
                  spread,
                  spreadPercent,
                  lastUpdate: now,
                  updateCount: updateCountRef.current,
                  priceChanged,
                  lastPriceChangeTime: priceChanged ? now : 0,
                });
              }
            }
          } catch (err) {
            console.error('Error parsing message:', err);
          }
        };

        ws.onerror = (err) => {
          console.error('WebSocket error:', err);
          setError('Connection error');
          setIsConnected(false);
        };

        ws.onclose = () => {
          console.log('WebSocket closed');
          setIsConnected(false);

          // Only attempt reconnection if it wasn't a manual close
          if (!isManualCloseRef.current) {
            const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000); // Max 30 seconds
            console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttemptsRef.current + 1})`);

            reconnectTimeoutRef.current = setTimeout(() => {
              reconnectAttemptsRef.current += 1;
              connect();
            }, delay);
          }
        };
      } catch (err) {
        console.error('Failed to connect:', err);
        setError('Failed to connect');

        // Retry connection on error
        if (!isManualCloseRef.current) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000);
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current += 1;
            connect();
          }, delay);
        }
      }
    };

    connect();

    return () => {
      isManualCloseRef.current = true;

      // Clear any pending reconnection attempts
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }

      // Close the WebSocket connection
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [wsUrl, coin, nLevels, nSigFigs, includeNLevels]);

  return { orderbook, stats, isConnected, error };
}
