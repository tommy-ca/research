# CAN SLIM Screening Criteria: Technical Specifications

## Core Screening Parameters

### Tier 1: Essential Criteria (Must Meet All)

| Criterion | Parameter | Threshold | Formula/Calculation | Rationale |
|-----------|-----------|-----------|-------------------|-----------|
| **C - Current Quarterly EPS** | YoY Growth | ≥ 25% | `(EPS_current - EPS_prior) / abs(EPS_prior) × 100` | Identifies acceleration |
| **Price Floor** | Stock Price | > $15 | Current market price | Ensures liquidity |
| **Volume Floor** | Avg Daily Volume | > 100,000 | 20-day average volume | Tradability requirement |
| **Exchange Quality** | Listing | NYSE, NASDAQ | Exchange membership | Excludes OTC/Pink sheets |

### Tier 2: Performance Criteria (Meet 4 of 6)

| Criterion | Parameter | Threshold | Formula/Calculation | Weight |
|-----------|-----------|-----------|-------------------|--------|
| **A - Annual EPS Growth** | 3-Year CAGR | ≥ 25% | `((EPS_year3/EPS_year0)^(1/3) - 1) × 100` | 20% |
| **A - Return on Equity** | ROE | ≥ 17% | `Net_Income / Shareholder_Equity × 100` | 15% |
| **N - Price Position** | % of 52W High | ≥ 90% | `Current_Price / 52_Week_High × 100` | 15% |
| **S - Outstanding Shares** | Float | < 50M shares | Shares available for trading | 10% |
| **L - Relative Strength** | RS Rating | ≥ 80 | Price performance vs market | 20% |
| **I - Institutional Count** | # of Holders | 20-500 | Number of institutional owners | 15% |

### Tier 3: Quality Filters (Additional Screening)

| Criterion | Parameter | Threshold | Formula/Calculation | Purpose |
|-----------|-----------|-----------|-------------------|---------|
| **Sales Growth** | Quarterly YoY | ≥ 25% | `(Sales_Q - Sales_Q-4) / Sales_Q-4 × 100` | Revenue validation |
| **Profit Margin** | Trend | Increasing | `PM_current > PM_avg_4Q` | Operational efficiency |
| **Debt/Equity** | Ratio | < 0.5 | `Total_Debt / Total_Equity` | Financial health |
| **Free Cash Flow** | Growth | Positive | `FCF_TTM > 0 AND FCF_growth > 0` | Cash generation |

## Detailed Calculation Methods

### 1. Earnings Per Share (EPS) Calculations

#### Current Quarterly EPS Growth
```python
def calculate_quarterly_eps_growth(current_q_eps, prior_year_q_eps):
    """
    Calculate year-over-year quarterly EPS growth
    Handles negative earnings appropriately
    """
    if prior_year_q_eps == 0:
        return float('inf') if current_q_eps > 0 else 0
    
    if prior_year_q_eps < 0:
        if current_q_eps >= 0:
            return 100  # Turnaround situation
        else:
            # Both negative: use absolute values
            return -((current_q_eps - prior_year_q_eps) / abs(prior_year_q_eps) * 100)
    
    return (current_q_eps - prior_year_q_eps) / prior_year_q_eps * 100
```

#### Annual EPS CAGR
```python
def calculate_annual_eps_cagr(eps_list, years=3):
    """
    Calculate Compound Annual Growth Rate for EPS
    eps_list: [oldest_eps, ..., newest_eps]
    """
    if len(eps_list) < years + 1:
        return None
    
    start_eps = eps_list[0]
    end_eps = eps_list[-1]
    
    if start_eps <= 0 or end_eps <= 0:
        return None  # Cannot calculate CAGR with negative values
    
    return ((end_eps / start_eps) ** (1 / years) - 1) * 100
```

### 2. Return on Equity (ROE) Calculation

```python
def calculate_roe(net_income_ttm, shareholder_equity_avg):
    """
    Calculate Return on Equity using average shareholder equity
    """
    if shareholder_equity_avg <= 0:
        return None  # Negative equity situation
    
    return (net_income_ttm / shareholder_equity_avg) * 100

def calculate_dupont_roe(net_income, revenue, assets, equity):
    """
    DuPont Analysis: ROE = Profit Margin × Asset Turnover × Equity Multiplier
    """
    profit_margin = net_income / revenue
    asset_turnover = revenue / assets
    equity_multiplier = assets / equity
    
    return profit_margin * asset_turnover * equity_multiplier * 100
```

### 3. Relative Strength Calculation

```python
def calculate_relative_strength(stock_prices, market_prices, period=252):
    """
    Calculate relative strength rating (1-99 scale)
    period: trading days (252 = 1 year)
    """
    # Calculate returns
    stock_return = (stock_prices[-1] / stock_prices[-period] - 1) * 100
    market_return = (market_prices[-1] / market_prices[-period] - 1) * 100
    
    # Relative performance
    relative_performance = stock_return - market_return
    
    # Convert to percentile ranking (would need universe of stocks)
    # For illustration, using a simplified scoring
    if relative_performance > 20:
        return 90  # Top tier
    elif relative_performance > 10:
        return 80  # Strong
    elif relative_performance > 0:
        return 70  # Above average
    else:
        return 50  # Below average
```

### 4. Supply and Demand Metrics

```python
def calculate_float_impact(shares_outstanding, shares_restricted):
    """
    Calculate float and its impact on volatility
    """
    float_shares = shares_outstanding - shares_restricted
    
    # Float categories
    if float_shares < 10_000_000:
        return "Micro Float - Very High Volatility"
    elif float_shares < 50_000_000:
        return "Small Float - High Volatility"
    elif float_shares < 250_000_000:
        return "Medium Float - Moderate Volatility"
    else:
        return "Large Float - Lower Volatility"

def calculate_buyback_impact(shares_current, shares_year_ago):
    """
    Calculate share buyback percentage
    """
    if shares_year_ago == 0:
        return 0
    
    reduction_pct = (shares_year_ago - shares_current) / shares_year_ago * 100
    return max(0, reduction_pct)  # Only positive values (buybacks)
```

### 5. Institutional Sponsorship Analysis

```python
def analyze_institutional_ownership(inst_holders_count, inst_ownership_pct, 
                                   inst_holders_change_q):
    """
    Comprehensive institutional ownership analysis
    """
    score = 0
    
    # Number of institutions (20-500 optimal)
    if 20 <= inst_holders_count <= 500:
        score += 40
    elif inst_holders_count < 20:
        score += 20  # Too few
    else:
        score += 10  # Too many
    
    # Ownership percentage (10-80% optimal)
    if 10 <= inst_ownership_pct <= 80:
        score += 30
    elif inst_ownership_pct < 10:
        score += 10  # Under-owned
    else:
        score += 5   # Over-owned
    
    # Quarterly change in holders
    if inst_holders_change_q > 5:
        score += 30  # Increasing interest
    elif inst_holders_change_q > 0:
        score += 20  # Stable interest
    else:
        score += 0   # Declining interest
    
    return score  # Max 100
```

## Screening Implementation Examples

### Basic Screen (Python)
```python
def basic_canslim_screen(stock_universe):
    """
    Apply basic CAN SLIM screening criteria
    """
    screened_stocks = []
    
    for stock in stock_universe:
        # Tier 1: Essential Criteria
        if stock.price < 15:
            continue
        if stock.avg_volume < 100000:
            continue
        if stock.exchange not in ['NYSE', 'NASDAQ']:
            continue
        
        q_eps_growth = calculate_quarterly_eps_growth(
            stock.current_q_eps, 
            stock.prior_year_q_eps
        )
        if q_eps_growth < 25:
            continue
        
        # Tier 2: Performance (simplified)
        score = 0
        if stock.annual_eps_cagr >= 25:
            score += 1
        if stock.roe >= 17:
            score += 1
        if stock.price_pct_52w_high >= 90:
            score += 1
        if stock.float_shares < 50_000_000:
            score += 1
        if stock.relative_strength >= 80:
            score += 1
        if 20 <= stock.inst_holders <= 500:
            score += 1
        
        if score >= 4:  # Meet at least 4 of 6
            screened_stocks.append({
                'symbol': stock.symbol,
                'score': score,
                'q_eps_growth': q_eps_growth,
                'roe': stock.roe,
                'rs_rating': stock.relative_strength
            })
    
    # Sort by score
    return sorted(screened_stocks, key=lambda x: x['score'], reverse=True)
```

### Advanced Multi-Factor Screen
```python
def advanced_canslim_screen(stock_universe, market_data):
    """
    Advanced screening with weighted scoring and market conditions
    """
    # Check market condition first
    market_trend = determine_market_trend(market_data)
    if market_trend == 'BEAR':
        return []  # Don't buy in bear markets
    
    candidates = []
    
    for stock in stock_universe:
        # Calculate comprehensive score
        score = {
            'C': score_current_earnings(stock) * 0.20,
            'A': score_annual_earnings(stock) * 0.15,
            'N': score_new_highs(stock) * 0.15,
            'S': score_supply_demand(stock) * 0.10,
            'L': score_leadership(stock) * 0.20,
            'I': score_institutional(stock) * 0.15,
            'M': score_market(market_trend) * 0.05
        }
        
        total_score = sum(score.values())
        
        if total_score >= 0.70:  # 70% threshold
            candidates.append({
                'symbol': stock.symbol,
                'total_score': total_score,
                'breakdown': score,
                'fundamentals': {
                    'eps_growth': stock.q_eps_growth,
                    'roe': stock.roe,
                    'revenue_growth': stock.revenue_growth,
                    'profit_margin': stock.profit_margin
                }
            })
    
    # Rank and return top candidates
    candidates.sort(key=lambda x: x['total_score'], reverse=True)
    return candidates[:20]  # Top 20 stocks
```

## Screening Frequency and Timing

### Optimal Screening Schedule

| Frequency | Purpose | Key Metrics to Update |
|-----------|---------|---------------------|
| **Daily** | Price/Volume monitoring | Price position, Volume, RS Rating |
| **Weekly** | Trend confirmation | Institutional changes, New highs |
| **Monthly** | Portfolio rebalance | Full CAN SLIM scoring |
| **Quarterly** | Earnings updates | EPS growth, Sales growth, Margins |

### Market Condition Adjustments

```python
def adjust_criteria_for_market(base_criteria, market_condition):
    """
    Adjust screening criteria based on market conditions
    """
    if market_condition == 'BULL':
        # More aggressive in bull markets
        return {
            'eps_growth_min': base_criteria['eps_growth_min'] * 0.9,
            'roe_min': base_criteria['roe_min'] * 0.9,
            'rs_rating_min': base_criteria['rs_rating_min'] * 0.95
        }
    elif market_condition == 'BEAR':
        # More conservative in bear markets
        return {
            'eps_growth_min': base_criteria['eps_growth_min'] * 1.2,
            'roe_min': base_criteria['roe_min'] * 1.1,
            'rs_rating_min': base_criteria['rs_rating_min'] * 1.1
        }
    else:  # NEUTRAL
        return base_criteria
```

## Data Sources and APIs

### Required Data Points

1. **Price Data**
   - Current price
   - 52-week high/low
   - Daily volume
   - Price history (1+ years)

2. **Fundamental Data**
   - Quarterly EPS (8 quarters)
   - Annual EPS (5 years)
   - Revenue (quarterly & annual)
   - Balance sheet items
   - Cash flow statements

3. **Ownership Data**
   - Institutional holdings
   - Insider transactions
   - Float shares
   - Share buyback data

### Sample API Integration

```python
class CANSLIMDataProvider:
    """
    Abstract data provider for CAN SLIM screening
    """
    
    def get_earnings_data(self, symbol):
        """Fetch quarterly and annual earnings"""
        pass
    
    def get_price_data(self, symbol, period='2y'):
        """Fetch historical price data"""
        pass
    
    def get_institutional_data(self, symbol):
        """Fetch institutional ownership data"""
        pass
    
    def get_market_data(self, index='SPY'):
        """Fetch market index data for comparison"""
        pass
    
    def calculate_relative_strength(self, symbol):
        """Calculate RS rating vs market"""
        pass
```

## Quality Assurance Checks

### Data Validation Rules

1. **Earnings Consistency**: Check for restatements
2. **Price Continuity**: Detect splits/dividends adjustments
3. **Volume Authenticity**: Filter unusual volume spikes
4. **Institutional Quality**: Verify reported holdings
5. **Market Cap Sanity**: Price × Shares = Market Cap

### Backtesting Framework

```python
def backtest_canslim_strategy(historical_data, start_date, end_date):
    """
    Backtest CAN SLIM strategy with proper controls
    """
    results = {
        'trades': [],
        'returns': [],
        'win_rate': 0,
        'sharpe_ratio': 0
    }
    
    for date in trading_days(start_date, end_date):
        # Point-in-time data (avoid look-ahead bias)
        universe = get_historical_universe(date)
        
        # Apply screening
        candidates = basic_canslim_screen(universe)
        
        # Simulate trades
        for candidate in candidates[:10]:  # Top 10
            entry_price = get_price(candidate, date)
            exit_date = date + timedelta(days=90)  # 3-month hold
            exit_price = get_price(candidate, exit_date)
            
            returns = (exit_price - entry_price) / entry_price
            results['trades'].append({
                'symbol': candidate,
                'entry_date': date,
                'exit_date': exit_date,
                'return': returns
            })
    
    # Calculate metrics
    results['returns'] = [t['return'] for t in results['trades']]
    results['win_rate'] = sum(1 for r in results['returns'] if r > 0) / len(results['returns'])
    results['sharpe_ratio'] = calculate_sharpe(results['returns'])
    
    return results
```