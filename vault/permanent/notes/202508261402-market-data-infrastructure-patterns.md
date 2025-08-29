---
date: 2025-08-26
type: zettel
tags: [market-data, time-series, data-quality, real-time-processing, financial-infrastructure]
links: ["[[202508251225-crypto-quant-trading-systems-overview]]", "[[202508261401-event-driven-architecture-core-principles]]"]
---

# Market Data Infrastructure Patterns

## Core Concept

**Systematic capture, validation, normalization, and distribution of financial market data** optimized for both historical analysis and real-time algorithmic decision-making with pristine data quality guarantees.

## Architecture Patterns

### Lambda Architecture for Market Data
```
Historical Data → Batch Processing → Analytics Database
     ↓               ↓                     ↓
Real-Time Feed → Stream Processing → Live Cache → Trading Engine
     ↓               ↓                     ↓
   Archive ← Reconciliation ← Quality Control
```

**Design Principles**:
- **Immutable Data**: Raw market data never modified, only enhanced
- **Multiple Representations**: Same data optimized for different access patterns
- **Quality Gates**: Systematic validation at every processing stage
- **Reconciliation**: Batch and real-time views eventually consistent

### Multi-Exchange Normalization Layer

**Standardization Challenges**:
- **Price Precision**: Different decimal places (8 vs 2 vs 4)
- **Volume Units**: Base vs quote currency denomination
- **Timestamp Formats**: UTC vs exchange-local vs Unix epoch
- **Message Schemas**: REST vs WebSocket vs FIX protocol variations

**Normalization Strategy**:
```python
class UnifiedTick:
    symbol: str          # BTC/USDT (unified format)
    exchange: str        # binance, coinbase, kraken
    timestamp: datetime  # UTC with microsecond precision
    price: Decimal       # 8 decimal places (crypto standard)
    volume: Decimal      # Base currency units
    side: str           # bid, ask, trade
    sequence_id: int    # Exchange sequence number
```

### Time-Series Storage Optimization

#### **TimescaleDB Pattern**
```sql
-- Hypertable with automatic partitioning
CREATE TABLE market_ticks (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    price NUMERIC(20,8),
    volume NUMERIC(20,8),
    side TEXT
);

-- Partition by time + symbol for query optimization
SELECT create_hypertable('market_ticks', 'time', 
                        partitioning_column => 'symbol',
                        number_partitions => 16);

-- Compress old data (90%+ reduction)
ALTER TABLE market_ticks SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol,exchange'
);
```

**Performance Benefits**:
- **100M+ inserts/day**: Sustained write performance
- **Complex queries**: Sub-second analytical queries on TB+ data
- **Storage efficiency**: 10:1 compression ratios for historical data
- **PostgreSQL compatibility**: Standard SQL with time-series optimization

#### **Parquet + Delta Lake Pattern**
```python
# Partitioned by date and symbol for analytics
data_path = f"s3://market-data/year={year}/month={month}/day={day}/symbol={symbol}"

# Schema evolution support
schema = pa.schema([
    ('timestamp', pa.timestamp('us', tz='UTC')),
    ('symbol', pa.string()),
    ('price', pa.decimal128(20, 8)),
    ('volume', pa.decimal128(20, 8))
])

# ACID transactions on data lake
delta_table.write.mode('append').partitionBy(['year', 'month', 'symbol']).save()
```

## Data Quality Framework

### Validation Pipeline
```
Raw Data → Format Check → Range Validation → Gap Detection → Outlier Analysis → Quality Score
    ↓           ↓              ↓               ↓               ↓              ↓
  Reject    Standard     Market Hours    Missing Ticks    Statistical    Acceptance
           Format       Price Limits     Interpolation    Anomalies      Threshold
```

**Quality Metrics**:
- **Completeness**: >99.9% expected ticks received
- **Accuracy**: Price/volume within expected ranges
- **Timeliness**: <100ms from exchange to processing
- **Consistency**: Cross-exchange price correlation validation

### Gap Detection and Handling
```python
class MarketDataQualityChecker:
    def detect_gaps(self, symbol: str, start_time: datetime, end_time: datetime):
        expected_intervals = self.calculate_expected_ticks(symbol, start_time, end_time)
        actual_intervals = self.query_tick_timestamps(symbol, start_time, end_time)
        
        gaps = []
        for expected in expected_intervals:
            if not any(abs((actual - expected).total_seconds()) < 1.0 
                      for actual in actual_intervals):
                gaps.append(expected)
                
        return self.classify_gaps(gaps)  # Missing vs Exchange Downtime vs Network
```

## Real-Time Processing Patterns

### WebSocket Connection Management
```python
class ExchangeConnector:
    async def maintain_connections(self):
        while True:
            for exchange in self.exchanges:
                if not exchange.is_connected():
                    await self.reconnect_with_backoff(exchange)
                    
                # Health check via ping/pong
                if exchange.last_message_age() > self.heartbeat_timeout:
                    await self.send_ping(exchange)
                    
            await asyncio.sleep(1)
    
    async def reconnect_with_backoff(self, exchange):
        # Exponential backoff: 1s, 2s, 4s, 8s, max 30s
        for attempt in range(10):
            try:
                await exchange.connect()
                return
            except ConnectionError:
                await asyncio.sleep(min(30, 2 ** attempt))
```

### Rate Limiting and Throttling
```python
class RateLimiter:
    def __init__(self, requests_per_second: int):
        self.rate = requests_per_second
        self.tokens = requests_per_second
        self.last_update = time.time()
    
    async def acquire(self):
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.rate, self.tokens + elapsed * self.rate)
        self.last_update = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return
        
        # Wait for next token
        wait_time = (1 - self.tokens) / self.rate
        await asyncio.sleep(wait_time)
        self.tokens = 0
```

## Cross-Domain Applications

### Universal Data Infrastructure Patterns
**Applicable to any real-time data system**:
- **IoT Sensor Networks**: Device telemetry, status monitoring
- **Web Analytics**: User behavior tracking, performance metrics
- **Supply Chain**: Inventory updates, shipment tracking
- **Gaming**: Player actions, game state updates
- **Healthcare**: Patient monitoring, diagnostic data

### Mental Model Applications

#### **Charlie Munger Economics Models**
- **Network Effects**: More exchanges → better price discovery → more participants
- **Competitive Advantage**: Data quality and latency as moats
- **Scale Economics**: Fixed infrastructure costs distributed over volume

#### **Physics Models**
- **Information Theory**: Data compression vs query performance trade-offs
- **Thermodynamics**: System entropy increases without data quality maintenance
- **Conservation Laws**: Data lineage and audit trail preservation

## Success Factors

### Technical Excellence
- **Multi-9s Reliability**: 99.99% uptime during trading hours
- **Sub-millisecond Latency**: End-to-end tick processing
- **Petabyte Scale**: Historical data retention and query performance
- **Global Distribution**: Edge processing for geographic distribution

### Operational Excellence
- **Monitoring**: Real-time quality metrics, alerting, SLA tracking
- **Data Lineage**: Complete audit trail from source to consumption
- **Schema Management**: Backward-compatible evolution of data formats
- **Disaster Recovery**: Multi-region replication, automated failover

### Business Impact
- **Decision Quality**: High-quality data enables superior algorithmic decisions
- **Regulatory Compliance**: Complete audit trails for financial reporting
- **Competitive Advantage**: Speed and quality advantages in market access
- **Revenue Generation**: Data products and insights as additional revenue streams

---

**Meta**: Market data infrastructure patterns represent the intersection of high-performance computing, distributed systems, and data engineering - creating universal principles applicable to any system requiring real-time data processing with quality guarantees.