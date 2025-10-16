---
date: 2025-10-16
type: research
tags: [cryptofeed, cryptocurrency, market-data, python, data-types, schema]
status: complete
source: github-bmoscon-cryptofeed
confidence: high
---

# Cryptofeed Python Library - Complete Data Types Research

## Executive Summary

Cryptofeed is a Python library that provides normalized, standardized access to cryptocurrency market data from 43+ exchanges. It handles real-time WebSocket feeds and REST APIs, converting exchange-specific formats into consistent Python data structures using Decimal precision for financial accuracy.

**Key Features:**
- 43+ exchange integrations (Binance, Coinbase, Kraken, Deribit, OKX, etc.)
- 15+ standardized data types covering market data and authenticated channels
- Cython-optimized performance with object pooling (`@cython.freelist`)
- Decimal precision for all financial values
- Bidirectional symbol normalization across exchanges
- Flexible backend support (Redis, MongoDB, Kafka, PostgreSQL, InfluxDB)

## Complete Data Type Catalog

### 1. Trade
**Purpose:** Individual trade executions
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Trading pair in normalized format
- `side` (str): BUY or SELL
- `amount` (Decimal): Trade quantity
- `price` (Decimal): Execution price
- `timestamp` (double): Unix timestamp in seconds
- `id` (str, optional): Exchange-specific trade ID
- `type` (str, optional): Trade type classification
- `raw` (dict/list, optional): Original exchange data

**Performance:** Uses `@cython.freelist(128)` for object pooling
**Methods:** `from_dict()`, `to_dict()`, `__eq__()`, `__hash__()`

### 2. Ticker
**Purpose:** Current market quotes (Level 1 data)
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Trading pair
- `bid` (Decimal): Best bid price
- `ask` (Decimal): Best ask price
- `timestamp` (float, optional): Unix timestamp
- `raw` (dict/list, optional): Original data

**Use Case:** Real-time spread monitoring, price alerts
**Methods:** `from_dict()`, `to_dict()`, `__eq__()`, `__hash__()`

### 3. L1Book
**Purpose:** Single best bid/ask level
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Trading pair
- `bid_price` (Decimal): Best bid price
- `bid_size` (Decimal): Size at best bid
- `ask_price` (Decimal): Best ask price
- `ask_size` (Decimal): Size at best ask
- `timestamp` (double): Unix timestamp

**Difference from Ticker:** L1Book includes sizes, Ticker only prices

### 4. OrderBook (L2/L3 Books)
**Purpose:** Full order book depth with delta tracking
**Fields:**
- `exchange` (str, readonly): Exchange identifier
- `symbol` (str, readonly): Trading pair
- `book` (object, readonly): Internal `_OrderBook` instance
- `delta` (dict, public): Contains BID/ASK price-size tuples for updates
- `sequence_number` (object, public): Message sequence tracking
- `checksum` (object, public): Data integrity validation
- `timestamp` (object, public): Update timestamp
- `raw` (object, public): Original exchange data

**Book Structure:**
```python
book.book.bids  # SortedDict: {price: size, ...}
book.book.asks  # SortedDict: {price: size, ...}
book.book.bids.index(0)[0]  # Best bid price
book.book.asks.index(0)[0]  # Best ask price
```

**Delta Tracking:**
```python
delta = {
    BID: [(price1, size1), (price2, size2), ...],
    ASK: [(price1, size1), (price2, size2), ...]
}
# size == 0 indicates level removal
```

**L2 vs L3:**
- **L2Book:** Price-aggregated (multiple orders at same price)
- **L3Book:** Order-level data (individual order IDs)

### 5. Candle
**Purpose:** OHLCV candlestick data
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Trading pair
- `start` (double): Candle start timestamp
- `stop` (double): Candle end timestamp
- `interval` (str): Time interval ("1m", "5m", "1h", "1d", etc.)
- `trades` (int, optional): Number of trades in candle
- `open` (Decimal): Opening price
- `high` (Decimal): Highest price
- `low` (Decimal): Lowest price
- `close` (Decimal): Closing price
- `volume` (Decimal): Total volume
- `closed` (bool): Whether candle is finalized
- `timestamp` (float, optional): Update timestamp
- `raw` (dict/list, optional): Original data

**Methods:** `from_dict()`, `to_dict()`, `__eq__()`, `__hash__()`
**Use Case:** Technical analysis, charting, backtesting

### 6. Funding
**Purpose:** Perpetual contract funding rates
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Contract symbol
- `mark_price` (Decimal, optional): Mark price reference
- `rate` (Decimal, optional): Current funding rate
- `next_funding_time` (float, optional): Next funding timestamp
- `predicted_rate` (Decimal, optional): Predicted next rate
- `timestamp` (double): Update timestamp
- `raw` (dict, optional): Original data

**Methods:** `from_dict()`, `to_dict()`, `__eq__()`, `__hash__()`
**Use Case:** Perpetual swap trading, arbitrage strategies

### 7. OpenInterest
**Purpose:** Total outstanding derivative contracts
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Contract symbol
- `open_interest` (Decimal): Total open contracts
- `timestamp` (double): Update timestamp
- `raw` (dict, optional): Original data

**Methods:** `from_dict()`, `to_dict()`, `__eq__()`, `__hash__()`
**Use Case:** Market sentiment, leverage monitoring

### 8. Liquidation
**Purpose:** Forced position closures
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Contract symbol
- `side` (str): LONG or SHORT position liquidated
- `quantity` (Decimal): Liquidated amount
- `price` (Decimal): Liquidation price
- `id` (str): Liquidation identifier
- `status` (str): Liquidation status
- `timestamp` (float, optional): Event timestamp
- `raw` (dict, optional): Original data

**Methods:** `from_dict()`, `to_dict()`, `__eq__()`, `__hash__()`
**Use Case:** Risk management, market volatility analysis

### 9. Index
**Purpose:** Index price data
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Index symbol
- `price` (Decimal): Index value
- `timestamp` (double): Update timestamp
- `raw` (dict): Original data

**Methods:** `to_dict()`, `__eq__()`, `__hash__()`
**Use Case:** Derivatives pricing, reference rates

### 10. OrderInfo
**Purpose:** Order status and details
**Fields:**
- `exchange` (str, readonly): Exchange identifier
- `symbol` (str, readonly): Trading pair
- `id` (str, readonly): Exchange order ID
- `client_order_id` (str, readonly): Client-specified ID
- `side` (str, readonly): BUY or SELL
- `status` (str, readonly): Order status (OPEN, FILLED, CANCELLED, etc.)
- `type` (str, readonly): Order type (LIMIT, MARKET, etc.)
- `price` (Decimal, readonly): Order price
- `amount` (Decimal, readonly): Order amount
- `remaining` (Decimal or None, readonly): Unfilled amount
- `account` (str, readonly): Account identifier
- `timestamp` (float or None, readonly): Event timestamp
- `raw` (object, readonly): Original data

**Order Status Constants:**
- OPEN, PENDING, FILLED, PARTIAL, CANCELLED, UNFILLED
- EXPIRED, SUSPENDED, FAILED, SUBMITTING, CANCELLING, CLOSED

**Order Type Constants:**
- LIMIT, MARKET, STOP_LIMIT, STOP_MARKET
- FILL_OR_KILL, IMMEDIATE_OR_CANCEL, GOOD_TIL_CANCELED

### 11. Order
**Purpose:** Order placement specification
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Trading pair
- `client_order_id` (str): Client order ID
- `side` (str): BUY or SELL
- `type` (str): Order type
- `price` (Decimal): Order price
- `amount` (Decimal): Order quantity
- `account` (str): Account identifier
- `timestamp` (float): Creation timestamp

**Difference from OrderInfo:** Order is for placement, OrderInfo is for status/tracking

### 12. Fill
**Purpose:** Trade execution details (fill reports)
**Fields:**
- `exchange` (str, readonly): Exchange identifier
- `symbol` (str, readonly): Trading pair
- `price` (Decimal, readonly): Execution price
- `amount` (Decimal, readonly): Filled quantity
- `side` (str, readonly): BUY or SELL
- `fee` (Decimal or None, readonly): Trading fee
- `id` (str, readonly): Fill ID
- `order_id` (str, readonly): Parent order ID
- `liquidity` (str, readonly): MAKER or TAKER
- `type` (str, readonly): Order type
- `account` (str, readonly): Account identifier
- `timestamp` (float, readonly): Fill timestamp
- `raw` (object, readonly): Original data

**Use Case:** Trade reconciliation, fee accounting, execution quality

### 13. Balance
**Purpose:** Account balance information
**Fields:**
- `exchange` (str, readonly): Exchange identifier
- `currency` (str, readonly): Currency/asset code
- `balance` (Decimal, readonly): Total balance
- `reserved` (Decimal or None, readonly): Amount in orders
- `raw` (dict, readonly): Original data

**Use Case:** Portfolio tracking, available margin calculation

### 14. Position
**Purpose:** Open derivative positions
**Fields:**
- `exchange` (str): Exchange identifier
- `symbol` (str): Contract symbol
- `position` (Decimal): Position size (positive/negative for long/short)
- `entry_price` (Decimal): Average entry price
- `side` (object): LONG, SHORT, or BOTH
- `unrealised_pnl` (Decimal, nullable): Unrealized profit/loss
- `timestamp` (float, nullable): Update timestamp
- `raw` (dict or list, nullable): Original data

**Position Side Constants:**
- LONG, SHORT, BOTH (for hedge mode)

**Use Case:** Risk monitoring, P&L tracking

### 15. Transaction
**Purpose:** Deposit/withdrawal records
**Fields:**
- `exchange` (str): Exchange identifier
- `currency` (str): Currency code
- `type` (str): Transaction type (DEPOSIT, WITHDRAWAL)
- `status` (str): Transaction status
- `amount` (Decimal): Transaction amount
- `timestamp` (double): Event timestamp
- `raw` (dict): Original data

**Use Case:** Account reconciliation, audit trails

## Symbol Normalization

### Standard Format
Cryptofeed uses hyphen-separated normalized symbols:

**SPOT:** `BASE-QUOTE` (e.g., `BTC-USD`, `ETH-USDT`)
**PERPETUAL:** `BASE-QUOTE-PERP` (e.g., `BTC-USD-PERP`)
**FUTURES:** `BASE-QUOTE-EXPIRY` (e.g., `BTC-USD-25Z`, `ETH-USDT-250328`)
**OPTIONS:** `BASE-QUOTE-STRIKE-EXPIRY-CALLPUT`
**FX:** `BASE-QUOTE-FX`
**CURRENCY:** Single value (e.g., `USD`, `BTC`)

### Expiry Date Codes
Uses CME month codes:
- F=Jan, G=Feb, H=Mar, J=Apr, K=May, M=Jun
- N=Jul, Q=Aug, U=Sep, V=Oct, X=Nov, Z=Dec

Example: `BTC-USD-25Z` = Bitcoin futures expiring December 2025

### Symbol Mapping
The `Symbol` class provides:
- Bidirectional conversion between normalized and exchange-specific formats
- Validation of required fields (strike prices, expiry dates)
- Automatic date format conversion
- Registry lookup via `_Symbols.find()` method

## Data Standardization Principles

### 1. Numeric Precision
**All financial values use Python's `Decimal` type:**
- Prevents floating-point arithmetic errors
- Maintains precision for fractional prices and quantities
- Critical for accurate financial calculations

**Conversion Pattern:**
```python
from decimal import Decimal
price = Decimal(msg['p'])  # Exchange string → Decimal
```

### 2. Timestamp Normalization
**Unified to Unix seconds (float/double):**
- Exchange milliseconds → seconds: `ts / 1000.0`
- All timestamps in UTC
- `receipt_timestamp` parameter tracks message receipt time for latency analysis

### 3. Field Standardization
**Consistent naming across exchanges:**
- `side`: BUY/SELL (not "buy"/"b"/1/2)
- `symbol`: Normalized format (not "BTCUSDT" or "BTC-PERP")
- `amount`/`quantity`: Consistent terminology
- `timestamp`: Always Unix seconds

### 4. Raw Data Preservation
**Every data type includes `raw` field:**
- Contains original exchange message
- Enables debugging and validation
- Allows access to exchange-specific fields
- Type: `dict` or `list` depending on exchange format

## Exchange Implementation Pattern

### Message Routing
Exchanges implement `message_handler()` that:
1. Identifies message type via event field (`'e'`, `'channel'`, etc.)
2. Routes to appropriate parser method
3. Extracts and converts fields
4. Creates standardized data objects
5. Invokes registered callbacks

**Example (Binance):**
```python
def message_handler(self, msg):
    if msg.get('e') == 'depthUpdate':
        self._book_update(msg)
    elif msg.get('e') == 'aggTrade':
        self._trade_update(msg)
    elif msg.get('e') == 'forceOrder':
        self._liquidation_update(msg)
```

### Data Conversion Pipeline
1. **Extract:** Parse exchange-specific JSON structure
2. **Convert:** Transform to standard types (Decimal, normalized symbols)
3. **Normalize:** Apply timestamp conversion, symbol mapping
4. **Construct:** Create appropriate data type object
5. **Callback:** Pass to user handlers with receipt timestamp

### Field Mapping
Exchanges map their fields to standard names:
```python
# Exchange specific → Standard
'p' → price
'q' → amount/quantity
'S' → side (mapped to BUY/SELL constants)
'T' → timestamp (converted from ms to seconds)
'b' → bid_price
'a' → ask_price
```

## Callback System

### Callback Interface
All callbacks receive two parameters:
```python
async def callback(data_object, receipt_timestamp):
    # data_object: One of the 15 data types
    # receipt_timestamp: Message receipt time (for latency)
    pass
```

### Supported Callback Types
1. `TradeCallback`
2. `TickerCallback`
3. `L1BookCallback`
4. `BookCallback` (L2/L3)
5. `CandleCallback`
6. `FundingCallback`
7. `OpenInterestCallback`
8. `LiquidationCallback`
9. `IndexCallback`
10. `OrderInfoCallback`
11. `BalancesCallback`
12. `TransactionsCallback`
13. `UserFillsCallback`
14. `PositionCallback` (inferred)

### Execution Model
- **Async-first:** Callbacks can be async or sync functions
- **Auto-detection:** Uses `inspect.iscoroutinefunction()`
- **Sync support:** Runs sync callbacks in executor
- **Type routing:** Framework routes messages to appropriate callback type

## Supported Exchanges (43+)

### Major Exchanges
**Spot & Derivatives:**
- Binance (spot, futures, delivery, US, TR variants)
- Coinbase
- Kraken (spot, futures)
- OKX / OKCoin
- Bybit
- Deribit
- Bitfinex
- Gate.io (spot, futures)

**Spot Focused:**
- Bitstamp
- Gemini
- KuCoin
- Crypto.com
- Bitget

**Derivatives Focused:**
- BitMEX
- Phemex
- Delta
- dYdX

### Regional Exchanges
- Huobi (spot, DM, swap)
- Upbit (Korea)
- Bithumb (Korea)
- Bitflyer (Japan)

### Additional Exchanges (30+)
AscendEx, Bequant, Bit.com, Blockchain, EXX, FMFW, HitBTC, Independent Reserve, Poloniex, ProBit, and others

**Total:** 43 exchange implementations with shared functionality via mixins

## Backend Support

### Storage Backends
**Databases:**
- PostgreSQL
- MongoDB
- InfluxDB
- QuestDB
- QuasarDB
- VictoriaMetrics
- Arctic

**Message Queues:**
- Kafka
- RabbitMQ (exchange and queue modes)

**In-Memory:**
- Redis

**Cloud:**
- Google Cloud Pub/Sub

**Network Protocols:**
- TCP, UDP, UDS (Unix Domain Sockets)
- ZeroMQ

### Backend Pattern
Backends receive normalized data via callbacks and handle persistence:
```python
from cryptofeed import FeedHandler
from cryptofeed.backends.postgres import TradePostgres

fh = FeedHandler()
fh.add_feed(COINBASE,
            channels=[TRADES],
            symbols=['BTC-USD'],
            callbacks={TRADES: TradePostgres()})
```

## Performance Optimizations

### 1. Cython Implementation
**Core data types compiled with Cython (`types.pyx`):**
- Significant performance improvement over pure Python
- Static typing for speed
- Memory-efficient C-level structures

### 2. Object Pooling
**Freelist optimization for high-frequency objects:**
```python
@cython.freelist(128)
cdef class Trade:
    # Maintains pool of 128 pre-allocated objects
```
Reduces allocation overhead for frequently created objects

### 3. SortedDict for Order Books
**Efficient price level management:**
- O(log n) insertion/deletion
- Maintains sorted price order
- Fast best bid/ask access via indexing

## Usage Examples

### Basic Setup
```python
from cryptofeed import FeedHandler
from cryptofeed.defines import TRADES, L2_BOOK, TICKER
from cryptofeed.exchanges import Coinbase, Binance

async def trade_handler(trade, receipt_timestamp):
    print(f"{trade.exchange} {trade.symbol}: {trade.price} @ {trade.amount}")

async def book_handler(book, receipt_timestamp):
    best_bid = book.book.bids.index(0)[0]
    best_ask = book.book.asks.index(0)[0]
    print(f"Spread: {best_ask - best_bid}")

fh = FeedHandler()
fh.add_feed(Coinbase(channels=[TRADES, L2_BOOK],
                     symbols=['BTC-USD'],
                     callbacks={
                         TRADES: trade_handler,
                         L2_BOOK: book_handler
                     }))
fh.add_feed(Binance(channels=[TICKER],
                    symbols=['BTC-USDT'],
                    callbacks={TICKER: ticker_handler}))
fh.run()
```

### Data Access Patterns
```python
# Trade object
trade.exchange  # 'COINBASE'
trade.symbol    # 'BTC-USD'
trade.side      # 'BUY'
trade.price     # Decimal('50000.00')
trade.amount    # Decimal('0.1')
trade.timestamp # 1634567890.123

# OrderBook object
book.book.bids.keys()           # All bid prices
book.book.asks.values()         # All ask sizes
book.book.bids.index(0)         # (best_bid_price, size)
book.delta[BID]                 # [(price, size), ...]
book.sequence_number            # Message sequence

# Candle object
candle.open     # Decimal('50000.00')
candle.high     # Decimal('51000.00')
candle.low      # Decimal('49500.00')
candle.close    # Decimal('50500.00')
candle.volume   # Decimal('1234.56')
candle.interval # '1h'
candle.closed   # True
```

## Architecture Insights

### Design Philosophy
1. **Normalization First:** Convert all exchange data to standard formats
2. **Preserve Raw Data:** Always maintain original exchange message
3. **Callback-Driven:** Event-driven architecture for real-time processing
4. **Backend Flexibility:** Decouple data collection from storage
5. **Exchange Agnostic:** Write once, work with any supported exchange

### Extensibility
**Adding new exchanges:**
1. Subclass `FeedHandler` or `Exchange`
2. Implement `message_handler()` for message routing
3. Map exchange fields to standard data types
4. Register supported channels and symbols

**Adding new data types:**
1. Define Cython class in `types.pyx`
2. Add corresponding callback class in `callback.py`
3. Update exchange handlers to parse new type
4. Define channel constant in `defines.py`

### Quality Features
- **Sequence numbers:** Detect message gaps
- **Checksums:** Validate order book integrity
- **Latency tracking:** Receipt timestamps for monitoring
- **Raw data:** Enable debugging and validation
- **Type safety:** Cython static typing where possible

## Key Takeaways

### Strengths
1. **Comprehensive:** 43+ exchanges, 15+ data types
2. **Normalized:** Consistent API across all exchanges
3. **Precise:** Decimal types for financial accuracy
4. **Fast:** Cython optimizations and object pooling
5. **Flexible:** Multiple backends and callback patterns
6. **Production-Ready:** Used by trading systems and research platforms

### Best Practices
1. Always use Decimal for financial calculations
2. Check `raw` field when debugging exchange-specific issues
3. Monitor `sequence_number` for data gaps
4. Use `receipt_timestamp` for latency analysis
5. Validate `checksum` for order book integrity
6. Handle partial fills via `remaining` field in OrderInfo

### Common Patterns
```python
# Type checking
assert isinstance(trade.price, Decimal)
assert trade.side in ['BUY', 'SELL']

# Dictionary conversion
trade_dict = trade.to_dict(numeric_type=float)

# Book operations
best_bid_price = book.book.bids.index(0)[0]
best_bid_size = book.book.bids.index(0)[1]
spread = best_ask_price - best_bid_price

# Delta processing
for price, size in book.delta[BID]:
    if size == 0:
        # Level removed
        pass
    else:
        # Level added/updated
        pass
```

## References

**Primary Sources:**
- GitHub: https://github.com/bmoscon/cryptofeed
- Documentation: https://cryptofeed.readthedocs.io
- PyPI: https://pypi.org/project/cryptofeed/

**Key Files:**
- `/cryptofeed/types.pyx` - All data type definitions
- `/cryptofeed/defines.py` - Constants and channel definitions
- `/cryptofeed/symbols.py` - Symbol normalization
- `/cryptofeed/callback.py` - Callback interfaces
- `/cryptofeed/exchanges/` - Exchange implementations (43 files)
- `/examples/` - Usage examples (41 examples)

**Technical Specifications:**
- Python: 3.8+ required
- License: XFree86
- Performance: Cython 4.6%, Python 95.3%
- Repository: 2.6k stars, 741 forks

## Related Topics

[[cryptocurrency-market-data]] [[python-decimal-precision]] [[websocket-data-feeds]] [[order-book-management]] [[real-time-trading-systems]] [[data-normalization-patterns]] [[exchange-integration]] [[cython-optimization]]

---

**Research Date:** 2025-10-16
**Research Method:** Multi-source web research + GitHub repository analysis
**Validation:** Cross-referenced official documentation, source code, and examples
**Confidence Level:** High (primary sources, complete code review)
**Next Steps:** Implement cryptofeed integration, test data type usage, benchmark performance
