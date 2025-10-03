import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Orderbook Demo - Dwellir vs Public API",
  description: "Real-time comparison of Dwellir's Hyperliquid orderbook infrastructure vs public API",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
