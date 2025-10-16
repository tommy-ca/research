---
date: 2025-10-16
type: capture
tags: [tardis-node, cryptocurrency, market-data, research, typescript, data-types]
status: draft
sources:
  - https://github.com/tardis-dev/tardis-node
  - https://docs.tardis.dev
  - https://docs.tardis.dev/api/node-js
---

# Tardis-Node Library: Comprehensive Data Types and Structure Research

## Executive Summary

Tardis-node is a TypeScript library providing tick-level access to both historical and real-time cryptocurrency market data across 56+ exchanges. The library implements a sophisticated normalization system that transforms exchange-native formats into unified data structures, enabling consistent consumption across all supported venues.

**Key Features:**
- Historical replay via tardis.dev HTTP API
- Real-time streaming via exchange WebSocket APIs
- Both raw and normalized data formats
- Full order book reconstruction
- Derived data computation (trade bars, snapshots)
- Built-in caching with GZIP compression
- 100-nanosecond timestamp precision

---

## 1. Core Normalized Data Types

All normalized messages inherit from a base structure with common metadata fields.

### 1.1 Base Type: NormalizedData

```typescript
type NormalizedData = {
  readonly type: string
  readonly symbol: string
  readonly exchange: Exchange
  readonly timestamp: Date          // Exchange-reported timestamp
  readonly localTimestamp: Date     // Client-received timestamp
  readonly name?: string            // Optional identifier for computed data
}
```

### 1.2 Trade

**Type:** `'trade'`

**Description:** Individual tick-by-tick trade executions representing liquidity taker/aggressor transactions.

**Fields:**
```typescript
type Trade = {
  readonly type: 'trade'
  readonly symbol: string
  readonly exchange: Exchange
  readonly id: string | undefined        // Exchange-specific trade identifier
  readonly price: number                 // Execution price
  readonly amount: number                // Trade quantity
  readonly side: 'buy' | 'sell' | 'unknown'  // Taker side
  readonly timestamp: Date
  readonly localTimestamp: Date
}
```

**Important Notes:**
- `side` represents the liquidity taker/aggressor direction
- `id` may be undefined for exchanges that don't provide trade IDs
- Off-book trades (insurance fund, ADL) are filtered out in some mappers

### 1.3 BookChange

**Type:** `'book_change'`

**Description:** Order book Level 2 updates representing price level changes.

**Fields:**
```typescript
type BookPriceLevel = {
  readonly price: number
  readonly amount: number
}

type BookChange = {
  readonly type: 'book_change'
  readonly symbol: string
  readonly exchange: Exchange
  readonly isSnapshot: boolean           // True for full snapshots
  readonly bids: BookPriceLevel[]        // Bid price levels
  readonly asks: BookPriceLevel[]        // Ask price levels
  readonly timestamp: Date
  readonly localTimestamp: Date
}
```

**Important Notes:**
- `isSnapshot: true` indicates full order book state
- `isSnapshot: false` indicates incremental update
- `amount: 0` in an update indicates level removal
- Amount values are absolute, not deltas
- Daily snapshots captured at 00:00 UTC
- Some exchanges generate snapshots via REST API when native snapshots unavailable

### 1.4 DerivativeTicker

**Type:** `'derivative_ticker'`

**Description:** Aggregated derivative-specific metrics for futures and perpetual contracts.

**Fields:**
```typescript
type DerivativeTicker = {
  readonly type: 'derivative_ticker'
  readonly symbol: string
  readonly exchange: Exchange
  readonly lastPrice: number | undefined
  readonly openInterest: number | undefined
  readonly fundingRate: number | undefined
  readonly fundingTimestamp: Date | undefined
  readonly predictedFundingRate: number | undefined
  readonly indexPrice: number | undefined
  readonly markPrice: number | undefined
  readonly timestamp: Date
  readonly localTimestamp: Date
}
```

**Important Notes:**
- Not all fields available for all exchanges
- Funding rates typically updated every 8 hours
- Uses pending ticker helper pattern for aggregation

### 1.5 BookTicker

**Type:** `'book_ticker'`

**Description:** Top-of-book best bid/ask snapshots.

**Fields:**
```typescript
type BookTicker = {
  readonly type: 'book_ticker'
  readonly symbol: string
  readonly exchange: Exchange
  readonly askPrice: number | undefined
  readonly askAmount: number | undefined
  readonly bidPrice: number | undefined
  readonly bidAmount: number | undefined
  readonly timestamp: Date
  readonly localTimestamp: Date
}
```

**Use Case:** Efficient for tracking best bid/offer without full order book depth.

### 1.6 OptionSummary

**Type:** `'option_summary'`

**Description:** Options chain data including Greeks and volatility metrics.

**Fields:**
```typescript
type OptionSummary = NormalizedData & {
  readonly optionType: 'call' | 'put'
  readonly strikePrice: number
  readonly expirationDate: Date
  readonly askPrice: number | undefined
  readonly askAmount: number | undefined
  readonly askIv: number | undefined        // Implied volatility
  readonly bidPrice: number | undefined
  readonly bidAmount: number | undefined
  readonly bidIv: number | undefined
  readonly delta: number | undefined
  readonly gamma: number | undefined
  readonly vega: number | undefined
  readonly theta: number | undefined
  readonly rho: number | undefined
  readonly markPrice: number | undefined
  readonly openInterest: number | undefined
  readonly underlyingPrice: number | undefined
  readonly underlyingIndex: string | undefined
}
```

**Important Notes:**
- Greeks may not be available for all exchanges
- IV calculated at both bid and ask sides when available

### 1.7 Liquidation

**Type:** `'liquidation'`

**Description:** Forced liquidation events on derivative exchanges.

**Fields:**
```typescript
type Liquidation = {
  readonly type: 'liquidation'
  readonly symbol: string
  readonly exchange: Exchange
  readonly id: string | undefined
  readonly price: number
  readonly amount: number
  readonly side: 'buy' | 'sell' | 'unknown'
  readonly timestamp: Date
  readonly localTimestamp: Date
}
```

**Important Notes:**
- Only filled liquidation orders included (filtered)
- Critical for market microstructure analysis

### 1.8 Disconnect

**Type:** `'disconnect'`

**Description:** Connection loss indicator for real-time streams.

**Fields:**
```typescript
type Disconnect = {
  readonly type: 'disconnect'
  readonly exchange: Exchange
  readonly timestamp: Date
  readonly localTimestamp: Date
  readonly symbols?: string[]
}
```

**Important Notes:**
- Stateful mappers reset on disconnect events
- Important for replay consistency

---

## 2. Computed/Derived Data Types

### 2.1 TradeBar

**Type:** `'trade_bar'`

**Description:** Aggregated OHLCV trade data across time, volume, or tick intervals.

**Configuration:**
```typescript
type TradeBarComputableOptions = {
  kind: 'time' | 'volume' | 'tick'
  interval: number
  name?: string
}
```

**Fields:**
```typescript
type TradeBar = {
  readonly type: 'trade_bar'
  readonly symbol: string
  readonly exchange: Exchange
  readonly name: string
  readonly interval: number
  readonly kind: 'time' | 'volume' | 'tick'
  readonly open: number
  readonly high: number
  readonly low: number
  readonly close: number
  readonly volume: number              // Total volume
  readonly buyVolume: number           // Taker buy volume
  readonly sellVolume: number          // Taker sell volume
  readonly trades: number              // Trade count
  readonly vwap: number                // Volume-weighted average price
  readonly openTimestamp: Date
  readonly closeTimestamp: Date
  readonly timestamp: Date
  readonly localTimestamp: Date
}
```

**Bar Completion Triggers:**
- **Time-based:** When exchange timestamp crosses interval boundary (milliseconds)
- **Volume-based:** When cumulative amount reaches threshold
- **Tick-based:** When trade count reaches threshold

**Important Notes:**
- Handles out-of-order trades with timestamp validation
- High/low update regardless of timestamp ordering
- Close price only updates for chronologically later trades

### 2.2 BookSnapshot

**Type:** `'book_snapshot'`

**Description:** Periodic order book depth snapshots with optional price grouping.

**Configuration:**
```typescript
type BookSnapshotComputableOptions = {
  name?: string
  depth: number                        // Number of price levels
  grouping?: number                    // Price level aggregation interval
  interval: number                     // Millisecond snapshot frequency
  removeCrossedLevels?: boolean
  onCrossedLevelRemoved?: (crossedLevel: any) => void
}
```

**Fields:**
```typescript
type BookSnapshot = {
  readonly type: 'book_snapshot'
  readonly symbol: string
  readonly exchange: Exchange
  readonly name: string
  readonly depth: number
  readonly interval: number
  readonly grouping: number | undefined
  readonly bids: BookPriceLevel[]
  readonly asks: BookPriceLevel[]
  readonly timestamp: Date
  readonly localTimestamp: Date
}
```

**Snapshot Generation:**
- **interval = 0:** Real-time snapshots on every book change
- **interval > 0:** Time-bucketed snapshots at specified millisecond intervals
- Change detection optimizes unnecessary snapshot generation

**Price Grouping:**
- Bid prices rounded down to grouping increment
- Ask prices rounded up to grouping increment
- Enables aggregated order book views

---

## 3. Mapper Architecture

### 3.1 Mapper Interface

All exchange-specific mappers implement this contract:

```typescript
export type Mapper<T extends Exchange, U extends NormalizedData> = {
  canHandle: (message: any) => boolean
  map(message: any, localTimestamp: Date): IterableIterator<U> | undefined
  getFilters: (symbols?: string[]) => FilterForExchange[T][]
}
```

**Methods:**

1. **canHandle(message):** Determines if mapper can process the message
2. **map(message, localTimestamp):** Transforms raw exchange data to normalized format
3. **getFilters(symbols?):** Generates exchange-specific subscription filters

### 3.2 Normalization Factory Functions

Three primary normalizers available:

1. **normalizeTrades** - Trade execution standardization
2. **normalizeBookChanges** - Order book update standardization
3. **normalizeDerivativeTickers** - Derivative metrics standardization

**Customization:** Developers can replace, extend, or modify built-in normalizers without forking.

### 3.3 Exchange-Specific Mappers

The library includes 42 mapper files for different exchanges:

**Major Mappers:**
- `binance.ts` - Binance spot and futures
- `coinbase.ts` - Coinbase Pro
- `deribit.ts` - Deribit derivatives
- `ftx.ts` - FTX (legacy)
- `kraken.ts` - Kraken spot and futures
- `okex.ts` - OKX spot/futures/options
- `bybit.ts` - Bybit derivatives

**Mapper Implementation Pattern:**
- Uses generator functions (`*map()`) for memory efficiency
- Stateful mappers maintain per-symbol state (e.g., order book buffers)
- Filters out exchange-specific anomalies (off-book trades, invalid orders)
- Buffers updates until snapshots arrive for book change mappers

---

## 4. Supported Exchanges and Channels

### 4.1 Exchange List (56 Total)

**Major Exchanges:**
- Binance (Spot, Futures, US, DEX, Jersey, Coin-M Futures)
- Coinbase Pro
- Kraken (Spot, Futures)
- OKX (Spot, Futures, Swap, Options)
- Bybit (Spot, Derivatives)
- Deribit
- FTX (historical)
- Huobi (Global, Futures, Swap, Linear Swap)
- Gate.io (Spot, Futures)
- KuCoin

**Regional & Specialized:**
- Upbit, bitFlyer, Bitstamp, Gemini, Poloniex
- Hyperliquid, dYdX, Serum
- Delta Exchange, Phemex, CoinFLEX

### 4.2 Common Data Channels by Exchange

**Binance:**
- `trade`, `aggTrade`, `ticker`, `depth`, `markPrice`, `bookTicker`, `forceOrder`, `openInterest`

**Deribit:**
- `book`, `trades`, `ticker`, `deribit_price_index`, `perpetual`, `platform_state`

**Coinbase:**
- `match`, `received`, `open`, `done`, `l2update`, `ticker`, `snapshot`

**OKEx:**
- `trades`, `books`, `tickers`, `mark-price`, `funding-rate`, `liquidations`, `open-interest`

**Kraken:**
- `trade`, `ticker`, `book`, `spread`

**Channel Definitions:** Stored in `EXCHANGE_CHANNELS_INFO` object mapping each exchange to its available data streams.

---

## 5. Data Quality and Specifications

### 5.1 Timestamp Precision

- **Collection Precision:** 100-nanosecond precision using synchronized GCP clocks
- **Storage Format:** ISO 8601 UTC timestamps
- **Dual Timestamps:**
  - `timestamp` - Exchange-reported time
  - `localTimestamp` - Client receipt time

**Monotonicity:** Exchanges may publish non-sequential timestamps within single channels (requires handling).

### 5.2 Data Collection Infrastructure

**Location:** Google Cloud Platform Kubernetes Clusters
- London (europe-west2)
- Tokyo (asia-northeast1)

**Collection Method:**
- Primary: Real-time WebSocket feeds (preferred for completeness)
- Fallback: Periodic REST API calls

**Health Monitoring:**
- Subscription validation (20-second timeout)
- Heartbeat ping monitoring
- Order book sequence number validation
- JSON format validation
- Stale connection detection
- Message volume anomaly detection

### 5.3 Data Delay and Availability

- **Real-time delay:** ~6 minutes from exchange to availability
- **Daily snapshots:** Captured at 00:00 UTC
- **Snapshot gaps:** 300-3000ms during daily re-subscription
- **Generated snapshots:** Used for exchanges without native snapshots (Binance, Bitstamp, Coinbase Pro)

### 5.4 Data Quality Considerations

**Known Issues:**
- Exchange-published duplicate trade messages (requires deduplication)
- Occasionally crossed order books (bid/ask overlap) in historical data
- Non-complete data due to exchange outages or connection issues
- Out-of-order message delivery on some channels

**Handling:**
- Mappers filter anomalous data (off-book trades, invalid orders)
- Book change mappers buffer updates until snapshots arrive
- Validation rules specific to exchange characteristics (e.g., stricter validation for Binance Futures)

---

## 6. CSV Data Formats

### 6.1 Format Standards

- **Delimiter:** Comma (,)
- **Line ending:** \n (LF)
- **Decimal mark:** . (dot)
- **Timestamps:** Microseconds since Unix epoch
- **Timezone:** UTC

### 6.2 Available CSV Dataset Types

#### incremental_book_L2
Tick-level order book updates from WebSocket feeds.

**Schema:**
```
exchange, symbol, timestamp, local_timestamp, is_snapshot, side, price, amount
```

#### book_snapshot_25 / book_snapshot_5
Reconstructed order book snapshots (top 25 or top 5 levels).

**Schema:**
```
exchange, symbol, timestamp, local_timestamp,
asks[0..24].price, asks[0..24].amount,
bids[0..24].price, bids[0..24].amount
```

#### trades
Individual trade records.

**Schema:**
```
exchange, symbol, timestamp, local_timestamp, id, side, price, amount
```

#### options_chain
Options summary with Greeks.

**Schema:**
```
exchange, symbol, timestamp, local_timestamp,
strike_price, expiration, open_interest, last_price,
bid_price, bid_amount, bid_iv,
ask_price, ask_amount, ask_iv,
mark_price, underlying_index, underlying_price,
delta, gamma, vega, theta, rho
```

#### quotes
Best bid/ask data.

**Schema:**
```
exchange, symbol, timestamp, local_timestamp,
ask_price, ask_amount, bid_price, bid_amount
```

#### derivative_ticker
Futures/perpetual metrics.

**Schema:**
```
exchange, symbol, timestamp, local_timestamp,
funding_timestamp, funding_rate, open_interest,
last_price, index_price, mark_price
```

#### liquidations
Forced liquidation events.

**Schema:**
```
exchange, symbol, timestamp, local_timestamp,
id, side, price, amount
```

### 6.3 Grouped Symbols

Special symbol values for bulk downloads:
- **SPOT** - All spot trading pairs
- **FUTURES** - All futures contracts
- **OPTIONS** - All options contracts

---

## 7. Type System Overview

### 7.1 Core Type Definitions

```typescript
// Exchange type derived from constants
type Exchange = (typeof EXCHANGES)[number]

// Generic filter type
type Filter<T> = {
  channel: T
  symbols?: string[]
}

// Exchange-specific filter mapping
type FilterForExchange = {
  [key in Exchange]: Filter<(typeof EXCHANGE_CHANNELS_INFO)[key][number]>
}

// Utility types
type Writeable<T> = { -readonly [P in keyof T]: T[P] }
type Optional<T> = { [P in keyof T]: T[P] | undefined }
```

### 7.2 Message Type Hierarchy

```
NormalizedData (base)
├── Trade
├── BookChange
├── DerivativeTicker
├── BookTicker
├── OptionSummary
├── Liquidation
├── Disconnect
└── Computed Types
    ├── TradeBar
    └── BookSnapshot
```

### 7.3 Raw Exchange Message Types

Each mapper defines exchange-specific raw types (example from Binance):

```typescript
type BinanceTradeData = {
  e: string                    // Event type
  E: number                    // Event time
  s: string                    // Symbol
  t: number                    // Trade ID
  p: string                    // Price
  q: string                    // Quantity
  T: number                    // Trade time
  m: boolean                   // Is buyer maker
  M: boolean                   // Ignore
}

type BinanceDepthData = {
  e: string                    // Event type
  E: number                    // Event time
  s: string                    // Symbol
  U: number                    // First update ID
  u: number                    // Final update ID
  b: [string, string][]        // Bids
  a: [string, string][]        // Asks
}
```

---

## 8. Integration and Usage Patterns

### 8.1 Installation

```bash
npm install tardis-dev --save
```

**Requirements:** Node.js v12+

### 8.2 Basic Usage Patterns

**Historical Replay:**
```javascript
const messages = replay({
  exchange: 'binance',
  from: '2025-01-01',
  to: '2025-01-02',
  filters: [
    { channel: 'trade', symbols: ['BTCUSDT'] }
  ]
})

for await (const message of messages) {
  console.log(message)
}
```

**Real-time Streaming:**
```javascript
const messages = stream({
  exchange: 'binance',
  filters: [
    { channel: 'trade', symbols: ['BTCUSDT'] }
  ]
})

for await (const message of messages) {
  console.log(message)
}
```

**Computed Trade Bars:**
```javascript
const messages = compute(
  replay({ /* config */ }),
  [
    { type: 'trade_bar', kind: 'time', interval: 60000 }  // 1-minute bars
  ]
)
```

### 8.3 Normalization Usage

```javascript
import { normalizeTrades, normalizeBookChanges } from 'tardis-dev'

const normalizedMessages = replay({
  exchange: 'binance',
  filters: [{ channel: 'trade', symbols: ['BTCUSDT'] }],
  withDisconnects: true
}, normalizeTrades, normalizeBookChanges)
```

---

## 9. Key Implementation Notes

### 9.1 Memory Efficiency

- Generator-based iteration prevents loading entire datasets into memory
- Streaming architecture supports processing arbitrarily large historical datasets
- GZIP compression for local caching

### 9.2 State Management

- **Stateful Mappers:** Book change mappers maintain per-symbol buffers
- **Reset on Disconnect:** Stateful state cleared on disconnect events
- **Snapshot Synchronization:** Updates buffered until snapshot arrives

### 9.3 Error Handling

- **Validation:** Sequence number checking for order books
- **Filtering:** Anomalous data removed (off-book trades, invalid orders)
- **Graceful Degradation:** Undefined values for unavailable fields

### 9.4 Performance Considerations

- **Book Change Buffering:** May accumulate updates if snapshot delayed
- **Overlap Validation:** Different strategies for spot vs. futures (stricter validation for futures)
- **Crossed Level Removal:** Optional callback for monitoring data quality issues

---

## 10. Advanced Features

### 10.1 Multi-Exchange Feed Combining

Combine data from multiple exchanges into single stream:

```javascript
const combined = combine(
  stream({ exchange: 'binance', filters: [...] }),
  stream({ exchange: 'coinbase', filters: [...] })
)
```

### 10.2 Local Data Caching

Automatic caching with GZIP compression reduces API calls for repeated historical queries.

### 10.3 Order Book Reconstruction

Full limit order book state maintained through:
1. Initial snapshot
2. Incremental updates applied sequentially
3. Periodic re-snapshots for validation

### 10.4 Custom Normalizers

Replace built-in normalizers:

```javascript
function customTradeNormalizer(exchange, timestamp) {
  return {
    canHandle: (message) => { /* custom logic */ },
    map: function* (message, localTimestamp) {
      // Custom transformation
      yield normalizedTrade
    },
    getFilters: (symbols) => { /* custom filters */ }
  }
}
```

---

## 11. Research Findings Summary

### 11.1 Strengths

1. **Comprehensive Coverage:** 56+ exchanges with consistent API
2. **Dual Format Support:** Both raw and normalized data
3. **High Precision:** 100-nanosecond timestamp resolution
4. **Flexible Computation:** Built-in derived data with custom options
5. **Type Safety:** Full TypeScript support with detailed type definitions
6. **Memory Efficient:** Generator-based streaming architecture
7. **Quality Monitoring:** Multiple health check and validation layers

### 11.2 Considerations

1. **Data Completeness:** Subject to exchange outages and connection issues
2. **Timestamp Ordering:** Non-monotonic timestamps require handling
3. **Crossed Books:** Occasional bid/ask inversions in historical data
4. **Snapshot Gaps:** 300-3000ms gaps during daily re-subscription
5. **Exchange Differences:** Varying field availability across venues
6. **Duplicate Messages:** Exchange-level duplicates require deduplication

### 11.3 Normalization Approach

**Philosophy:** Standardize structure while preserving exchange-specific semantics

**Key Principles:**
- Unified field names across exchanges
- Consistent timestamp handling (dual timestamps)
- Type safety with TypeScript
- Extensible mapper architecture
- Optional field handling for exchange differences
- Filter-based anomaly removal

### 11.4 Recommended Use Cases

1. **Quantitative Research:** Tick-level data for strategy backtesting
2. **Market Microstructure Analysis:** Trade flow and order book dynamics
3. **Cross-Exchange Arbitrage:** Unified format simplifies multi-venue analysis
4. **Machine Learning:** Consistent features across exchanges
5. **Risk Management:** Historical volatility and liquidation analysis
6. **Market Making:** Order book depth and spread analytics

---

## 12. References and Resources

### Official Documentation
- **Main Docs:** https://docs.tardis.dev
- **Node.js API:** https://docs.tardis.dev/api/node-js
- **GitHub Repository:** https://github.com/tardis-dev/tardis-node

### Source Files
- **Type Definitions:** `/src/types.ts`
- **Constants:** `/src/consts.ts`
- **Mappers:** `/src/mappers/` (42 exchange-specific files)
- **Computed Types:** `/src/computable/`

### Key Concepts
- **PARA Method:** Used in repository organization
- **MPL-2.0 License:** Open-source with specific permissions
- **Repository Stats:** 343 stars, 74 forks, 1,081 commits (as of research date)

---

## Validation and Confidence Assessment

### Source Quality: HIGH
- Official GitHub repository with active maintenance
- Comprehensive documentation site
- TypeScript source code directly reviewed
- Multiple independent documentation sources cross-referenced

### Information Completeness: HIGH
- All major data types documented with field definitions
- Mapper architecture fully specified
- Exchange coverage comprehensive
- Type system complete

### Technical Accuracy: HIGH
- Source code directly examined
- Type definitions extracted from TypeScript
- Normalization logic reviewed in mapper implementations
- CSV schemas documented in official docs

### Known Gaps
- Specific exchange channel mappings not exhaustively documented
- Some raw exchange message types not fully detailed
- Performance benchmarks not available
- Pricing/API limits not covered in technical research

---

*Research conducted: 2025-10-16*
*Primary sources: GitHub repository, official documentation, TypeScript definitions*
*Confidence level: High (95%+)*
