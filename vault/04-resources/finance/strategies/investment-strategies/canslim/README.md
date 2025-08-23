# CAN SLIM Investment Strategy Research

## Overview

Comprehensive research and analysis of William O'Neil's CAN SLIM investment methodology, explained through first principles and Feynman techniques.

## Repository Structure

```
canslim/
├── README.md                           # This file
├── comprehensive-guide.md              # Complete first-principles analysis
├── fundamentals/
│   └── theory-and-examples.md         # Theoretical foundations & case studies
├── screening/
│   └── screening-criteria.md          # Technical screening specifications
└── implementation/
    └── practical-strategies.md        # Real-world implementation guide
```

## The CAN SLIM Framework

**C** - Current Quarterly Earnings (>25% growth)  
**A** - Annual Earnings Increases (>25% CAGR, ROE >17%)  
**N** - New (Products, Management, Price Highs)  
**S** - Supply and Demand (Small float, buybacks)  
**L** - Leader or Laggard (RS Rating >80)  
**I** - Institutional Sponsorship (20-500 holders)  
**M** - Market Direction (Trade with the trend)

## Quick Start Guide

1. **Understand the Theory**: Start with `comprehensive-guide.md` for first-principles understanding
2. **Learn the Criteria**: Review `screening/screening-criteria.md` for specific parameters
3. **Study Examples**: Examine `fundamentals/theory-and-examples.md` for historical cases
4. **Implement**: Follow `implementation/practical-strategies.md` for practical application

## Key Insights

### First Principle: Business Momentum
Stock prices ultimately reflect business performance. Companies with accelerating earnings tend to continue accelerating (Newton's First Law applied to business).

### The Mathematics
```
Future Price = Current Price × (1 + growth_rate)^time × Multiple_Expansion
```

### Risk Management
- Maximum 7-8% loss per position
- Position size: 1-2% portfolio risk
- Total portfolio heat: <6% at any time

## Core Screening Formula

```python
def canslim_score(stock):
    return (
        earnings_score * 0.25 +     # C & A factors
        technical_score * 0.25 +    # N factor (new highs)
        momentum_score * 0.20 +     # L factor (leadership)
        fundamental_score * 0.20 +  # Quality metrics
        institutional_score * 0.10  # I factor
    )
```

## Historical Performance Examples

| Stock | Period | Entry | Exit | Return | Key Success Factor |
|-------|--------|-------|------|--------|-------------------|
| AAPL | 2004-07 | $8.50 | $28 | 229% | iPod/iPhone innovation |
| MNST | 2003-06 | $5.25 | $31 | 490% | Energy drink revolution |
| NFLX | 2009-11 | $7 | $42 | 500%+ | Streaming transformation |

## Implementation Checklist

- [ ] Set up screening tools with CAN SLIM criteria
- [ ] Create watchlist of 20-30 candidates
- [ ] Perform 10-point research on top 5
- [ ] Paper trade for 30 days minimum
- [ ] Start with 10% capital allocation
- [ ] Maintain trading journal
- [ ] Review performance weekly
- [ ] Adjust parameters quarterly

## Critical Warnings

1. **Very few stocks meet all criteria** - Be selective
2. **Stop losses are mandatory** - No exceptions
3. **Market timing matters** - Don't fight the trend
4. **Psychology is crucial** - Control emotions
5. **Continuous learning required** - Markets evolve

## Advanced Concepts

- **Power Law Distribution**: 4% of stocks drive 80% of returns
- **Reflexivity**: Price influences fundamentals which influence price
- **Information Cascades**: How momentum becomes self-reinforcing
- **Network Effects**: Value = n² (where n = believers)

## The Ultimate Principle

> "The whole secret to winning in the stock market is to lose the least amount possible when you're not right." - William O'Neil

Success with CAN SLIM requires:
1. **Discipline** to follow the system
2. **Patience** to wait for setups
3. **Courage** to buy strength
4. **Humility** to take losses quickly

## Resources

- **Book**: "How to Make Money in Stocks" by William O'Neil
- **Website**: investors.com (IBD)
- **Tools**: Stock screeners with fundamental + technical filters
- **Practice**: Paper trading platforms

## Research Methodology

This research employs:
- **First Principles Thinking**: Breaking down complex concepts to fundamentals
- **Feynman Technique**: Explaining concepts simply as if teaching a child
- **Historical Analysis**: Learning from past successes and failures
- **Mathematical Framework**: Quantifying the qualitative aspects

---

*Research compiled from Portfolio123 blog analysis and extensive market study*  
*Last Updated: 2024*