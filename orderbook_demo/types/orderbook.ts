export interface OrderLevel {
  px: string;  // price
  sz: string;  // size
  n: number;   // number of orders
}

export interface OrderbookData {
  coin: string;
  levels: [OrderLevel[], OrderLevel[]]; // [bids, asks]
  time: number;
}

export interface OrderbookMessage {
  channel: string;
  data: OrderbookData;
}

export interface OrderbookStats {
  totalBids: number;
  totalAsks: number;
  bestBid: number;
  bestAsk: number;
  spread: number;
  spreadPercent: number;
  lastUpdate: number;
  updateCount: number;
  priceChanged: boolean;
  lastPriceChangeTime: number;
}
