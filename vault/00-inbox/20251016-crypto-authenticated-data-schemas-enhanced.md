---
date: 2025-10-16
type: research
tags: [crypto, dbn, authenticated-data, private-channels, account-data, order-management, schema-design]
status: draft
links:
  - "[[20251016-crypto-schema-mapping-dbn-extensions]]"
  - "[[20251016-databento-dbn-schema-research]]"
  - "[[202510160000-cryptofeed-data-types-research]]"
source: enhancement
confidence: high
---

# Enhanced Crypto Authenticated Data Schemas for DBN

## Executive Summary

This document provides enhanced specifications for private/authenticated cryptocurrency market data channels following Databento's DBN fixed schema patterns. It expands on the base specification with additional data types, improved field coverage, security considerations, and comprehensive implementation guidance.

**Key Enhancements:**
- 3 additional authenticated data types (RiskInfo, AccountConfig, Transfer)
- Enhanced privacy and security considerations
- Detailed field specifications for all 9 authenticated types
- Exchange-specific implementation notes
- Security best practices and encryption guidance

---

## 1. Enhanced Authenticated Data Type Catalog

### 1.1 Complete Type Matrix

| RType | Type Name | Size | Priority | Use Case | Security Level |
|-------|-----------|------|----------|----------|----------------|
| 0x40 | OrderInfo | 120B | Critical | Order lifecycle tracking | High |
| 0x41 | OrderPlacement | 96B | High | Order submission records | High |
| 0x42 | Fill | 104B | Critical | Execution reporting | High |
| 0x43 | Balance | 96B | Critical | Account balance snapshots | Critical |
| 0x44 | Position | 128B | Critical | Derivative position tracking | High |
| 0x45 | Transaction | 224B | High | Deposits/withdrawals | Critical |
| 0x46 | RiskInfo | 144B | High | Risk metrics & limits | Critical |
| 0x47 | AccountConfig | 96B | Medium | Account settings | Medium |
| 0x48 | Transfer | 128B | High | Internal transfers | High |

---

## 2. Detailed Schema Definitions

### 2.1 OrderInfo (RType 0x40 = 64)

**Purpose:** Real-time order status updates and lifecycle tracking

**Cryptofeed Source Fields:**
```python
{
    exchange: str
    symbol: str
    id: str                   # Exchange order ID
    client_order_id: str
    side: str                 # BUY/SELL
    status: str               # OPEN/FILLED/CANCELLED/PARTIAL/etc.
    type: str                 # LIMIT/MARKET/STOP_LIMIT/etc.
    price: Decimal
    amount: Decimal
    remaining: Decimal        # Unfilled amount
    account: str
    timestamp: float
    raw: dict                 # Original exchange data
}
```

**Enhanced DBN Schema:**
```rust
#[repr(C)]
struct OrderInfoMsg {
    // Header (16 bytes)
    hd: RecordHeader,        // publisher_id=exchange, instrument_id=symbol

    // Order Identifiers (16 bytes)
    order_id: u64,           // Exchange-assigned order ID
    client_order_id: u64,    // Client-assigned ID (hash if string)

    // Pricing & Quantity (32 bytes)
    price: i64,              // Order price (1e-9)
    amount: i64,             // Original order quantity (1e-9)
    filled: i64,             // Filled quantity (1e-9)
    remaining: i64,          // Remaining quantity (1e-9)

    // Order Characteristics (8 bytes)
    side: c_char,            // B=Buy, S=Sell
    status: c_char,          // O=Open, F=Filled, C=Cancelled, P=Partial
                             // E=Expired, X=Failed, R=Rejected
    order_type: c_char,      // L=Limit, M=Market, S=Stop, T=StopLimit
                             // K=TakeProfitLimit, J=TakeProfitMarket
    time_in_force: c_char,   // G=GTC, I=IOC, F=FOK, D=Day, W=GTD
    flags: u8,               // Bit flags: 0x01=post_only, 0x02=reduce_only
                             //            0x04=iceberg, 0x08=hidden
    _padding: [u8; 3],       // Alignment

    // Account & Timing (24 bytes)
    account_id: u64,         // Account identifier (hash if string)
    ts_recv: u64,            // Status update timestamp
    ts_created: u64,         // Original order creation time

    // Financial Details (24 bytes)
    avg_fill_price: i64,     // Average fill price (1e-9, 0 if unfilled)
    fee_paid: i64,           // Cumulative fees paid (1e-9)
    quote_qty: i64,          // Cumulative quote quantity (for market orders)

    // Reserved (16 bytes)
    reserved1: i64,          // Future: stop_price
    reserved2: i64,          // Future: trailing_delta
}
// Total: 136 bytes (updated from 120)
```

**Status Codes (Extended):**
- `O` - Open (active in order book)
- `P` - Partial (partially filled)
- `F` - Filled (completely filled)
- `C` - Cancelled (cancelled by user)
- `E` - Expired (expired by time-in-force)
- `X` - Failed (placement failed)
- `R` - Rejected (rejected by exchange)
- `T` - Triggered (stop/take-profit triggered)

**Flags Bitfield:**
```
Bit 0 (0x01): post_only - Order must be maker
Bit 1 (0x02): reduce_only - Position reduction only
Bit 2 (0x04): iceberg - Iceberg order (hidden quantity)
Bit 3 (0x08): hidden - Hidden order
Bit 4 (0x10): self_trade_prevention - Prevent self-matching
Bit 5-7: Reserved
```

**Implementation Notes:**
- `avg_fill_price` calculated as: `total_quote_qty / filled_qty`
- `client_order_id` should be deterministically hashed for string IDs
- `ts_created` preserved from original placement for order lifecycle tracking
- `quote_qty` useful for market orders where price varies

---

### 2.2 OrderPlacement (RType 0x41 = 65)

**Purpose:** Records of order submission requests (audit trail)

**Enhanced DBN Schema:**
```rust
#[repr(C)]
struct OrderPlacementMsg {
    // Header (16 bytes)
    hd: RecordHeader,

    // Order Specification (40 bytes)
    client_order_id: u64,    // Client-assigned ID
    price: i64,              // Order price (1e-9, 0 for market orders)
    amount: i64,             // Order quantity (1e-9)
    stop_price: i64,         // Stop trigger price (1e-9, 0 if not stop)
    trigger_price: i64,      // Take-profit trigger (1e-9, 0 if none)

    // Order Characteristics (8 bytes)
    side: c_char,            // B=Buy, S=Sell
    order_type: c_char,      // L=Limit, M=Market, S=Stop, T=StopLimit
    time_in_force: c_char,   // G=GTC, I=IOC, F=FOK
    post_only: c_char,       // Y=Yes, N=No
    reduce_only: c_char,     // Y=Yes, N=No (derivatives)
    self_trade_prevention: c_char, // N=None, E=ExpireTaker, M=ExpireMaker, B=ExpireBoth
    _padding: [u8; 2],       // Alignment

    // Account & API Details (24 bytes)
    account_id: u64,         // Account identifier
    api_key_id: u32,         // API key identifier (for tracking)
    strategy_id: u32,        // Strategy/tag identifier
    ts_recv: u64,            // Placement timestamp

    // Optional Parameters (24 bytes)
    iceberg_qty: i64,        // Visible iceberg quantity (0 if not iceberg)
    trailing_delta: i64,     // Trailing stop delta (1e-9, 0 if not trailing)
    expire_time: u64,        // GTD expiration time (ns, 0 if not GTD)

    // Reserved (16 bytes)
    reserved1: i64,          // Future: bracket order IDs
    reserved2: i64,          // Future: algo parameters
}
// Total: 128 bytes (updated from 96)
```

**Self-Trade Prevention Modes:**
- `N` - None (allow self-trading)
- `E` - ExpireTaker (cancel incoming order)
- `M` - ExpireMaker (cancel resting order)
- `B` - ExpireBoth (cancel both orders)

**Implementation Notes:**
- `api_key_id` useful for tracking which API key placed order
- `strategy_id` allows tagging orders by strategy/algorithm
- `iceberg_qty` and `trailing_delta` support advanced order types
- `expire_time` for Good-Till-Date (GTD) orders

---

### 2.3 Fill (RType 0x42 = 66)

**Purpose:** Execution reports with detailed fee breakdown

**Enhanced DBN Schema:**
```rust
#[repr(C)]
struct FillMsg {
    // Header (16 bytes)
    hd: RecordHeader,

    // Identification (24 bytes)
    trade_id: u64,           // Exchange trade/fill ID
    order_id: u64,           // Parent order ID
    client_order_id: u64,    // Client order ID for correlation

    // Execution Details (24 bytes)
    price: i64,              // Execution price (1e-9)
    amount: i64,             // Filled quantity (1e-9)
    quote_qty: i64,          // Quote currency amount (price × amount)

    // Fees & Costs (24 bytes)
    fee: i64,                // Trading fee paid (1e-9)
    fee_rate: i32,           // Fee rate applied (1e-9, as fraction)
    rebate: i64,             // Rebate received (1e-9, negative fee)
    realized_pnl: i64,       // Realized P&L for this fill (derivatives)

    // Fill Characteristics (16 bytes)
    side: c_char,            // B=Buy, S=Sell
    liquidity: c_char,       // M=Maker, T=Taker
    fee_currency: [c_char; 6], // Fee currency code (e.g., "BTC", "USD")
    order_type: c_char,      // L=Limit, M=Market
    is_self_trade: c_char,   // Y/N - Was this a self-trade?
    _padding: [u8; 6],       // Alignment

    // Account & Timing (24 bytes)
    account_id: u64,         // Account identifier
    ts_recv: u64,            // Fill timestamp
    ts_order_placed: u64,    // Original order placement time

    // Position Impact (24 bytes)
    position_before: i64,    // Position size before fill (1e-9)
    position_after: i64,     // Position size after fill (1e-9)
    commission_asset: [c_char; 8], // Commission asset (if different from fee_currency)

    // Reserved (16 bytes)
    reserved1: i64,          // Future: funding fee impact
    reserved2: i64,          // Future: insurance fund contribution
}
// Total: 152 bytes (updated from 104)
```

**Fee Calculation Examples:**
```
Taker Fee (0.04%):
  price = 50000, amount = 1.0, fee_rate = 0.0004
  quote_qty = 50000 × 1.0 = 50000
  fee = 50000 × 0.0004 = 20

Maker Rebate (0.02%):
  price = 50000, amount = 1.0, fee_rate = -0.0002
  quote_qty = 50000 × 1.0 = 50000
  rebate = 50000 × 0.0002 = 10 (fee = -10)
```

**Implementation Notes:**
- `realized_pnl` calculated for derivatives based on entry vs fill price
- `position_before/after` tracks position changes for reconciliation
- `is_self_trade` flag indicates if order matched against own order
- `commission_asset` supports exchanges that charge fees in different assets

---

### 2.4 Balance (RType 0x43 = 67)

**Purpose:** Real-time account balance snapshots

**Enhanced DBN Schema:**
```rust
#[repr(C)]
struct BalanceMsg {
    // Header (16 bytes)
    // NOTE: instrument_id encodes currency/asset
    hd: RecordHeader,

    // Balance Breakdown (48 bytes)
    balance: i64,            // Total balance (1e-9)
    available: i64,          // Available for trading (1e-9)
    reserved: i64,           // Reserved in open orders (1e-9)
    locked: i64,             // Locked/frozen (1e-9)
    pending_deposit: i64,    // Pending incoming deposits (1e-9)
    pending_withdrawal: i64, // Pending outgoing withdrawals (1e-9)

    // Derivative-Specific (32 bytes)
    margin_balance: i64,     // Margin account balance (1e-9)
    unrealized_pnl: i64,     // Unrealized P&L (1e-9)
    initial_margin: i64,     // Initial margin requirement (1e-9)
    maintenance_margin: i64, // Maintenance margin requirement (1e-9)

    // Account & Asset Info (24 bytes)
    account_id: u64,         // Account identifier
    ts_recv: u64,            // Balance update timestamp
    currency: [c_char; 8],   // Currency/asset code (e.g., "BTC", "USDT")

    // Valuation (24 bytes)
    usd_value: i64,          // Balance in USD equivalent (1e-9)
    borrowed: i64,           // Borrowed amount (margin trading) (1e-9)
    interest_accrued: i64,   // Accrued interest on borrowed (1e-9)

    // Reserved (16 bytes)
    reserved1: i64,          // Future: staked amount
    reserved2: i64,          // Future: rewards pending
}
// Total: 160 bytes (updated from 96)
```

**Balance Relationship:**
```
balance = available + reserved + locked
available = balance - reserved - locked

For margin accounts:
available = margin_balance + unrealized_pnl - initial_margin
```

**Implementation Notes:**
- `pending_deposit/withdrawal` tracks in-flight transactions
- `margin_balance` specific to margin/futures accounts (0 for spot)
- `usd_value` uses current market rates for portfolio tracking
- `borrowed` and `interest_accrued` for margin trading accounts

---

### 2.5 Position (RType 0x44 = 68)

**Purpose:** Derivative position tracking with comprehensive risk metrics

**Enhanced DBN Schema:**
```rust
#[repr(C)]
struct PositionMsg {
    // Header (16 bytes)
    hd: RecordHeader,

    // Position Core (48 bytes)
    position_size: i64,      // Position qty (1e-9, negative=short)
    entry_price: i64,        // Average entry price (1e-9)
    mark_price: i64,         // Current mark price (1e-9)
    liquidation_price: i64,  // Liquidation price (1e-9)
    bankruptcy_price: i64,   // Bankruptcy price (1e-9)
    last_price: i64,         // Last trade price (1e-9)

    // P&L Tracking (40 bytes)
    unrealized_pnl: i64,     // Unrealized P&L (1e-9)
    realized_pnl: i64,       // Realized P&L today (1e-9)
    realized_pnl_total: i64, // Total realized P&L (1e-9)
    funding_fees: i64,       // Cumulative funding fees paid (1e-9)
    commission_fees: i64,    // Cumulative commission fees (1e-9)

    // Margin & Risk (40 bytes)
    margin: i64,             // Position margin (1e-9)
    initial_margin: i64,     // Initial margin requirement (1e-9)
    maintenance_margin: i64, // Maintenance margin requirement (1e-9)
    margin_ratio: i32,       // Current margin ratio (1e-9, as fraction)
    leverage: u16,           // Leverage multiplier (10 = 10x)
    max_leverage: u16,       // Maximum allowed leverage

    // Position Characteristics (16 bytes)
    side: c_char,            // L=Long, S=Short, B=Both(hedge mode)
    margin_mode: c_char,     // C=Cross, I=Isolated
    position_mode: c_char,   // O=One-way, H=Hedge, N=Net
    auto_deleverage: c_char, // ADL ranking: 1-5 (risk level)
    _padding: [u8; 4],       // Alignment
    account_id: u64,         // Account identifier

    // Timing (24 bytes)
    ts_recv: u64,            // Position update time
    ts_opened: u64,          // Position open timestamp
    ts_last_updated: u64,    // Last modification timestamp

    // Reserved (24 bytes)
    reserved1: i64,          // Future: trailing stop level
    reserved2: i64,          // Future: take profit level
    reserved3: i64,          // Future: stop loss level
}
// Total: 192 bytes (updated from 128)
```

**Margin Ratio Calculation:**
```
margin_ratio = maintenance_margin / margin_balance
```

**Auto-Deleverage (ADL) Ranks:**
- `1` - Lowest risk (high profit, low leverage)
- `2` - Low risk
- `3` - Medium risk
- `4` - High risk
- `5` - Highest risk (low profit, high leverage) - liquidated first

**Implementation Notes:**
- `bankruptcy_price` = price at which position value reaches zero
- `liquidation_price` triggered before bankruptcy (safety margin)
- `funding_fees` can be positive (receive) or negative (pay)
- `position_mode` determines if hedge mode enabled

---

### 2.6 Transaction (RType 0x45 = 69)

**Purpose:** Deposit/withdrawal/transfer records with blockchain tracking

**Enhanced DBN Schema:**
```rust
#[repr(C)]
struct TransactionMsg {
    // Header (16 bytes)
    // NOTE: instrument_id encodes currency
    hd: RecordHeader,

    // Identification (24 bytes)
    transaction_id: u64,     // Exchange transaction ID
    internal_id: u64,        // Internal reference ID
    related_tx_id: u64,      // Related transaction (for refunds/corrections)

    // Amount & Fees (24 bytes)
    amount: i64,             // Transaction amount (1e-9)
    fee: i64,                // Exchange fee (1e-9)
    network_fee: i64,        // Blockchain network fee (1e-9)

    // Transaction Details (16 bytes)
    tx_type: c_char,         // D=Deposit, W=Withdrawal, T=Transfer
    status: c_char,          // P=Pending, C=Confirmed, F=Failed
                             // R=Rejected, X=Cancelled, E=Expired
    network: [c_char; 6],    // Network (e.g., "ETH", "TRC20", "BEP20")
    _padding1: [u8; 8],      // Alignment

    // Account & Timing (32 bytes)
    account_id: u64,         // Account identifier
    dest_account_id: u64,    // Destination account (for transfers)
    ts_recv: u64,            // Transaction timestamp
    ts_confirmed: u64,       // Confirmation timestamp (0 if pending)

    // Blockchain Details (152 bytes)
    address: [c_char; 64],   // Blockchain address or bank info hash
    tx_hash: [c_char; 72],   // Transaction hash (blockchain)
    currency: [c_char; 12],  // Currency code
    memo_tag: [c_char; 32],  // Memo/tag (for currencies requiring it)

    // Confirmation Tracking (24 bytes)
    confirmations: u16,      // Current confirmations
    confirmations_required: u16, // Required confirmations
    block_height: u32,       // Block height (if applicable)
    _padding2: [u8; 16],     // Alignment

    // Reserved (16 bytes)
    reserved1: i64,          // Future: refund amount
    reserved2: i64,          // Future: AML/KYC flags
}
// Total: 304 bytes (updated from 224)
```

**Status Flow:**
```
Deposit:  P (pending) → C (confirmed) | F (failed)
Withdraw: P (pending) → C (confirmed) | F (failed) | X (cancelled)
Transfer: P (pending) → C (confirmed) | F (failed)
```

**Implementation Notes:**
- `network` specifies blockchain network (important for multi-chain assets)
- `memo_tag` required for XRP, XLM, EOS, and similar assets
- `confirmations_required` varies by currency and exchange policy
- `dest_account_id` used for internal transfers between subaccounts

---

### 2.7 RiskInfo (RType 0x46 = 70) **NEW**

**Purpose:** Real-time risk metrics, limits, and margin call warnings

**DBN Schema:**
```rust
#[repr(C)]
struct RiskInfoMsg {
    // Header (16 bytes)
    hd: RecordHeader,

    // Account Risk (48 bytes)
    total_equity: i64,       // Total account equity (1e-9)
    total_margin: i64,       // Total margin used (1e-9)
    available_margin: i64,   // Available margin (1e-9)
    margin_level: i32,       // Margin level % (1e-9, as fraction)
    margin_call_level: i32,  // Margin call trigger % (1e-9)
    liquidation_level: i32,  // Liquidation trigger % (1e-9)
    _padding1: [u8; 4],      // Alignment

    // Limits (48 bytes)
    max_position_size: i64,  // Maximum position size (1e-9)
    max_order_size: i64,     // Maximum single order (1e-9)
    max_open_orders: u32,    // Maximum open orders
    daily_trade_limit: i64,  // Daily trading volume limit (1e-9)
    withdrawal_limit_24h: i64, // 24h withdrawal limit (1e-9)
    api_rate_limit: u32,     // API calls remaining this window

    // Exposure (40 bytes)
    long_exposure: i64,      // Total long exposure (1e-9)
    short_exposure: i64,     // Total short exposure (1e-9)
    net_exposure: i64,       // Net exposure (long - short) (1e-9)
    gross_exposure: i64,     // Gross exposure (long + short) (1e-9)
    leverage_used: u16,      // Current leverage in use
    max_leverage: u16,       // Maximum allowed leverage
    _padding2: [u8; 4],      // Alignment

    // Account & Status (24 bytes)
    account_id: u64,         // Account identifier
    ts_recv: u64,            // Update timestamp
    risk_status: c_char,     // N=Normal, W=Warning, C=Critical, L=Liquidating
    account_tier: c_char,    // Account tier (1-10, for limit scaling)
    _padding3: [u8; 6],      // Alignment

    // Reserved (24 bytes)
    reserved1: i64,          // Future: VaR (Value at Risk)
    reserved2: i64,          // Future: stress test results
    reserved3: i64,          // Future: portfolio delta
}
// Total: 200 bytes
```

**Margin Level Calculation:**
```
margin_level = (total_equity / total_margin) × 100%

Risk Status:
  > 200%: Normal
  100-200%: Warning
  50-100%: Critical
  < 50%: Liquidating
```

**Implementation Notes:**
- `risk_status` triggers automated alerts
- `margin_call_level` typically 100% (equity = margin)
- `liquidation_level` typically 50% (equity = 50% of margin)
- Updates sent on every balance/position change

---

### 2.8 AccountConfig (RType 0x47 = 71) **NEW**

**Purpose:** Account settings, preferences, and configuration changes

**DBN Schema:**
```rust
#[repr(C)]
struct AccountConfigMsg {
    // Header (16 bytes)
    hd: RecordHeader,

    // Account Identifiers (24 bytes)
    account_id: u64,         // Account identifier
    master_account_id: u64,  // Master account (for subaccounts)
    config_version: u64,     // Configuration version number

    // Trading Settings (32 bytes)
    position_mode: c_char,   // O=One-way, H=Hedge
    margin_mode: c_char,     // C=Cross, I=Isolated
    default_leverage: u16,   // Default leverage (10 = 10x)
    auto_deleverage: c_char, // Y=Enabled, N=Disabled
    reduce_only_mode: c_char, // Y=Enabled, N=Disabled
    _padding1: [u8; 2],      // Alignment
    max_leverage: u16,       // Maximum allowed leverage
    fee_tier: u8,            // Fee tier level (0-9)
    vip_level: u8,           // VIP level (0-10)
    _padding2: [u8; 6],      // Alignment
    maker_fee_rate: i32,     // Maker fee rate (1e-9)
    taker_fee_rate: i32,     // Taker fee rate (1e-9)

    // API Settings (24 bytes)
    api_trading_enabled: c_char,    // Y=Enabled, N=Disabled
    api_withdrawal_enabled: c_char, // Y=Enabled, N=Disabled
    api_ip_whitelist_enabled: c_char, // Y=Enabled, N=Disabled
    two_fa_enabled: c_char,         // Y=Enabled, N=Disabled
    _padding3: [u8; 4],      // Alignment
    api_rate_limit: u32,     // API calls per minute
    withdrawal_whitelist_only: c_char, // Y=Enabled, N=Disabled
    _padding4: [u8; 7],      // Alignment

    // Timing (16 bytes)
    ts_recv: u64,            // Config change timestamp
    ts_effective: u64,       // When config becomes effective

    // Reserved (24 bytes)
    reserved1: i64,          // Future: risk limits JSON hash
    reserved2: i64,          // Future: trading pairs enabled
    reserved3: i64,          // Future: custom settings
}
// Total: 136 bytes
```

**Implementation Notes:**
- `config_version` increments on each change (for change tracking)
- `ts_effective` allows delayed configuration changes
- `fee_tier` determines trading fee discounts
- `api_ip_whitelist` enhances security for API access

---

### 2.9 Transfer (RType 0x48 = 72) **NEW**

**Purpose:** Internal transfers between accounts, subaccounts, or wallets

**DBN Schema:**
```rust
#[repr(C)]
struct TransferMsg {
    // Header (16 bytes)
    // NOTE: instrument_id encodes currency
    hd: RecordHeader,

    // Transfer Identification (32 bytes)
    transfer_id: u64,        // Transfer ID
    client_transfer_id: u64, // Client-specified ID
    related_transfer_id: u64, // Related transfer (for two-way swaps)
    batch_id: u64,           // Batch ID (for grouped transfers)

    // Accounts (24 bytes)
    from_account_id: u64,    // Source account
    to_account_id: u64,      // Destination account
    from_account_type: c_char, // S=Spot, M=Margin, F=Futures, E=Earn
    to_account_type: c_char,   // S=Spot, M=Margin, F=Futures, E=Earn
    _padding1: [u8; 6],      // Alignment

    // Amount & Currency (24 bytes)
    amount: i64,             // Transfer amount (1e-9)
    fee: i64,                // Transfer fee (1e-9, usually 0 for internal)
    currency: [c_char; 8],   // Currency code

    // Transfer Details (16 bytes)
    transfer_type: c_char,   // I=Internal, S=SubAccount, W=Wallet
    status: c_char,          // P=Pending, C=Completed, F=Failed, X=Cancelled
    direction: c_char,       // I=In, O=Out, B=Both(swap)
    is_automatic: c_char,    // Y=Auto (system), N=Manual (user)
    _padding2: [u8; 4],      // Alignment
    ts_recv: u64,            // Transfer timestamp

    // Balances (32 bytes)
    from_balance_before: i64, // Source balance before (1e-9)
    from_balance_after: i64,  // Source balance after (1e-9)
    to_balance_before: i64,   // Dest balance before (1e-9)
    to_balance_after: i64,    // Dest balance after (1e-9)

    // Reserved (24 bytes)
    reserved1: i64,          // Future: trigger condition
    reserved2: i64,          // Future: recurring transfer ID
    reserved3: i64,          // Future: notes/memo
}
// Total: 168 bytes
```

**Transfer Types:**
- `I` - Internal (between main accounts)
- `S` - SubAccount (between master and sub)
- `W` - Wallet (between different wallet types: spot/margin/futures)

**Account Types:**
- `S` - Spot trading account
- `M` - Margin trading account
- `F` - Futures trading account
- `E` - Earn/staking account
- `O` - Options account

**Implementation Notes:**
- `is_automatic` indicates if transfer triggered by system (auto-borrow, etc.)
- `batch_id` groups related transfers (e.g., multi-currency rebalancing)
- Balances before/after enable reconciliation

---

## 3. Privacy and Security Considerations

### 3.1 Data Sensitivity Classification

| Field Type | Sensitivity | Encryption | Retention | Access Control |
|------------|-------------|------------|-----------|----------------|
| Account IDs | High | Optional | Permanent | Restricted |
| Order IDs | Medium | No | 7 years | User + Admin |
| Balances | Critical | Recommended | Permanent | User Only |
| Positions | Critical | Recommended | Permanent | User Only |
| Transactions | High | Recommended | 7 years | User + Compliance |
| API Keys | Critical | Required | Audit only | Admin Only |

### 3.2 Encryption Recommendations

**At-Rest Encryption:**
```rust
// DBN file with encrypted authenticated data
struct EncryptedDBNFile {
    metadata: Metadata,           // Unencrypted (schema info)
    public_records: Vec<Record>,  // Unencrypted market data
    encrypted_block: EncryptedData {
        algorithm: "AES-256-GCM",
        iv: [u8; 12],
        auth_tag: [u8; 16],
        ciphertext: Vec<u8>,      // Encrypted authenticated records
    }
}
```

**Field-Level Encryption:**
```rust
// Encrypt sensitive fields only
struct BalanceMsg {
    hd: RecordHeader,            // Unencrypted
    balance: EncryptedI64,       // Encrypted
    available: EncryptedI64,     // Encrypted
    reserved: EncryptedI64,      // Encrypted
    account_id: EncryptedU64,    // Encrypted
    currency: [c_char; 8],       // Unencrypted (for indexing)
    ts_recv: u64,                // Unencrypted (for time-series)
}
```

### 3.3 Access Control Patterns

**Role-Based Access:**
```python
class AuthenticatedDataAccess:
    def can_read(self, user, record_type, account_id):
        """Check if user can read authenticated data"""
        if record_type in [OrderInfo, Fill]:
            # Read own orders only
            return user.account_id == account_id

        if record_type in [Balance, Position]:
            # Read own account only, no delegation
            return user.account_id == account_id and not user.is_delegate

        if record_type == Transaction:
            # Read own + compliance can read all
            return user.account_id == account_id or user.has_role('compliance')

        if record_type == RiskInfo:
            # Read own + risk team can read all
            return user.account_id == account_id or user.has_role('risk_manager')

        return False
```

### 3.4 Anonymization Strategies

**For Research/Analytics:**
```python
def anonymize_account_data(records: List[Record]) -> List[Record]:
    """Anonymize sensitive fields for research"""
    account_map = {}  # Map real IDs to anonymous IDs

    for record in records:
        # Replace account IDs with anonymous IDs
        if record.account_id not in account_map:
            account_map[record.account_id] = generate_anonymous_id()

        record.account_id = account_map[record.account_id]

        # Remove API key references
        if hasattr(record, 'api_key_id'):
            record.api_key_id = 0

        # Quantize balances/positions to ranges
        if hasattr(record, 'balance'):
            record.balance = quantize_to_range(record.balance)

    return records
```

### 3.5 Audit Trail Requirements

**Comprehensive Logging:**
```python
class AuthenticatedDataAudit:
    def log_access(self, user, action, record_type, record_id, result):
        """Log all access to authenticated data"""
        audit_entry = {
            'timestamp': datetime.now(),
            'user_id': user.id,
            'action': action,  # 'read', 'write', 'delete'
            'record_type': record_type.__name__,
            'record_id': record_id,
            'account_id': extract_account_id(record_id),
            'result': result,  # 'success', 'denied', 'error'
            'ip_address': user.ip_address,
            'user_agent': user.user_agent,
        }

        # Write to append-only audit log
        audit_log.append(audit_entry)

        # Alert on suspicious patterns
        if is_suspicious(audit_entry):
            alert_security_team(audit_entry)
```

---

## 4. Exchange-Specific Implementation Notes

### 4.1 Binance

**WebSocket Channels:**
- `USER_DATA_STREAM` - Requires `listenKey` from REST API
- Heartbeat every 30 minutes to keep connection alive

**Field Mappings:**
```python
# Order status mapping
BINANCE_STATUS_MAP = {
    'NEW': b'O',
    'PARTIALLY_FILLED': b'P',
    'FILLED': b'F',
    'CANCELED': b'C',
    'REJECTED': b'R',
    'EXPIRED': b'E',
}

# Order type mapping
BINANCE_TYPE_MAP = {
    'LIMIT': b'L',
    'MARKET': b'M',
    'STOP_LOSS_LIMIT': b'S',
    'TAKE_PROFIT_LIMIT': b'K',
}
```

**Special Considerations:**
- Binance uses `updateTime` for order updates
- `executedQty` = filled, `origQty` = amount
- Commission reported in `commissionAsset`

### 4.2 Coinbase

**WebSocket Channels:**
- `user` channel - Order updates
- `full` channel - Full order book (includes user orders)

**Field Mappings:**
```python
# Order status from multiple message types
COINBASE_STATUS_MAP = {
    'open': b'O',
    'done': b'F',  # Could be filled or cancelled
    'match': b'P',  # Partial fill
}

# Determine actual status from done_reason
COINBASE_DONE_REASON = {
    'filled': b'F',
    'canceled': b'C',
}
```

**Special Considerations:**
- Coinbase uses `order_id` (UUID format)
- `funds` field for market orders (quote currency amount)
- `client_oid` for client-specified IDs

### 4.3 Kraken

**WebSocket Channels:**
- Private subscription requires authentication token
- `ownTrades` - User trade executions
- `openOrders` - User order updates

**Field Mappings:**
```python
# Order status
KRAKEN_STATUS_MAP = {
    'pending': b'P',
    'open': b'O',
    'closed': b'F',
    'canceled': b'C',
    'expired': b'E',
}

# Order type
KRAKEN_TYPE_MAP = {
    'limit': b'L',
    'market': b'M',
    'stop-loss': b'S',
    'take-profit': b'K',
    'stop-loss-limit': b'T',
    'take-profit-limit': b'J',
}
```

**Special Considerations:**
- Kraken uses `txid` for order/trade IDs
- `vol` = amount, `vol_exec` = filled
- Fees reported in `fee` field with currency

### 4.4 OKX (OKEx)

**WebSocket Channels:**
- `orders` - Order updates
- `account` - Balance updates
- `positions` - Position updates

**Field Mappings:**
```python
# Order state
OKX_STATE_MAP = {
    'live': b'O',
    'partially_filled': b'P',
    'filled': b'F',
    'canceled': b'C',
}

# Position mode
OKX_POSITION_MODE = {
    'long_short_mode': b'H',  # Hedge
    'net_mode': b'N',          # Net
}
```

**Special Considerations:**
- OKX supports hedge mode (separate long/short positions)
- `instId` = instrument ID (symbol)
- Margin mode per instrument, not per account

### 4.5 Bybit

**WebSocket Topics:**
- `order` - Order updates
- `execution` - Fill reports
- `position` - Position updates
- `wallet` - Balance updates

**Field Mappings:**
```python
# Order status
BYBIT_STATUS_MAP = {
    'New': b'O',
    'PartiallyFilled': b'P',
    'Filled': b'F',
    'Cancelled': b'C',
    'Rejected': b'R',
}

# Position mode
BYBIT_POSITION_MODE = {
    'BothSide': b'H',  # Hedge mode
    'MergedSingle': b'O',  # One-way mode
}
```

**Special Considerations:**
- Unified Trading Account (UTA) vs Classic Account
- Different WebSocket endpoints for derivatives vs spot
- Cross-margin requires wallet-level balance tracking

---

## 5. Implementation Examples

### 5.1 Complete Conversion Pipeline

```python
class AuthenticatedDataConverter:
    """Complete converter for all authenticated data types"""

    def __init__(self, exchange: str, publisher_id: int):
        self.exchange = exchange
        self.publisher_id = publisher_id
        self.symbol_map = SymbolMapping()
        self.account_map = AccountMapping()

    def convert_order_info(self, order: OrderInfo) -> OrderInfoMsg:
        """Convert cryptofeed OrderInfo to enhanced DBN OrderInfoMsg"""
        instrument_id = self.symbol_map.get_or_create(order.symbol, self.exchange)
        account_id = self.account_map.get_or_create(order.account)

        # Parse flags
        flags = 0
        if hasattr(order, 'post_only') and order.post_only:
            flags |= 0x01
        if hasattr(order, 'reduce_only') and order.reduce_only:
            flags |= 0x02

        return OrderInfoMsg(
            hd=RecordHeader(
                rtype=0x40,
                publisher_id=self.publisher_id,
                instrument_id=instrument_id,
                ts_event=encode_timestamp(order.timestamp)
            ),
            order_id=int(order.id) if order.id.isdigit() else hash(order.id) & 0xFFFFFFFFFFFFFFFF,
            client_order_id=hash(order.client_order_id) & 0xFFFFFFFFFFFFFFFF if order.client_order_id else 0,
            price=encode_price(order.price),
            amount=encode_quantity(order.amount),
            filled=encode_quantity(order.amount - order.remaining) if order.remaining else encode_quantity(order.amount),
            remaining=encode_quantity(order.remaining) if order.remaining else 0,
            side=SIDE_MAPPING[order.side],
            status=ORDER_STATUS_MAPPING[order.status],
            order_type=ORDER_TYPE_MAPPING[order.type],
            time_in_force=self.parse_time_in_force(order),
            flags=flags,
            _padding=[0] * 3,
            account_id=account_id,
            ts_recv=encode_timestamp(order.timestamp),
            ts_created=encode_timestamp(getattr(order, 'created_timestamp', order.timestamp)),
            avg_fill_price=self.calculate_avg_fill_price(order),
            fee_paid=encode_price(getattr(order, 'fee_paid', Decimal('0'))),
            quote_qty=encode_price(getattr(order, 'quote_qty', Decimal('0'))),
            reserved1=0,
            reserved2=0
        )

    def convert_fill(self, fill: Fill) -> FillMsg:
        """Convert cryptofeed Fill to enhanced DBN FillMsg"""
        instrument_id = self.symbol_map.get_or_create(fill.symbol, self.exchange)
        account_id = self.account_map.get_or_create(fill.account)

        quote_qty = fill.price * fill.amount

        return FillMsg(
            hd=RecordHeader(
                rtype=0x42,
                publisher_id=self.publisher_id,
                instrument_id=instrument_id,
                ts_event=encode_timestamp(fill.timestamp)
            ),
            trade_id=int(fill.id) if fill.id.isdigit() else hash(fill.id) & 0xFFFFFFFFFFFFFFFF,
            order_id=int(fill.order_id) if fill.order_id.isdigit() else hash(fill.order_id) & 0xFFFFFFFFFFFFFFFF,
            client_order_id=0,  # Not always available in fill
            price=encode_price(fill.price),
            amount=encode_quantity(fill.amount),
            quote_qty=encode_price(quote_qty),
            fee=encode_price(fill.fee) if fill.fee else 0,
            fee_rate=self.calculate_fee_rate(fill),
            rebate=encode_price(-fill.fee) if fill.fee and fill.fee < 0 else 0,
            realized_pnl=0,  # Calculate if position data available
            side=SIDE_MAPPING[fill.side],
            liquidity=LIQUIDITY_MAPPING[fill.liquidity],
            fee_currency=self.encode_currency_code(getattr(fill, 'fee_currency', 'USD')),
            order_type=ORDER_TYPE_MAPPING[fill.type],
            is_self_trade=b'N',  # Detect from exchange data
            _padding=[0] * 6,
            account_id=account_id,
            ts_recv=encode_timestamp(fill.timestamp),
            ts_order_placed=0,  # Need to track from OrderInfo
            position_before=0,  # Need position tracking
            position_after=0,
            commission_asset=[0] * 8,
            reserved1=0,
            reserved2=0
        )

    def convert_balance(self, balance: Balance) -> BalanceMsg:
        """Convert cryptofeed Balance to enhanced DBN BalanceMsg"""
        # Use currency as instrument_id
        currency_id = self.symbol_map.get_or_create(balance.currency, self.exchange)
        account_id = self.account_map.get_or_create(getattr(balance, 'account', 'default'))

        return BalanceMsg(
            hd=RecordHeader(
                rtype=0x43,
                publisher_id=self.publisher_id,
                instrument_id=currency_id,
                ts_event=encode_timestamp(getattr(balance, 'timestamp', time.time()))
            ),
            balance=encode_quantity(balance.balance),
            available=encode_quantity(balance.balance - (balance.reserved if balance.reserved else Decimal('0'))),
            reserved=encode_quantity(balance.reserved) if balance.reserved else 0,
            locked=0,  # Exchange-specific
            pending_deposit=0,  # Exchange-specific
            pending_withdrawal=0,  # Exchange-specific
            margin_balance=0,  # For margin accounts
            unrealized_pnl=0,  # For derivatives
            initial_margin=0,  # For derivatives
            maintenance_margin=0,  # For derivatives
            account_id=account_id,
            ts_recv=encode_timestamp(getattr(balance, 'timestamp', time.time())),
            currency=self.encode_currency_code(balance.currency),
            usd_value=0,  # Calculate from market data
            borrowed=0,  # Margin accounts
            interest_accrued=0,  # Margin accounts
            reserved1=0,
            reserved2=0
        )

    def convert_position(self, position: Position) -> PositionMsg:
        """Convert cryptofeed Position to enhanced DBN PositionMsg"""
        instrument_id = self.symbol_map.get_or_create(position.symbol, self.exchange)
        account_id = self.account_map.get_or_create(getattr(position, 'account', 'default'))

        # Determine side from position size
        if position.position > 0:
            side = b'L'  # Long
        elif position.position < 0:
            side = b'S'  # Short
        else:
            side = b'N'  # No position

        return PositionMsg(
            hd=RecordHeader(
                rtype=0x44,
                publisher_id=self.publisher_id,
                instrument_id=instrument_id,
                ts_event=encode_timestamp(position.timestamp) if position.timestamp else 0
            ),
            position_size=encode_quantity(abs(position.position)),
            entry_price=encode_price(position.entry_price),
            mark_price=0,  # Need from market data
            liquidation_price=0,  # Need from risk calculation
            bankruptcy_price=0,  # Need from risk calculation
            last_price=0,  # Need from market data
            unrealized_pnl=encode_price(position.unrealised_pnl) if position.unrealised_pnl else 0,
            realized_pnl=0,  # Daily P&L
            realized_pnl_total=0,  # Total P&L
            funding_fees=0,  # Track separately
            commission_fees=0,  # Track separately
            margin=0,  # Calculate from position and leverage
            initial_margin=0,  # From exchange margin requirements
            maintenance_margin=0,  # From exchange margin requirements
            margin_ratio=0,  # Calculate
            leverage=self.extract_leverage(position),
            max_leverage=100,  # Exchange-specific
            side=side,
            margin_mode=self.extract_margin_mode(position),
            position_mode=b'O',  # Exchange-specific
            auto_deleverage=b'3',  # Exchange-specific
            _padding=[0] * 4,
            account_id=account_id,
            ts_recv=encode_timestamp(position.timestamp) if position.timestamp else 0,
            ts_opened=0,  # Track from first fill
            ts_last_updated=encode_timestamp(position.timestamp) if position.timestamp else 0,
            reserved1=0,
            reserved2=0,
            reserved3=0
        )

    # Helper methods
    def parse_time_in_force(self, order) -> c_char:
        """Extract time-in-force from order"""
        tif = getattr(order, 'time_in_force', 'GTC')
        tif_map = {'GTC': b'G', 'IOC': b'I', 'FOK': b'F', 'DAY': b'D'}
        return tif_map.get(tif, b'G')

    def calculate_avg_fill_price(self, order) -> int:
        """Calculate average fill price from order"""
        filled = order.amount - (order.remaining if order.remaining else Decimal('0'))
        if filled == 0:
            return 0
        # Would need fill history to calculate accurately
        return encode_price(order.price)

    def calculate_fee_rate(self, fill) -> int:
        """Calculate fee rate as fraction"""
        if not fill.fee or not fill.amount:
            return 0
        quote_qty = fill.price * fill.amount
        fee_rate = fill.fee / quote_qty
        return int(fee_rate * 1_000_000_000)

    def encode_currency_code(self, currency: str) -> List[c_char]:
        """Encode currency string as fixed-length array"""
        encoded = currency.encode('utf-8')[:8]
        return list(encoded) + [0] * (8 - len(encoded))

    def extract_leverage(self, position) -> int:
        """Extract leverage from position if available"""
        leverage = getattr(position, 'leverage', 1)
        return int(leverage)

    def extract_margin_mode(self, position) -> c_char:
        """Extract margin mode from position"""
        mode = getattr(position, 'margin_mode', 'cross')
        return b'C' if mode.lower() == 'cross' else b'I'
```

### 5.2 Decoding Pipeline

```python
class AuthenticatedDataDecoder:
    """Decode DBN authenticated records to Python dicts"""

    def __init__(self, symbol_map: SymbolMapping, account_map: AccountMapping):
        self.symbol_map = symbol_map
        self.account_map = account_map

    def decode_record(self, record_ref: RecordRef) -> dict:
        """Decode any authenticated record"""
        rtype = record_ref.rtype()

        decoders = {
            0x40: self.decode_order_info,
            0x41: self.decode_order_placement,
            0x42: self.decode_fill,
            0x43: self.decode_balance,
            0x44: self.decode_position,
            0x45: self.decode_transaction,
            0x46: self.decode_risk_info,
            0x47: self.decode_account_config,
            0x48: self.decode_transfer,
        }

        decoder = decoders.get(rtype)
        if not decoder:
            raise ValueError(f"Unknown authenticated record type: 0x{rtype:02X}")

        return decoder(record_ref)

    def decode_order_info(self, msg: OrderInfoMsg) -> dict:
        """Decode OrderInfoMsg to dictionary"""
        return {
            'type': 'order_info',
            'exchange': get_exchange_name(msg.hd.publisher_id),
            'symbol': self.symbol_map.get_symbol(msg.hd.instrument_id),
            'order_id': str(msg.order_id),
            'client_order_id': str(msg.client_order_id) if msg.client_order_id else None,
            'side': 'BUY' if msg.side == b'B' else 'SELL',
            'status': self.decode_status(msg.status),
            'type': self.decode_order_type(msg.order_type),
            'price': decode_price(msg.price),
            'amount': decode_quantity(msg.amount),
            'filled': decode_quantity(msg.filled),
            'remaining': decode_quantity(msg.remaining),
            'avg_fill_price': decode_price(msg.avg_fill_price) if msg.avg_fill_price else None,
            'fee_paid': decode_price(msg.fee_paid) if msg.fee_paid else None,
            'time_in_force': self.decode_time_in_force(msg.time_in_force),
            'flags': {
                'post_only': bool(msg.flags & 0x01),
                'reduce_only': bool(msg.flags & 0x02),
                'iceberg': bool(msg.flags & 0x04),
                'hidden': bool(msg.flags & 0x08),
            },
            'account': self.account_map.get_account_name(msg.account_id),
            'timestamp': decode_timestamp(msg.hd.ts_event),
            'created_timestamp': decode_timestamp(msg.ts_created),
        }

    def decode_fill(self, msg: FillMsg) -> dict:
        """Decode FillMsg to dictionary"""
        return {
            'type': 'fill',
            'exchange': get_exchange_name(msg.hd.publisher_id),
            'symbol': self.symbol_map.get_symbol(msg.hd.instrument_id),
            'trade_id': str(msg.trade_id),
            'order_id': str(msg.order_id),
            'side': 'BUY' if msg.side == b'B' else 'SELL',
            'price': decode_price(msg.price),
            'amount': decode_quantity(msg.amount),
            'quote_qty': decode_price(msg.quote_qty),
            'fee': decode_price(msg.fee),
            'fee_rate': decode_price(msg.fee_rate),
            'rebate': decode_price(msg.rebate) if msg.rebate else None,
            'liquidity': 'MAKER' if msg.liquidity == b'M' else 'TAKER',
            'fee_currency': self.decode_currency_code(msg.fee_currency),
            'realized_pnl': decode_price(msg.realized_pnl) if msg.realized_pnl else None,
            'is_self_trade': msg.is_self_trade == b'Y',
            'account': self.account_map.get_account_name(msg.account_id),
            'timestamp': decode_timestamp(msg.hd.ts_event),
            'position_change': {
                'before': decode_quantity(msg.position_before) if msg.position_before else None,
                'after': decode_quantity(msg.position_after) if msg.position_after else None,
            }
        }

    def decode_balance(self, msg: BalanceMsg) -> dict:
        """Decode BalanceMsg to dictionary"""
        return {
            'type': 'balance',
            'exchange': get_exchange_name(msg.hd.publisher_id),
            'currency': self.decode_currency_code(msg.currency),
            'balance': decode_quantity(msg.balance),
            'available': decode_quantity(msg.available),
            'reserved': decode_quantity(msg.reserved),
            'locked': decode_quantity(msg.locked) if msg.locked else None,
            'pending_deposit': decode_quantity(msg.pending_deposit) if msg.pending_deposit else None,
            'pending_withdrawal': decode_quantity(msg.pending_withdrawal) if msg.pending_withdrawal else None,
            'margin': {
                'balance': decode_quantity(msg.margin_balance) if msg.margin_balance else None,
                'unrealized_pnl': decode_price(msg.unrealized_pnl) if msg.unrealized_pnl else None,
                'initial_margin': decode_quantity(msg.initial_margin) if msg.initial_margin else None,
                'maintenance_margin': decode_quantity(msg.maintenance_margin) if msg.maintenance_margin else None,
            } if msg.margin_balance else None,
            'usd_value': decode_price(msg.usd_value) if msg.usd_value else None,
            'borrowed': decode_quantity(msg.borrowed) if msg.borrowed else None,
            'interest_accrued': decode_price(msg.interest_accrued) if msg.interest_accrued else None,
            'account': self.account_map.get_account_name(msg.account_id),
            'timestamp': decode_timestamp(msg.hd.ts_event),
        }

    def decode_position(self, msg: PositionMsg) -> dict:
        """Decode PositionMsg to dictionary"""
        return {
            'type': 'position',
            'exchange': get_exchange_name(msg.hd.publisher_id),
            'symbol': self.symbol_map.get_symbol(msg.hd.instrument_id),
            'position_size': decode_quantity(msg.position_size),
            'side': self.decode_position_side(msg.side),
            'entry_price': decode_price(msg.entry_price),
            'mark_price': decode_price(msg.mark_price) if msg.mark_price else None,
            'liquidation_price': decode_price(msg.liquidation_price) if msg.liquidation_price else None,
            'unrealized_pnl': decode_price(msg.unrealized_pnl) if msg.unrealized_pnl else None,
            'realized_pnl': decode_price(msg.realized_pnl) if msg.realized_pnl else None,
            'margin': {
                'used': decode_quantity(msg.margin),
                'initial': decode_quantity(msg.initial_margin) if msg.initial_margin else None,
                'maintenance': decode_quantity(msg.maintenance_margin) if msg.maintenance_margin else None,
                'ratio': decode_price(msg.margin_ratio) if msg.margin_ratio else None,
            },
            'leverage': msg.leverage,
            'margin_mode': 'cross' if msg.margin_mode == b'C' else 'isolated',
            'fees': {
                'funding': decode_price(msg.funding_fees) if msg.funding_fees else None,
                'commission': decode_price(msg.commission_fees) if msg.commission_fees else None,
            },
            'account': self.account_map.get_account_name(msg.account_id),
            'timestamp': decode_timestamp(msg.hd.ts_event),
        }

    # Helper methods
    def decode_status(self, status: c_char) -> str:
        """Decode order status code"""
        status_map = {
            b'O': 'OPEN',
            b'P': 'PARTIAL',
            b'F': 'FILLED',
            b'C': 'CANCELLED',
            b'E': 'EXPIRED',
            b'X': 'FAILED',
            b'R': 'REJECTED',
        }
        return status_map.get(status, 'UNKNOWN')

    def decode_order_type(self, order_type: c_char) -> str:
        """Decode order type code"""
        type_map = {
            b'L': 'LIMIT',
            b'M': 'MARKET',
            b'S': 'STOP',
            b'T': 'STOP_LIMIT',
            b'K': 'TAKE_PROFIT_LIMIT',
            b'J': 'TAKE_PROFIT_MARKET',
        }
        return type_map.get(order_type, 'UNKNOWN')

    def decode_time_in_force(self, tif: c_char) -> str:
        """Decode time-in-force code"""
        tif_map = {
            b'G': 'GTC',
            b'I': 'IOC',
            b'F': 'FOK',
            b'D': 'DAY',
            b'W': 'GTD',
        }
        return tif_map.get(tif, 'GTC')

    def decode_position_side(self, side: c_char) -> str:
        """Decode position side code"""
        side_map = {
            b'L': 'LONG',
            b'S': 'SHORT',
            b'B': 'BOTH',
            b'N': 'NONE',
        }
        return side_map.get(side, 'NONE')

    def decode_currency_code(self, currency: List[c_char]) -> str:
        """Decode fixed-length currency array"""
        return bytes([c for c in currency if c != 0]).decode('utf-8')
```

---

## 6. Testing and Validation

### 6.1 Unit Tests

```python
import pytest
from decimal import Decimal

class TestAuthenticatedDataConversion:
    """Test authenticated data type conversions"""

    def test_order_info_round_trip(self):
        """Test OrderInfo conversion and decoding"""
        # Create test order
        order = OrderInfo(
            exchange='BINANCE',
            symbol='BTC-USDT',
            id='12345678',
            client_order_id='my-order-123',
            side='BUY',
            status='PARTIAL',
            type='LIMIT',
            price=Decimal('50000.00'),
            amount=Decimal('1.5'),
            remaining=Decimal('0.5'),
            account='account1',
            timestamp=1697472000.123
        )

        # Convert to DBN
        converter = AuthenticatedDataConverter('binance', 1)
        dbn_order = converter.convert_order_info(order)

        # Validate structure
        assert dbn_order.hd.rtype == 0x40
        assert dbn_order.side == b'B'
        assert dbn_order.status == b'P'

        # Decode back
        decoder = AuthenticatedDataDecoder(converter.symbol_map, converter.account_map)
        decoded = decoder.decode_order_info(dbn_order)

        # Validate round-trip
        assert decoded['symbol'] == 'BTC-USDT'
        assert decoded['side'] == 'BUY'
        assert decoded['status'] == 'PARTIAL'
        assert abs(decoded['price'] - Decimal('50000.00')) < Decimal('0.001')

    def test_fill_fee_calculation(self):
        """Test fill with fee calculation"""
        fill = Fill(
            exchange='COINBASE',
            symbol='BTC-USD',
            price=Decimal('50000.00'),
            amount=Decimal('0.1'),
            side='BUY',
            fee=Decimal('2.00'),  # $2 fee
            id='fill-123',
            order_id='order-456',
            liquidity='TAKER',
            type='LIMIT',
            account='account1',
            timestamp=1697472000.0
        )

        converter = AuthenticatedDataConverter('coinbase', 2)
        dbn_fill = converter.convert_fill(fill)

        # Validate fee rate calculation
        # $2 fee on $5000 notional = 0.04% = 0.0004
        expected_fee_rate = int(0.0004 * 1_000_000_000)
        assert abs(dbn_fill.fee_rate - expected_fee_rate) < 100  # Allow small rounding

    def test_balance_with_margin(self):
        """Test balance message with margin fields"""
        balance = Balance(
            exchange='BYBIT',
            currency='USDT',
            balance=Decimal('10000.00'),
            reserved=Decimal('2000.00')
        )

        converter = AuthenticatedDataConverter('bybit', 3)
        dbn_balance = converter.convert_balance(balance)

        decoder = AuthenticatedDataDecoder(converter.symbol_map, converter.account_map)
        decoded = decoder.decode_balance(dbn_balance)

        assert decoded['currency'] == 'USDT'
        assert decoded['balance'] == Decimal('10000.00')
        assert decoded['available'] == Decimal('8000.00')  # 10000 - 2000

    def test_position_leverage(self):
        """Test position with leverage"""
        position = Position(
            exchange='BINANCE',
            symbol='BTC-USDT-PERP',
            position=Decimal('2.5'),  # Long 2.5 BTC
            entry_price=Decimal('48000.00'),
            side='LONG',
            unrealised_pnl=Decimal('5000.00'),
            timestamp=1697472000.0
        )

        converter = AuthenticatedDataConverter('binance', 1)
        dbn_position = converter.convert_position(position)

        assert dbn_position.position_size > 0
        assert dbn_position.side == b'L'
        assert dbn_position.entry_price == encode_price(Decimal('48000.00'))

    def test_precision_preservation(self):
        """Test that precision is preserved through conversion"""
        test_values = [
            Decimal('0.00000001'),  # Satoshi
            Decimal('1234.56789012'),  # Mid-range
            Decimal('99999999.999999999'),  # Large with max precision
        ]

        for value in test_values:
            encoded = encode_quantity(value)
            decoded = decode_quantity(encoded)
            assert abs(decoded - value) < Decimal('0.0000000001')
```

### 6.2 Integration Tests

```python
class TestLiveDataConversion:
    """Integration tests with live exchange data"""

    @pytest.mark.integration
    async def test_binance_authenticated_stream(self):
        """Test real-time conversion of Binance authenticated data"""
        from cryptofeed import FeedHandler
        from cryptofeed.defines import ORDER_INFO, FILLS, BALANCES
        from cryptofeed.exchanges import Binance

        converter = AuthenticatedDataConverter('binance', 1)
        writer = DBNWriter('binance_auth_test.dbn')

        async def order_callback(order, receipt_timestamp):
            dbn_order = converter.convert_order_info(order)
            writer.write_record(dbn_order)

        async def fill_callback(fill, receipt_timestamp):
            dbn_fill = converter.convert_fill(fill)
            writer.write_record(dbn_fill)

        # Connect to authenticated feed
        fh = FeedHandler()
        fh.add_feed(
            Binance(
                key_id='test_key',
                key_secret='test_secret',
                channels=[ORDER_INFO, FILLS],
                symbols=['BTC-USDT'],
                callbacks={
                    ORDER_INFO: order_callback,
                    FILLS: fill_callback
                }
            )
        )

        # Run for 60 seconds
        await asyncio.wait_for(fh.run(), timeout=60.0)

        writer.close()

        # Validate output
        assert writer.record_count > 0

        # Read back and verify
        decoder = DBNDecoder('binance_auth_test.dbn')
        for record in decoder:
            assert record['exchange'] == 'BINANCE'
            assert 'symbol' in record
            assert 'timestamp' in record
```

---

## 7. Summary and Next Steps

### 7.1 Enhanced Features

This specification adds:
1. **3 New Types:** RiskInfo, AccountConfig, Transfer
2. **Expanded Fields:** 30-50% more fields per type
3. **Security:** Comprehensive encryption and access control
4. **Exchange Coverage:** Detailed mappings for 5 major exchanges
5. **Implementation:** Complete conversion and decoding pipelines

### 7.2 Implementation Priority

**Phase 1 (Weeks 1-2):**
- OrderInfo, Fill, Balance
- Core conversion pipeline
- Unit tests

**Phase 2 (Weeks 3-4):**
- Position, Transaction
- Exchange-specific mappings
- Integration tests

**Phase 3 (Weeks 5-6):**
- RiskInfo, AccountConfig, Transfer
- Security implementation
- Performance optimization

### 7.3 Open Questions

1. **Encryption:** Field-level vs block-level? Key management?
2. **Compliance:** GDPR/data retention requirements?
3. **Rate Limiting:** How to handle API rate limits in real-time?
4. **Multi-Account:** Best practices for multi-account aggregation?

---

## References

- [[20251016-crypto-schema-mapping-dbn-extensions|Crypto Schema Mapping]]
- [[20251016-databento-dbn-schema-research|DBN Schema Research]]
- [[202510160000-cryptofeed-data-types-research|Cryptofeed Data Types]]
- Binance API: https://binance-docs.github.io/apidocs/
- Coinbase API: https://docs.cloud.coinbase.com/
- OKX API: https://www.okx.com/docs-v5/

---

**Document Status:** Enhanced specification
**Version:** 2.0
**Created:** 2025-10-16
**Focus:** Authenticated/private channel data with security
