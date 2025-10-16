---
date: 2025-10-16
type: research
tags: [cryptofeed, tardis-node, dbn, schema-mapping, market-data, crypto]
status: draft
links:
  - "[[202510160000-cryptofeed-data-types-research]]"
  - "[[20251016-tardis-node-comprehensive-research]]"
  - "[[20251016-databento-dbn-schema-research]]"
source: synthesis
confidence: high
---

# Crypto Market Data Schema Mapping: DBN Extensions for Cryptofeed and Tardis-Node

## Executive Summary

This document provides a comprehensive mapping between cryptofeed (15 data types), tardis-node (8 normalized + 2 computed types), and Databento's DBN fixed schema format (20+ record types). It identifies direct mappings, partial coverage, and gaps that require new DBN record types to support the full range of cryptocurrency market data.

**Key Findings:**
- **Direct mappings:** 5 types (Trades, MBP/OrderBook, OHLCV/Candles)
- **Partial coverage:** 3 types (BBO/L1Book, DerivativeTicker, Statistics)
- **New types needed:** 12 crypto-specific types (Funding, Liquidations, Index, authenticated data, etc.)
- **Proposed extensions:** 12 new RType values (0x30-0x3B range)

---

## 1. Schema Mapping Matrix

### 1.1 Complete Type Comparison

| Data Type | Cryptofeed | Tardis-Node | DBN Schema | Coverage | Notes |
|-----------|------------|-------------|------------|----------|-------|
| **Trades** | Trade | Trade | Trades (RType 0) | ✅ FULL | Direct mapping, all fields covered |
| **Order Book L2** | OrderBook | BookChange | MBP-1/10 (RType 1,10) | ✅ FULL | Price-aggregated depth |
| **Order Book L3** | OrderBook | N/A | MBO (RType 160) | ✅ FULL | Order-level data |
| **Candles/Bars** | Candle | TradeBar | OHLCV (RType 32-36) | ✅ FULL | Multiple timeframes |
| **Best Bid/Offer** | L1Book | BookTicker | BBO1S/1M (RType 195-196) | ⚠️ PARTIAL | Missing continuous updates |
| **Ticker** | Ticker | N/A | ❌ MISSING | ❌ NONE | Need new type |
| **Funding** | Funding | DerivativeTicker | ❌ MISSING | ❌ NONE | Crypto perpetual contracts |
| **Open Interest** | OpenInterest | DerivativeTicker | Statistics (RType 24) | ⚠️ PARTIAL | Generic stats, not specific |
| **Liquidations** | Liquidation | Liquidation | ❌ MISSING | ❌ NONE | Crypto-specific forced closes |
| **Index Price** | Index | N/A | ❌ MISSING | ❌ NONE | Derivative pricing reference |
| **Order Info** | OrderInfo | N/A | ❌ MISSING | ❌ NONE | Authenticated order status |
| **Order** | Order | N/A | ❌ MISSING | ❌ NONE | Authenticated order placement |
| **Fill** | Fill | N/A | ❌ MISSING | ❌ NONE | Authenticated execution |
| **Balance** | Balance | N/A | ❌ MISSING | ❌ NONE | Authenticated account data |
| **Position** | Position | N/A | ❌ MISSING | ❌ NONE | Authenticated derivative positions |
| **Transaction** | Transaction | N/A | ❌ MISSING | ❌ NONE | Deposits/withdrawals |
| **Option Summary** | N/A | OptionSummary | ❌ MISSING | ❌ NONE | Options chain with Greeks |
| **Derivative Ticker** | N/A | DerivativeTicker | ❌ MISSING | ❌ NONE | Comprehensive derivative metrics |
| **Disconnect** | N/A | Disconnect | System (RType 23) | ⚠️ PARTIAL | Can use System messages |
| **Book Snapshot** | N/A | BookSnapshot | MBP snapshots | ✅ FULL | Computed from book changes |

**Coverage Summary:**
- ✅ **Full Coverage:** 5 types (25%)
- ⚠️ **Partial Coverage:** 4 types (20%)
- ❌ **Missing:** 11 types (55%)

---

## 2. Detailed Field Mappings

### 2.1 Direct Mappings (Full Coverage)

#### 2.1.1 Trade → DBN Trades (RType 0)

**Cryptofeed Trade:**
```python
{
    exchange: str
    symbol: str
    side: str                 # BUY/SELL
    amount: Decimal
    price: Decimal
    timestamp: float          # Unix seconds
    id: str                   # Optional
    type: str                 # Optional
}
```

**Tardis-Node Trade:**
```typescript
{
    type: 'trade'
    symbol: string
    exchange: Exchange
    id: string | undefined
    price: number
    amount: number
    side: 'buy' | 'sell' | 'unknown'
    timestamp: Date
    localTimestamp: Date
}
```

**DBN TradeMsg (RType 0):**
```rust
{
    hd: RecordHeader {
        rtype: 0
        publisher_id: u16      // → exchange
        instrument_id: u32     // → symbol (mapped)
        ts_event: u64          // → timestamp (ns)
    }
    price: i64                 // → price (1e-9 scale)
    size: u32                  // → amount
    action: c_char             // 'T'
    side: c_char               // → side (A=Ask/B=Bid)
    flags: FlagSet
    depth: u8
    ts_recv: u64               // → localTimestamp
    ts_in_delta: i32
    sequence: u32              // → id (if numeric)
}
```

**Mapping Notes:**
- ✅ All essential fields covered
- Side mapping: BUY→'B', SELL→'A'
- Price precision: Decimal → i64 (1e-9 scale)
- Timestamp: seconds → nanoseconds conversion

#### 2.1.2 OrderBook/BookChange → DBN MBP (RType 1, 10)

**Cryptofeed OrderBook:**
```python
{
    exchange: str
    symbol: str
    book.bids: SortedDict[price, size]
    book.asks: SortedDict[price, size]
    delta: {BID: [(price, size)], ASK: [(price, size)]}
    sequence_number: int
    timestamp: float
}
```

**Tardis-Node BookChange:**
```typescript
{
    type: 'book_change'
    symbol: string
    exchange: Exchange
    isSnapshot: boolean
    bids: [{price: number, amount: number}]
    asks: [{price: number, amount: number}]
    timestamp: Date
    localTimestamp: Date
}
```

**DBN Mbp10Msg (RType 10):**
```rust
{
    hd: RecordHeader
    price: i64                 // Update price
    size: u32                  // Update size
    action: c_char             // A/C/M/R
    side: c_char               // A/B
    flags: FlagSet
    depth: u8
    ts_recv: u64
    ts_in_delta: i32
    sequence: u32              // → sequence_number
    levels: [BidAskPair; 10]   // Top 10 levels
}
```

**Mapping Notes:**
- ✅ Full depth representation
- Delta updates map to action codes (A=Add, C=Cancel, M=Modify)
- Snapshot vs incremental: isSnapshot → flags
- Levels: SortedDict → BidAskPair array

#### 2.1.3 Candle/TradeBar → DBN OHLCV (RType 32-36)

**Cryptofeed Candle:**
```python
{
    exchange: str
    symbol: str
    start: float
    stop: float
    interval: str             # "1m", "5m", "1h", "1d"
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    trades: int               # Optional
    closed: bool
}
```

**Tardis-Node TradeBar:**
```typescript
{
    type: 'trade_bar'
    kind: 'time' | 'volume' | 'tick'
    interval: number
    open: number
    high: number
    low: number
    close: number
    volume: number
    buyVolume: number
    sellVolume: number
    trades: number
    vwap: number
    openTimestamp: Date
    closeTimestamp: Date
}
```

**DBN OhlcvMsg (RType 32-36):**
```rust
{
    hd: RecordHeader {
        ts_event: u64          // → closeTimestamp (bar end)
    }
    open: i64                  // → open (1e-9 scale)
    high: i64                  // → high
    low: i64                   // → low
    close: i64                 // → close
    volume: u64                // → volume
}
```

**RType Mapping by Interval:**
- 1-second: RType 32 (Ohlcv1S)
- 1-minute: RType 33 (Ohlcv1M)
- 1-hour: RType 34 (Ohlcv1H)
- 1-day: RType 35 (Ohlcv1D)
- EOD: RType 36 (OhlcvEod)

**Mapping Notes:**
- ✅ OHLCV fields perfectly aligned
- ⚠️ Missing: trades count, buyVolume, sellVolume, vwap
- ⚠️ Missing: start timestamp (only close in ts_event)
- Interval mapping: string/number → RType selection

---

### 2.2 Partial Mappings

#### 2.2.1 L1Book/BookTicker → DBN BBO (RType 195-196)

**Cryptofeed L1Book:**
```python
{
    exchange: str
    symbol: str
    bid_price: Decimal
    bid_size: Decimal
    ask_price: Decimal
    ask_size: Decimal
    timestamp: float
}
```

**Tardis-Node BookTicker:**
```typescript
{
    type: 'book_ticker'
    askPrice: number | undefined
    askAmount: number | undefined
    bidPrice: number | undefined
    bidAmount: number | undefined
    timestamp: Date
}
```

**DBN BboMsg (RType 195-196):**
```rust
{
    hd: RecordHeader
    price: i64                 // Last trade price
    size: u32                  // Last trade size
    side: c_char
    flags: FlagSet
    ts_recv: u64
    sequence: u32
    levels: [BidAskPair; 1]    // Single BBO level
}
```

**Gap Analysis:**
- ✅ BidAskPair structure supports bid/ask price and size
- ⚠️ DBN BBO is subsampled (1S or 1M intervals)
- ⚠️ L1Book/BookTicker are continuous real-time updates
- **Solution:** Need new RType for continuous L1 updates

#### 2.2.2 OpenInterest → DBN Statistics (RType 24)

**Cryptofeed OpenInterest:**
```python
{
    exchange: str
    symbol: str
    open_interest: Decimal
    timestamp: float
}
```

**DBN StatMsg (RType 24):**
```rust
{
    hd: RecordHeader
    ts_recv: u64
    ts_ref: u64
    price: i64                 // Statistical value
    quantity: i32              // Could map to OI
    sequence: u32
    stat_type: u16             // Need OI type code
    channel_id: u16
    update_action: u8
    stat_flags: u8
}
```

**Gap Analysis:**
- ⚠️ Can use quantity field for open interest
- ⚠️ Need specific stat_type code for open interest
- ⚠️ Generic statistics message, not specific to derivatives
- **Solution:** Define stat_type=1 for OpenInterest, or create dedicated type

---

## 3. Missing Types: Gap Analysis

### 3.1 Crypto-Specific Market Data

#### 3.1.1 Ticker

**Cryptofeed Ticker:**
```python
{
    exchange: str
    symbol: str
    bid: Decimal              # Best bid price
    ask: Decimal              # Best ask price
    timestamp: float          # Optional
}
```

**Current DBN:** ❌ No equivalent
- BBO includes trade data, not just quotes
- L1Book includes sizes, Ticker doesn't

**Proposed:** New RType for lightweight ticker quotes

#### 3.1.2 Funding Rate

**Cryptofeed Funding:**
```python
{
    exchange: str
    symbol: str               # Perpetual contract
    mark_price: Decimal       # Optional
    rate: Decimal             # Current funding rate
    next_funding_time: float  # Optional
    predicted_rate: Decimal   # Optional
    timestamp: float
}
```

**Tardis-Node DerivativeTicker (includes funding):**
```typescript
{
    type: 'derivative_ticker'
    fundingRate: number | undefined
    fundingTimestamp: Date | undefined
    predictedFundingRate: number | undefined
    markPrice: number | undefined
    indexPrice: number | undefined
    lastPrice: number | undefined
    openInterest: number | undefined
}
```

**Current DBN:** ❌ No equivalent
**Proposed:** New RType for perpetual contract funding data

#### 3.1.3 Liquidations

**Cryptofeed Liquidation:**
```python
{
    exchange: str
    symbol: str
    side: str                 # LONG/SHORT position liquidated
    quantity: Decimal
    price: Decimal
    id: str
    status: str
    timestamp: float
}
```

**Tardis-Node Liquidation:**
```typescript
{
    type: 'liquidation'
    id: string | undefined
    price: number
    amount: number
    side: 'buy' | 'sell' | 'unknown'
    timestamp: Date
}
```

**Current DBN:** ❌ No equivalent
**Proposed:** New RType for forced liquidation events

#### 3.1.4 Index Price

**Cryptofeed Index:**
```python
{
    exchange: str
    symbol: str               # Index symbol
    price: Decimal            # Index value
    timestamp: float
}
```

**Current DBN:** ❌ No equivalent
- Could use Statistics (RType 24) with specific stat_type
- Better: Dedicated index price type

**Proposed:** New RType for index pricing data

### 3.2 Authenticated/Private Data

#### 3.2.1 Order Info (Order Status)

**Cryptofeed OrderInfo:**
```python
{
    exchange: str
    symbol: str
    id: str                   # Exchange order ID
    client_order_id: str
    side: str                 # BUY/SELL
    status: str               # OPEN/FILLED/CANCELLED/etc.
    type: str                 # LIMIT/MARKET/etc.
    price: Decimal
    amount: Decimal
    remaining: Decimal        # Unfilled amount
    account: str
    timestamp: float
}
```

**Current DBN:** ❌ No equivalent
**Proposed:** New RType for order status tracking

#### 3.2.2 Order (Placement)

**Cryptofeed Order:**
```python
{
    exchange: str
    symbol: str
    client_order_id: str
    side: str                 # BUY/SELL
    type: str                 # LIMIT/MARKET
    price: Decimal
    amount: Decimal
    account: str
    timestamp: float
}
```

**Current DBN:** ❌ No equivalent
**Proposed:** New RType for order placement records

#### 3.2.3 Fill (Trade Execution)

**Cryptofeed Fill:**
```python
{
    exchange: str
    symbol: str
    price: Decimal
    amount: Decimal
    side: str                 # BUY/SELL
    fee: Decimal              # Optional
    id: str                   # Fill ID
    order_id: str             # Parent order ID
    liquidity: str            # MAKER/TAKER
    type: str                 # Order type
    account: str
    timestamp: float
}
```

**Current DBN:** ❌ No equivalent
**Proposed:** New RType for execution reports with fee data

#### 3.2.4 Balance

**Cryptofeed Balance:**
```python
{
    exchange: str
    currency: str
    balance: Decimal
    reserved: Decimal         # Optional, in orders
}
```

**Current DBN:** ❌ No equivalent
**Proposed:** New RType for account balance snapshots

#### 3.2.5 Position

**Cryptofeed Position:**
```python
{
    exchange: str
    symbol: str
    position: Decimal         # Positive=long, negative=short
    entry_price: Decimal
    side: str                 # LONG/SHORT/BOTH
    unrealised_pnl: Decimal   # Optional
    timestamp: float          # Optional
}
```

**Current DBN:** ❌ No equivalent
**Proposed:** New RType for derivative position tracking

#### 3.2.6 Transaction

**Cryptofeed Transaction:**
```python
{
    exchange: str
    currency: str
    type: str                 # DEPOSIT/WITHDRAWAL
    status: str
    amount: Decimal
    timestamp: float
}
```

**Current DBN:** ❌ No equivalent
**Proposed:** New RType for deposit/withdrawal records

### 3.3 Options-Specific Data

#### 3.3.1 Option Summary

**Tardis-Node OptionSummary:**
```typescript
{
    type: 'option_summary'
    optionType: 'call' | 'put'
    strikePrice: number
    expirationDate: Date
    askPrice: number | undefined
    askAmount: number | undefined
    askIv: number | undefined     // Implied volatility
    bidPrice: number | undefined
    bidAmount: number | undefined
    bidIv: number | undefined
    delta: number | undefined     // Greeks
    gamma: number | undefined
    vega: number | undefined
    theta: number | undefined
    rho: number | undefined
    markPrice: number | undefined
    openInterest: number | undefined
    underlyingPrice: number | undefined
    underlyingIndex: string | undefined
}
```

**Current DBN:** ❌ No equivalent
- InstrumentDef has strike_price but no Greeks
- No IV or options-specific metrics

**Proposed:** New RType for options chain with Greeks and IV

---

## 4. Proposed DBN Schema Extensions

### 4.1 RType Assignment Strategy

**Available RType Ranges:**
- 0x00-0x0F: MBP depth levels (used)
- 0x11-0x18: Core types (used)
- 0x20-0x24: OHLCV variants (used)
- 0x30-0x3F: **PROPOSED for crypto extensions**
- 0x40-0x4F: **PROPOSED for authenticated data**
- 0x50-0x5F: **PROPOSED for options data**
- 0xA0: MBO (used)
- 0xB0-0xB1: Consolidated (used)
- 0xC0-0xC4: CBBO variants (used)

### 4.2 Crypto Market Data Extensions (0x30-0x3B)

#### 4.2.1 Ticker (RType 0x30 = 48)

```rust
#[repr(C)]
struct TickerMsg {
    hd: RecordHeader,        // 16 bytes
    bid_price: i64,          // Best bid (1e-9)
    ask_price: i64,          // Best ask (1e-9)
    ts_recv: u64,            // Capture timestamp
    ts_in_delta: i32,        // Delta to exchange time
    sequence: u32,           // Sequence number
    reserved1: i64,          // Future: last_price
    reserved2: i64,          // Future: 24h metrics
}
// Total: 72 bytes
```

#### 4.2.2 Funding (RType 0x31 = 49)

```rust
#[repr(C)]
struct FundingMsg {
    hd: RecordHeader,        // 16 bytes
    mark_price: i64,         // Mark price (1e-9)
    index_price: i64,        // Index price (1e-9)
    funding_rate: i64,       // Current rate (1e-9, can be negative)
    predicted_rate: i64,     // Predicted next rate (1e-9)
    next_funding_time: u64,  // Next funding timestamp (ns)
    ts_recv: u64,            // Capture timestamp
    interval_hours: u8,      // Funding interval (typically 8)
    _padding: [u8; 7],       // Alignment
    reserved1: i64,          // Future use
    reserved2: i64,
}
// Total: 96 bytes
```

#### 4.2.3 Liquidation (RType 0x32 = 50)

```rust
#[repr(C)]
struct LiquidationMsg {
    hd: RecordHeader,        // 16 bytes
    price: i64,              // Liquidation price (1e-9)
    quantity: i64,           // Liquidated amount (1e-9 for fractional)
    side: c_char,            // Position side liquidated (L=Long, S=Short)
    status: c_char,          // Status (F=Filled, P=Partial, C=Cancelled)
    _padding: [u8; 6],       // Alignment
    ts_recv: u64,            // Capture timestamp
    liquidation_id: u64,     // Exchange liquidation ID
    order_id: u64,           // Related order ID
    reserved1: i64,          // Future: liquidation fee
    reserved2: i64,          // Future: insurance fund
}
// Total: 88 bytes
```

#### 4.2.4 IndexPrice (RType 0x33 = 51)

```rust
#[repr(C)]
struct IndexPriceMsg {
    hd: RecordHeader,        // 16 bytes
    price: i64,              // Index value (1e-9)
    ts_recv: u64,            // Capture timestamp
    ts_in_delta: i32,        // Delta to exchange time
    component_count: u16,    // Number of components in index
    _padding: [u8; 2],       // Alignment
    reserved1: i64,          // Future: component breakdown
    reserved2: i64,
    reserved3: i64,
}
// Total: 72 bytes
```

#### 4.2.5 DerivativeTicker (RType 0x34 = 52)

Comprehensive derivative metrics combining funding, OI, and mark prices.

```rust
#[repr(C)]
struct DerivativeTickerMsg {
    hd: RecordHeader,        // 16 bytes
    last_price: i64,         // Last trade price (1e-9)
    mark_price: i64,         // Mark price (1e-9)
    index_price: i64,        // Index price (1e-9)
    funding_rate: i64,       // Current funding rate (1e-9)
    predicted_funding: i64,  // Predicted rate (1e-9)
    next_funding_time: u64,  // Next funding timestamp
    open_interest: u64,      // Total OI in contracts
    ts_recv: u64,            // Capture timestamp
    ts_in_delta: i32,        // Delta to exchange time
    interval_hours: u8,      // Funding interval
    _padding: [u8; 3],       // Alignment
    reserved1: i64,          // Future: 24h volume
    reserved2: i64,          // Future: 24h change
}
// Total: 120 bytes
```

#### 4.2.6 L1Book (RType 0x35 = 53)

Continuous real-time best bid/offer with sizes (not subsampled).

```rust
#[repr(C)]
struct L1BookMsg {
    hd: RecordHeader,        // 16 bytes
    bid_price: i64,          // Best bid (1e-9)
    ask_price: i64,          // Best ask (1e-9)
    bid_size: u32,           // Bid quantity
    ask_size: u32,           // Ask quantity
    ts_recv: u64,            // Capture timestamp
    ts_in_delta: i32,        // Delta to exchange time
    sequence: u32,           // Sequence number
    reserved1: i64,          // Future: bid order count
    reserved2: i64,          // Future: ask order count
}
// Total: 80 bytes
```

### 4.3 Authenticated Data Extensions (0x40-0x45)

#### 4.3.1 OrderInfo (RType 0x40 = 64)

```rust
#[repr(C)]
struct OrderInfoMsg {
    hd: RecordHeader,        // 16 bytes
    order_id: u64,           // Exchange order ID
    client_order_id: u64,    // Client-assigned ID (hash if string)
    price: i64,              // Order price (1e-9)
    amount: i64,             // Order quantity (1e-9)
    filled: i64,             // Filled quantity (1e-9)
    remaining: i64,          // Remaining quantity (1e-9)
    side: c_char,            // B=Buy, S=Sell
    status: c_char,          // O=Open, F=Filled, C=Cancelled, P=Partial
    order_type: c_char,      // L=Limit, M=Market, S=Stop, T=StopLimit
    time_in_force: c_char,   // G=GTC, I=IOC, F=FOK
    _padding: [u8; 4],       // Alignment
    account_id: u64,         // Account identifier
    ts_recv: u64,            // Status update time
    reserved1: i64,          // Future: fee paid
    reserved2: i64,          // Future: cumulative quote qty
}
// Total: 120 bytes
```

#### 4.3.2 OrderPlacement (RType 0x41 = 65)

```rust
#[repr(C)]
struct OrderPlacementMsg {
    hd: RecordHeader,        // 16 bytes
    client_order_id: u64,    // Client-assigned ID
    price: i64,              // Order price (1e-9)
    amount: i64,             // Order quantity (1e-9)
    side: c_char,            // B=Buy, S=Sell
    order_type: c_char,      // L=Limit, M=Market, S=Stop, T=StopLimit
    time_in_force: c_char,   // G=GTC, I=IOC, F=FOK
    post_only: c_char,       // Y=Yes, N=No
    reduce_only: c_char,     // Y=Yes, N=No (derivatives)
    _padding: [u8; 3],       // Alignment
    account_id: u64,         // Account identifier
    stop_price: i64,         // Stop trigger price (1e-9)
    ts_recv: u64,            // Placement time
    reserved1: i64,          // Future: trigger conditions
    reserved2: i64,
}
// Total: 96 bytes
```

#### 4.3.3 Fill (RType 0x42 = 66)

```rust
#[repr(C)]
struct FillMsg {
    hd: RecordHeader,        // 16 bytes
    trade_id: u64,           // Fill/trade ID
    order_id: u64,           // Parent order ID
    price: i64,              // Execution price (1e-9)
    amount: i64,             // Filled quantity (1e-9)
    fee: i64,                // Fee paid (1e-9)
    side: c_char,            // B=Buy, S=Sell
    liquidity: c_char,       // M=Maker, T=Taker
    fee_currency: [c_char; 6], // Fee currency code
    account_id: u64,         // Account identifier
    ts_recv: u64,            // Fill timestamp
    order_type: c_char,      // L=Limit, M=Market
    _padding: [u8; 7],       // Alignment
    reserved1: i64,          // Future: rebate
    reserved2: i64,          // Future: commission breakdown
}
// Total: 104 bytes
```

#### 4.3.4 Balance (RType 0x43 = 67)

```rust
#[repr(C)]
struct BalanceMsg {
    hd: RecordHeader,        // 16 bytes (instrument_id = currency)
    balance: i64,            // Total balance (1e-9)
    available: i64,          // Available balance (1e-9)
    reserved: i64,           // Reserved in orders (1e-9)
    locked: i64,             // Locked/frozen amount (1e-9)
    account_id: u64,         // Account identifier
    ts_recv: u64,            // Balance update time
    currency: [c_char; 12],  // Currency code (e.g., "BTC", "USD")
    reserved1: i64,          // Future: pending deposits
    reserved2: i64,          // Future: pending withdrawals
}
// Total: 96 bytes
```

#### 4.3.5 Position (RType 0x44 = 68)

```rust
#[repr(C)]
struct PositionMsg {
    hd: RecordHeader,        // 16 bytes
    position_size: i64,      // Position qty (1e-9, negative=short)
    entry_price: i64,        // Average entry price (1e-9)
    mark_price: i64,         // Current mark price (1e-9)
    liquidation_price: i64,  // Liquidation price (1e-9)
    unrealized_pnl: i64,     // Unrealized P&L (1e-9)
    realized_pnl: i64,       // Realized P&L (1e-9)
    margin: i64,             // Position margin (1e-9)
    side: c_char,            // L=Long, S=Short, B=Both(hedge mode)
    margin_mode: c_char,     // C=Cross, I=Isolated
    _padding: [u8; 6],       // Alignment
    account_id: u64,         // Account identifier
    ts_recv: u64,            // Position update time
    leverage: u16,           // Leverage multiplier (e.g., 10 = 10x)
    _padding2: [u8; 6],      // Alignment
    reserved1: i64,          // Future: funding fees paid
    reserved2: i64,          // Future: initial margin
}
// Total: 128 bytes
```

#### 4.3.6 Transaction (RType 0x45 = 69)

```rust
#[repr(C)]
struct TransactionMsg {
    hd: RecordHeader,        // 16 bytes (instrument_id = currency)
    transaction_id: u64,     // Exchange transaction ID
    amount: i64,             // Transaction amount (1e-9)
    fee: i64,                // Transaction fee (1e-9)
    tx_type: c_char,         // D=Deposit, W=Withdrawal
    status: c_char,          // P=Pending, C=Confirmed, F=Failed
    _padding: [u8; 6],       // Alignment
    account_id: u64,         // Account identifier
    ts_recv: u64,            // Transaction time
    currency: [c_char; 12],  // Currency code
    address: [c_char; 64],   // Blockchain address (or bank info hash)
    tx_hash: [c_char; 72],   // Transaction hash (blockchain)
    reserved1: i64,          // Future: confirmations
    reserved2: i64,          // Future: network fee
}
// Total: 224 bytes
```

### 4.4 Options Data Extensions (0x50)

#### 4.4.1 OptionSummary (RType 0x50 = 80)

```rust
#[repr(C)]
struct OptionSummaryMsg {
    hd: RecordHeader,        // 16 bytes
    strike_price: i64,       // Strike price (1e-9)
    underlying_price: i64,   // Current underlying price (1e-9)
    mark_price: i64,         // Mark price (1e-9)
    bid_price: i64,          // Best bid (1e-9)
    ask_price: i64,          // Best ask (1e-9)
    bid_size: u32,           // Bid quantity
    ask_size: u32,           // Ask quantity
    bid_iv: i32,             // Bid implied vol (1e-9, as fraction)
    ask_iv: i32,             // Ask implied vol (1e-9)
    delta: i32,              // Delta Greek (1e-9, -1 to 1)
    gamma: i32,              // Gamma Greek (1e-9)
    vega: i32,               // Vega Greek (1e-9)
    theta: i32,              // Theta Greek (1e-9)
    rho: i32,                // Rho Greek (1e-9)
    open_interest: u32,      // Total OI
    volume: u32,             // 24h volume
    expiration_date: u64,    // Expiration timestamp (ns)
    option_type: c_char,     // C=Call, P=Put
    _padding: [u8; 7],       // Alignment
    ts_recv: u64,            // Update timestamp
    underlying_id: u32,      // Underlying instrument ID
    _padding2: [u8; 4],      // Alignment
    reserved1: i64,          // Future: vanna
    reserved2: i64,          // Future: volga
}
// Total: 152 bytes
```

---

## 5. Implementation Specification

### 5.1 Type Conversion Rules

#### 5.1.1 Numeric Precision

**Price Conversion (Decimal/float → i64):**
```python
def encode_price(price: Decimal) -> int:
    """Convert Decimal price to DBN i64 (1e-9 scale)"""
    return int(price * 1_000_000_000)

def decode_price(price_i64: int) -> Decimal:
    """Convert DBN i64 to Decimal price"""
    return Decimal(price_i64) / Decimal(1_000_000_000)
```

**Quantity Conversion:**
```python
def encode_quantity(qty: Decimal) -> int:
    """For fractional quantities, use i64 with 1e-9 scale"""
    return int(qty * 1_000_000_000)

def encode_integer_quantity(qty: Decimal) -> int:
    """For integer quantities, use u32/u64 directly"""
    return int(qty)
```

**Timestamp Conversion:**
```python
def encode_timestamp(ts: float) -> int:
    """Convert Unix seconds to nanoseconds"""
    return int(ts * 1_000_000_000)

def encode_datetime(dt: datetime) -> int:
    """Convert datetime to nanoseconds since epoch"""
    return int(dt.timestamp() * 1_000_000_000)
```

#### 5.1.2 Side Mapping

```python
SIDE_MAPPING = {
    # Cryptofeed → DBN
    'BUY': b'B',
    'SELL': b'A',

    # Tardis-node → DBN
    'buy': b'B',
    'sell': b'A',
    'unknown': b'N',

    # Position sides
    'LONG': b'L',
    'SHORT': b'S',
    'BOTH': b'B',
}
```

#### 5.1.3 Status/Action Codes

```python
ORDER_STATUS_MAPPING = {
    'OPEN': b'O',
    'FILLED': b'F',
    'CANCELLED': b'C',
    'PARTIAL': b'P',
    'PENDING': b'P',
    'EXPIRED': b'E',
    'FAILED': b'X',
}

ORDER_TYPE_MAPPING = {
    'LIMIT': b'L',
    'MARKET': b'M',
    'STOP_LIMIT': b'S',
    'STOP_MARKET': b'T',
}

LIQUIDITY_MAPPING = {
    'MAKER': b'M',
    'TAKER': b'T',
}
```

### 5.2 Symbol Mapping Strategy

#### 5.2.1 Symbol Normalization

**Cryptofeed Symbols → DBN instrument_id:**
```python
def normalize_symbol(cf_symbol: str, exchange: str) -> tuple[u32, str]:
    """
    Convert cryptofeed symbol to DBN instrument_id and raw_symbol

    Examples:
        'BTC-USD' → (100001, 'BTCUSD')
        'BTC-USD-PERP' → (100002, 'BTC-PERP')
        'ETH-USDT-25Z' → (100003, 'ETHZ25')
    """
    # 1. Parse symbol type
    parts = cf_symbol.split('-')
    base = parts[0]
    quote = parts[1] if len(parts) > 1 else 'USD'

    # 2. Determine symbol type
    if len(parts) == 2:
        # Spot
        symbol_type = 'SPOT'
    elif len(parts) == 3 and parts[2] == 'PERP':
        # Perpetual
        symbol_type = 'PERP'
    elif len(parts) == 3:
        # Futures with expiry
        symbol_type = 'FUT'
    else:
        symbol_type = 'UNKNOWN'

    # 3. Generate instrument_id (hash or database lookup)
    instrument_id = generate_instrument_id(cf_symbol, exchange)

    # 4. Convert to exchange raw symbol
    raw_symbol = symbol_to_exchange_format(cf_symbol, exchange)

    return (instrument_id, raw_symbol)
```

#### 5.2.2 Instrument Definition Generation

For new crypto types, generate InstrumentDef records:

```python
def create_instrument_def(
    symbol: str,
    exchange: str,
    instrument_id: int,
    symbol_type: str
) -> InstrumentDefMsg:
    """Create DBN InstrumentDef for crypto symbols"""
    return InstrumentDefMsg(
        hd=RecordHeader(
            rtype=19,
            publisher_id=get_publisher_id(exchange),
            instrument_id=instrument_id,
            ts_event=current_timestamp_ns()
        ),
        raw_symbol=symbol.encode(),
        asset=extract_base(symbol).encode(),
        security_type=symbol_type.encode(),  # 'SPOT', 'PERP', 'FUT'
        exchange=exchange.encode(),
        currency=extract_quote(symbol).encode(),
        # ... other fields
    )
```

### 5.3 Encoding Pipeline

#### 5.3.1 Cryptofeed → DBN Conversion

```python
class CryptofeedToDBN:
    def __init__(self, exchange: str, publisher_id: int):
        self.exchange = exchange
        self.publisher_id = publisher_id
        self.symbol_map = SymbolMapping()

    def convert_trade(self, trade: Trade) -> TradeMsg:
        """Convert cryptofeed Trade to DBN TradeMsg"""
        instrument_id = self.symbol_map.get_or_create(trade.symbol, self.exchange)

        return TradeMsg(
            hd=RecordHeader(
                rtype=0,
                publisher_id=self.publisher_id,
                instrument_id=instrument_id,
                ts_event=encode_timestamp(trade.timestamp)
            ),
            price=encode_price(trade.price),
            size=encode_integer_quantity(trade.amount),
            action=b'T',
            side=SIDE_MAPPING[trade.side],
            flags=0,
            depth=0,
            ts_recv=encode_timestamp(trade.timestamp),  # Use same if no receipt time
            ts_in_delta=0,
            sequence=int(trade.id) if trade.id and trade.id.isdigit() else 0
        )

    def convert_funding(self, funding: Funding) -> FundingMsg:
        """Convert cryptofeed Funding to extended DBN FundingMsg"""
        instrument_id = self.symbol_map.get_or_create(funding.symbol, self.exchange)

        return FundingMsg(
            hd=RecordHeader(
                rtype=0x31,  # New funding type
                publisher_id=self.publisher_id,
                instrument_id=instrument_id,
                ts_event=encode_timestamp(funding.timestamp)
            ),
            mark_price=encode_price(funding.mark_price) if funding.mark_price else UNDEF_PRICE,
            index_price=UNDEF_PRICE,  # Not in cryptofeed Funding
            funding_rate=encode_price(funding.rate) if funding.rate else UNDEF_PRICE,
            predicted_rate=encode_price(funding.predicted_rate) if funding.predicted_rate else UNDEF_PRICE,
            next_funding_time=encode_timestamp(funding.next_funding_time) if funding.next_funding_time else 0,
            ts_recv=encode_timestamp(funding.timestamp),
            interval_hours=8,  # Default, exchange-specific
            _padding=[0] * 7,
            reserved1=0,
            reserved2=0
        )

    def convert_liquidation(self, liq: Liquidation) -> LiquidationMsg:
        """Convert cryptofeed Liquidation to extended DBN LiquidationMsg"""
        instrument_id = self.symbol_map.get_or_create(liq.symbol, self.exchange)

        # Map position side to liquidation side
        side_map = {'LONG': b'L', 'SHORT': b'S'}

        return LiquidationMsg(
            hd=RecordHeader(
                rtype=0x32,  # New liquidation type
                publisher_id=self.publisher_id,
                instrument_id=instrument_id,
                ts_event=encode_timestamp(liq.timestamp) if liq.timestamp else 0
            ),
            price=encode_price(liq.price),
            quantity=encode_quantity(liq.quantity),
            side=side_map.get(liq.side, b'N'),
            status=b'F' if liq.status == 'FILLED' else b'P',
            _padding=[0] * 6,
            ts_recv=encode_timestamp(liq.timestamp) if liq.timestamp else 0,
            liquidation_id=hash(liq.id) if liq.id else 0,
            order_id=0,
            reserved1=0,
            reserved2=0
        )
```

#### 5.3.2 Tardis-Node → DBN Conversion

```python
class TardisToDBN:
    def __init__(self, exchange: str, publisher_id: int):
        self.exchange = exchange
        self.publisher_id = publisher_id
        self.symbol_map = SymbolMapping()

    def convert_trade(self, trade: Trade) -> TradeMsg:
        """Convert tardis-node Trade to DBN TradeMsg"""
        instrument_id = self.symbol_map.get_or_create(trade['symbol'], self.exchange)

        return TradeMsg(
            hd=RecordHeader(
                rtype=0,
                publisher_id=self.publisher_id,
                instrument_id=instrument_id,
                ts_event=encode_datetime(trade['timestamp'])
            ),
            price=encode_price(Decimal(str(trade['price']))),
            size=encode_integer_quantity(Decimal(str(trade['amount']))),
            action=b'T',
            side=SIDE_MAPPING[trade['side']],
            flags=0,
            depth=0,
            ts_recv=encode_datetime(trade['localTimestamp']),
            ts_in_delta=calculate_delta(trade['timestamp'], trade['localTimestamp']),
            sequence=int(trade['id']) if trade.get('id') and trade['id'].isdigit() else 0
        )

    def convert_derivative_ticker(self, ticker: DerivativeTicker) -> DerivativeTickerMsg:
        """Convert tardis-node DerivativeTicker to extended DBN DerivativeTickerMsg"""
        instrument_id = self.symbol_map.get_or_create(ticker['symbol'], self.exchange)

        return DerivativeTickerMsg(
            hd=RecordHeader(
                rtype=0x34,  # New derivative ticker type
                publisher_id=self.publisher_id,
                instrument_id=instrument_id,
                ts_event=encode_datetime(ticker['timestamp'])
            ),
            last_price=encode_price(ticker.get('lastPrice')) if ticker.get('lastPrice') else UNDEF_PRICE,
            mark_price=encode_price(ticker.get('markPrice')) if ticker.get('markPrice') else UNDEF_PRICE,
            index_price=encode_price(ticker.get('indexPrice')) if ticker.get('indexPrice') else UNDEF_PRICE,
            funding_rate=encode_price(ticker.get('fundingRate')) if ticker.get('fundingRate') else UNDEF_PRICE,
            predicted_funding=encode_price(ticker.get('predictedFundingRate')) if ticker.get('predictedFundingRate') else UNDEF_PRICE,
            next_funding_time=encode_datetime(ticker.get('fundingTimestamp')) if ticker.get('fundingTimestamp') else 0,
            open_interest=int(ticker.get('openInterest', 0)),
            ts_recv=encode_datetime(ticker['localTimestamp']),
            ts_in_delta=calculate_delta(ticker['timestamp'], ticker['localTimestamp']),
            interval_hours=8,  # Exchange-specific
            _padding=[0] * 3,
            reserved1=0,
            reserved2=0
        )

    def convert_option_summary(self, opt: OptionSummary) -> OptionSummaryMsg:
        """Convert tardis-node OptionSummary to extended DBN OptionSummaryMsg"""
        instrument_id = self.symbol_map.get_or_create(opt['symbol'], self.exchange)

        return OptionSummaryMsg(
            hd=RecordHeader(
                rtype=0x50,  # New option summary type
                publisher_id=self.publisher_id,
                instrument_id=instrument_id,
                ts_event=encode_datetime(opt['timestamp'])
            ),
            strike_price=encode_price(opt['strikePrice']),
            underlying_price=encode_price(opt.get('underlyingPrice')) if opt.get('underlyingPrice') else UNDEF_PRICE,
            mark_price=encode_price(opt.get('markPrice')) if opt.get('markPrice') else UNDEF_PRICE,
            bid_price=encode_price(opt.get('bidPrice')) if opt.get('bidPrice') else UNDEF_PRICE,
            ask_price=encode_price(opt.get('askPrice')) if opt.get('askPrice') else UNDEF_PRICE,
            bid_size=int(opt.get('bidAmount', 0)),
            ask_size=int(opt.get('askAmount', 0)),
            bid_iv=encode_price(opt.get('bidIv')) if opt.get('bidIv') else UNDEF_PRICE,
            ask_iv=encode_price(opt.get('askIv')) if opt.get('askIv') else UNDEF_PRICE,
            delta=encode_price(opt.get('delta')) if opt.get('delta') else UNDEF_PRICE,
            gamma=encode_price(opt.get('gamma')) if opt.get('gamma') else UNDEF_PRICE,
            vega=encode_price(opt.get('vega')) if opt.get('vega') else UNDEF_PRICE,
            theta=encode_price(opt.get('theta')) if opt.get('theta') else UNDEF_PRICE,
            rho=encode_price(opt.get('rho')) if opt.get('rho') else UNDEF_PRICE,
            open_interest=int(opt.get('openInterest', 0)),
            volume=0,  # Not in tardis-node OptionSummary
            expiration_date=encode_datetime(opt['expirationDate']),
            option_type=b'C' if opt['optionType'] == 'call' else b'P',
            _padding=[0] * 7,
            ts_recv=encode_datetime(opt['localTimestamp']),
            underlying_id=0,  # Would need lookup
            _padding2=[0] * 4,
            reserved1=0,
            reserved2=0
        )
```

### 5.4 Decoding Pipeline

```python
class DBNDecoder:
    def decode_record(self, record_ref: RecordRef) -> dict:
        """Decode DBN record to Python dict"""
        rtype = record_ref.rtype()

        if rtype == 0:
            return self.decode_trade(record_ref.as_trade())
        elif rtype == 0x31:
            return self.decode_funding(record_ref.as_funding())
        elif rtype == 0x32:
            return self.decode_liquidation(record_ref.as_liquidation())
        elif rtype == 0x34:
            return self.decode_derivative_ticker(record_ref.as_derivative_ticker())
        elif rtype == 0x40:
            return self.decode_order_info(record_ref.as_order_info())
        # ... other types

    def decode_funding(self, msg: FundingMsg) -> dict:
        """Decode FundingMsg to cryptofeed-compatible dict"""
        return {
            'exchange': get_exchange_name(msg.hd.publisher_id),
            'symbol': self.symbol_map.get_symbol(msg.hd.instrument_id),
            'mark_price': decode_price(msg.mark_price) if msg.mark_price != UNDEF_PRICE else None,
            'rate': decode_price(msg.funding_rate) if msg.funding_rate != UNDEF_PRICE else None,
            'next_funding_time': decode_timestamp(msg.next_funding_time) if msg.next_funding_time > 0 else None,
            'predicted_rate': decode_price(msg.predicted_rate) if msg.predicted_rate != UNDEF_PRICE else None,
            'timestamp': decode_timestamp(msg.hd.ts_event),
        }
```

---

## 6. Storage and Performance Considerations

### 6.1 Record Size Analysis

| Record Type | Size (bytes) | Notes |
|-------------|--------------|-------|
| TradeMsg | 64 | Existing DBN |
| Mbp10Msg | 344 | Existing DBN |
| OhlcvMsg | 48 | Existing DBN |
| **TickerMsg** | 72 | **New** |
| **FundingMsg** | 96 | **New** |
| **LiquidationMsg** | 88 | **New** |
| **IndexPriceMsg** | 72 | **New** |
| **DerivativeTickerMsg** | 120 | **New** |
| **L1BookMsg** | 80 | **New** |
| **OrderInfoMsg** | 120 | **New** |
| **OrderPlacementMsg** | 96 | **New** |
| **FillMsg** | 104 | **New** |
| **BalanceMsg** | 96 | **New** |
| **PositionMsg** | 128 | **New** |
| **TransactionMsg** | 224 | **New** |
| **OptionSummaryMsg** | 152 | **New** |

### 6.2 Compression Estimates

Based on DBN typical compression ratios (5-10x with Zstandard):

**Example: 1 Million Messages**

| Type | Uncompressed | Compressed (7x) |
|------|--------------|-----------------|
| Trades | 64 MB | 9.1 MB |
| Funding | 96 MB | 13.7 MB |
| Liquidations | 88 MB | 12.6 MB |
| Order Info | 120 MB | 17.1 MB |
| Positions | 128 MB | 18.3 MB |

**Daily Storage Example (High-Frequency Exchange):**
- Trades: 10M/day × 64 bytes = 640 MB → 91 MB compressed
- Funding: 100K/day × 96 bytes = 9.6 MB → 1.4 MB compressed
- Liquidations: 50K/day × 88 bytes = 4.4 MB → 0.6 MB compressed
- Order Info: 5M/day × 120 bytes = 600 MB → 86 MB compressed

**Total: ~1.25 GB uncompressed → ~180 MB compressed per day**

### 6.3 Performance Projections

**Decoding Speed:**
- DBN baseline: 1-10 GB/s
- New types: Similar fixed-width structure
- Expected: 2-5 GB/s for crypto extensions
- Bottleneck: Price conversion (i64 → Decimal)

**Encoding Speed:**
- Price conversion: ~5M conversions/second
- Struct packing: ~10M records/second
- Expected throughput: 3-8M messages/second

---

## 7. Implementation Roadmap

### 7.1 Phase 1: Core Market Data (Weeks 1-2)

**Implement:**
- ✅ Ticker (RType 0x30)
- ✅ Funding (RType 0x31)
- ✅ Liquidation (RType 0x32)
- ✅ IndexPrice (RType 0x33)
- ✅ DerivativeTicker (RType 0x34)
- ✅ L1Book (RType 0x35)

**Deliverables:**
- Rust struct definitions
- Encoding/decoding functions
- Unit tests for each type
- Integration tests with cryptofeed/tardis-node data

### 7.2 Phase 2: Authenticated Data (Weeks 3-4)

**Implement:**
- ✅ OrderInfo (RType 0x40)
- ✅ OrderPlacement (RType 0x41)
- ✅ Fill (RType 0x42)
- ✅ Balance (RType 0x43)
- ✅ Position (RType 0x44)
- ✅ Transaction (RType 0x45)

**Deliverables:**
- Rust struct definitions
- Privacy/security considerations
- Encryption support (optional)
- Integration with authenticated feeds

### 7.3 Phase 3: Options Data (Week 5)

**Implement:**
- ✅ OptionSummary (RType 0x50)

**Deliverables:**
- Options-specific encoding
- Greeks precision testing
- Integration with Deribit/OKX options data

### 7.4 Phase 4: Conversion Libraries (Weeks 6-7)

**Implement:**
- Cryptofeed → DBN converter
- Tardis-Node → DBN converter
- DBN → Cryptofeed converter
- DBN → Tardis-Node converter

**Deliverables:**
- Python library: `cryptofeed-dbn`
- TypeScript library: `tardis-dbn`
- CLI tools for batch conversion
- Performance benchmarks

### 7.5 Phase 5: Validation & Documentation (Week 8)

**Implement:**
- End-to-end validation
- Performance testing
- Compression benchmarks
- Documentation

**Deliverables:**
- Complete API documentation
- Usage examples
- Performance report
- Schema specification document

---

## 8. Test Cases and Validation

### 8.1 Round-Trip Conversion Tests

```python
def test_trade_round_trip():
    """Test cryptofeed Trade → DBN → cryptofeed"""
    # Original
    cf_trade = Trade(
        exchange='BINANCE',
        symbol='BTC-USD',
        side='BUY',
        amount=Decimal('1.5'),
        price=Decimal('50000.00'),
        timestamp=1697472000.123456
    )

    # Convert to DBN
    dbn_trade = converter.convert_trade(cf_trade)

    # Convert back
    cf_trade_decoded = decoder.decode_trade(dbn_trade)

    # Assert equality
    assert cf_trade_decoded['symbol'] == cf_trade.symbol
    assert cf_trade_decoded['side'] == cf_trade.side
    assert abs(cf_trade_decoded['price'] - cf_trade.price) < Decimal('0.000000001')
    assert abs(cf_trade_decoded['amount'] - cf_trade.amount) < Decimal('0.000000001')

def test_funding_round_trip():
    """Test cryptofeed Funding → DBN → cryptofeed"""
    cf_funding = Funding(
        exchange='BINANCE',
        symbol='BTC-USD-PERP',
        mark_price=Decimal('50000.00'),
        rate=Decimal('0.0001'),
        predicted_rate=Decimal('0.00015'),
        next_funding_time=1697472000.0,
        timestamp=1697471900.0
    )

    dbn_funding = converter.convert_funding(cf_funding)
    cf_funding_decoded = decoder.decode_funding(dbn_funding)

    assert cf_funding_decoded['symbol'] == cf_funding.symbol
    assert abs(cf_funding_decoded['rate'] - cf_funding.rate) < Decimal('0.0000000001')
    assert abs(cf_funding_decoded['mark_price'] - cf_funding.mark_price) < Decimal('0.000000001')
```

### 8.2 Precision Tests

```python
def test_price_precision():
    """Test 9 decimal places precision preservation"""
    test_prices = [
        Decimal('0.000000001'),  # Min precision
        Decimal('50000.123456789'),  # Max precision
        Decimal('99999999.999999999'),  # Large with precision
    ]

    for price in test_prices:
        encoded = encode_price(price)
        decoded = decode_price(encoded)
        assert abs(decoded - price) < Decimal('0.0000000001')

def test_quantity_precision():
    """Test fractional quantity precision"""
    test_quantities = [
        Decimal('0.00000001'),  # Satoshi
        Decimal('1.23456789'),
        Decimal('1000000.123456789'),
    ]

    for qty in test_quantities:
        encoded = encode_quantity(qty)
        decoded = decode_quantity(encoded)
        assert abs(decoded - qty) < Decimal('0.0000000001')
```

### 8.3 Performance Benchmarks

```python
def benchmark_encoding(num_records=1_000_000):
    """Benchmark encoding speed"""
    trades = generate_test_trades(num_records)

    start = time.perf_counter()
    dbn_records = [converter.convert_trade(t) for t in trades]
    elapsed = time.perf_counter() - start

    throughput = num_records / elapsed
    print(f"Encoding: {throughput:,.0f} records/sec")
    assert throughput > 500_000  # Min 500K records/sec

def benchmark_decoding(num_records=1_000_000):
    """Benchmark decoding speed"""
    dbn_records = generate_test_dbn_records(num_records)

    start = time.perf_counter()
    decoded = [decoder.decode_record(r) for r in dbn_records]
    elapsed = time.perf_counter() - start

    throughput = num_records / elapsed
    print(f"Decoding: {throughput:,.0f} records/sec")
    assert throughput > 500_000

def benchmark_compression():
    """Benchmark Zstandard compression ratios"""
    data_types = ['trade', 'funding', 'liquidation', 'order_info']

    for dtype in data_types:
        records = generate_test_records(dtype, 100_000)
        uncompressed = serialize_records(records)
        compressed = zstd.compress(uncompressed)

        ratio = len(uncompressed) / len(compressed)
        print(f"{dtype}: {ratio:.2f}x compression")
        assert ratio >= 5.0  # Min 5x compression
```

### 8.4 Integration Tests

```python
def test_cryptofeed_integration():
    """Test live cryptofeed → DBN conversion"""
    async def trade_callback(trade, receipt_timestamp):
        dbn_trade = converter.convert_trade(trade)
        writer.write_record(dbn_trade)

    # Connect to live feed
    fh = FeedHandler()
    fh.add_feed(
        Binance(
            channels=[TRADES],
            symbols=['BTC-USDT'],
            callbacks={TRADES: trade_callback}
        )
    )

    # Run for 10 seconds
    await asyncio.wait_for(fh.run(), timeout=10.0)

    # Verify DBN file created
    assert writer.record_count > 0

    # Verify round-trip
    decoder = DBNDecoder(writer.filename)
    for record in decoder:
        assert record['exchange'] == 'BINANCE'
        assert record['symbol'] in ['BTC-USDT', 'BTCUSDT']

def test_tardis_integration():
    """Test tardis-node → DBN conversion"""
    messages = replay({
        'exchange': 'binance',
        'from': '2025-01-01',
        'to': '2025-01-02',
        'filters': [{'channel': 'trade', 'symbols': ['BTCUSDT']}]
    })

    writer = DBNWriter('output.dbn')
    count = 0

    for msg in messages:
        if msg['type'] == 'trade':
            dbn_trade = converter.convert_trade(msg)
            writer.write_record(dbn_trade)
            count += 1

    assert count > 0
    writer.close()
```

---

## 9. Migration Strategy

### 9.1 Existing Data Migration

**For users with existing cryptofeed/tardis-node data:**

1. **Historical Conversion:**
```bash
# Convert cryptofeed Redis/MongoDB data to DBN
cryptofeed-to-dbn --source redis --key trades:BINANCE:BTC-USDT \
                  --output trades-btc-usdt.dbn.zst \
                  --compress zstd

# Convert tardis-node CSV to DBN
tardis-to-dbn --input trades-2025-01-01.csv \
              --exchange binance \
              --output trades-2025-01-01.dbn.zst
```

2. **Real-Time Bridge:**
```python
# Cryptofeed → DBN real-time
async def realtime_to_dbn(trade, receipt_timestamp):
    dbn_trade = converter.convert_trade(trade)
    dbn_writer.write_record(dbn_trade)
    dbn_writer.flush()  # For low-latency

fh.add_feed(
    Binance(
        channels=[TRADES, FUNDING, LIQUIDATIONS],
        symbols=['BTC-USDT'],
        callbacks={
            TRADES: realtime_to_dbn,
            FUNDING: realtime_funding_to_dbn,
            LIQUIDATIONS: realtime_liquidation_to_dbn
        }
    )
)
```

### 9.2 Backward Compatibility

**DBN Format Version:**
- Propose as DBN v3 with crypto extensions
- Maintain v2 compatibility where possible
- Version field in metadata indicates extension support

**Decoder Compatibility:**
```rust
match msg.hd.rtype {
    0 => handle_trade(msg),
    // Standard DBN types...
    0x30 => {
        if version >= 3 {
            handle_ticker(msg)
        } else {
            return Err("Unsupported type for DBN v2")
        }
    }
    0x31 => handle_funding(msg),  // DBN v3+
    // ...
}
```

---

## 10. Summary and Recommendations

### 10.1 Key Findings

1. **Strong Foundation:** DBN's fixed-width binary format is excellent for market data
2. **Coverage Gap:** 55% of crypto-specific data types not currently supported
3. **Extensibility:** DBN's design allows clean addition of new record types
4. **Performance:** Expected to maintain DBN's high-performance characteristics

### 10.2 Recommended Extensions

**Priority 1 (Critical for crypto market data):**
- ✅ Funding (RType 0x31)
- ✅ Liquidation (RType 0x32)
- ✅ DerivativeTicker (RType 0x34)
- ✅ L1Book (RType 0x35)

**Priority 2 (Authenticated trading data):**
- ✅ OrderInfo (RType 0x40)
- ✅ Fill (RType 0x42)
- ✅ Position (RType 0x44)

**Priority 3 (Additional types):**
- ✅ Ticker (RType 0x30)
- ✅ IndexPrice (RType 0x33)
- ✅ OptionSummary (RType 0x50)
- ✅ Balance, OrderPlacement, Transaction

### 10.3 Implementation Approach

1. **Start with Rust:** Implement new record types in `dbn` crate
2. **Python Bindings:** Extend `databento-dbn` with PyO3 bindings
3. **Conversion Libraries:** Create `cryptofeed-dbn` and `tardis-dbn` packages
4. **Documentation:** Complete specification and usage guides
5. **Community Feedback:** Iterate based on real-world usage

### 10.4 Benefits

**For Cryptofeed Users:**
- High-performance binary storage (5-10x compression)
- Unified format across exchanges
- Nanosecond precision timestamps
- Zero-copy decoding potential

**For Tardis-Node Users:**
- Reduced storage costs vs CSV
- Faster processing than JSON
- Native Rust/Python integration
- Consistent schema across exchanges

**For DBN Ecosystem:**
- Expanded to crypto markets (56+ exchanges)
- Support for modern derivative types
- Authenticated data capability
- Options market support

---

## References

- [[202510160000-cryptofeed-data-types-research|Cryptofeed Data Types Research]]
- [[20251016-tardis-node-comprehensive-research|Tardis-Node Comprehensive Research]]
- [[20251016-databento-dbn-schema-research|DBN Schema Research]]
- Databento DBN Format: https://databento.com/docs/standards-and-conventions/databento-binary-encoding
- Cryptofeed GitHub: https://github.com/bmoscon/cryptofeed
- Tardis-Dev GitHub: https://github.com/tardis-dev/tardis-node

---

**Document Status:** Draft specification for review
**Next Steps:**
1. Review with Databento team for official RType assignment
2. Implement Phase 1 (Core Market Data) in Rust
3. Create conversion libraries for cryptofeed and tardis-node
4. Performance testing and benchmarking
5. Community feedback and iteration

**Created:** 2025-10-16
**Version:** 1.0
**Authors:** Research synthesis based on cryptofeed, tardis-node, and DBN documentation
