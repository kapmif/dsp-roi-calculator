# 📦 DSP Parcel Sorting ROI Calculator

> Open-source ROI calculator for last-mile delivery companies evaluating automated parcel sorting.  
> Built from real deployment data at [SortLease](https://www.sortlease.com) — the first pay-per-parcel sorting network for US DSPs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![HN Discussion](https://img.shields.io/badge/Hacker%20News-Discuss-orange.svg)](https://news.ycombinator.com)

---

## 🎯 The Problem This Solves

**5,000+ small US Delivery Service Partners (DSPs) are trapped in manual parcel sorting.**

Large carriers — Amazon, FedEx, UPS — have invested billions automating their sort hubs.  
The 5,000+ small DSPs operating **5,000–30,000 parcels/day** have zero affordable options.

| Pain Point | Real Cost |
|---|---|
| Manual sorting labor | $15–20/hr × 4–8 workers per shift |
| Mis-sort error rate | $8–12 per corrected package (industry avg: 3%) |
| Morning bottleneck 5:30–7 AM | 15–20% daily delivery capacity lost |
| Wage inflation | +25% since 2020 |
| Volume growth | +15–20%/year — manual cannot scale |

Legacy automation vendors (Vanderlande, Dematic, Siemens Logistics) require **$500K–$2M upfront** — completely out of reach for the DSP segment.

---

## 💡 The Pay-Per-Parcel Approach

[SortLease](https://www.sortlease.com) installs complete AI sorting systems at **zero capital cost** to DSP operators, then charges **$0.10 per sorted parcel**.

```
Manual sorting cost:    $0.22 – $0.30 per parcel
SortLease cost:         $0.10 per parcel
────────────────────────────────────────
Operator savings:       67% cost reduction
```

This calculator lets any DSP (or investor) model the exact economics for their specific operation.

---

## 🚀 Quick Start

```bash
git clone https://github.com/kapmif/dsp-roi-calculator.git
cd dsp-roi-calculator

# Pure Python standard library — nothing to install
python calculator.py
```

**No Git?** Just copy-paste `calculator.py` into any Python 3 environment and run it.

### Sample interactive session

```
🔢  DSP Parcel Sorting ROI Calculator
    github.com/kapmif/dsp-roi-calculator

  Enter daily parcel volume: 15000
  Enter number of sorting staff: 8
  Enter average hourly wage ($): 20
  Enter operating hours per day [8]: 8

════════════════════════════════════════════════════════
  📦  DSP PARCEL SORTING ROI ANALYSIS
════════════════════════════════════════════════════════

  OPERATION PROFILE
  Daily parcel volume:                  15,000
  Sorting staff:                             8
  Average hourly wage:                  $20.00

  CURRENT MANUAL SORTING COSTS
  Daily labor cost (w/ overhead):    $1,600.00
  Daily error correction cost:         $450.00
  Total daily manual cost:           $2,050.00
  Annual manual cost:               $635,500

  SORTLEASE PAY-PER-PARCEL ($0.10/parcel)
  Daily SortLease cost:              $1,500.00
  Annual SortLease cost:            $465,000

  SAVINGS ANALYSIS
  Daily savings:                       $550.00  ✅
  Monthly savings:                   $16,500
  Annual savings:                   $170,500

  ROI METRICS
  Station investment:               $100,000
  Payback period:                       6.1 months  🚀
  5-year net benefit:               $752,500
  5-year ROI:                            753%

  BREAK-EVEN ANALYSIS
  Break-even daily volume:              8,800
  Your volume above break-even:            70%  🚀

════════════════════════════════════════════════════════
  ✅  RECOMMENDATION: SortLease is cost-effective
      sortlease.com  |  (406) 479-0215
════════════════════════════════════════════════════════
```

### Batch market analysis

```bash
python calculator.py --market
```

Runs the model across the full small/medium/large DSP segment range.

---

## 📐 Formula & Assumptions

### Input parameters

| Parameter | Default | Description |
|---|---|---|
| `daily_volume` | required | Parcels sorted per day |
| `sort_staff` | required | Sorting headcount |
| `hourly_wage` | required | Average USD/hr |
| `hours_per_day` | 8.0 | Daily sorting window |
| `days_per_year` | 310 | Excluding holidays |
| `error_rate` | 0.03 | Mis-sort rate (3% avg) |
| `error_cost` | $10 | Per corrected package |
| `overhead_multiplier` | 1.25 | Benefits + mgmt overhead |
| `sortlease_rate` | $0.10 | Pay-per-parcel charge |
| `station_investment` | $100,000 | Capital per station |

### Core math

```python
# Manual sorting cost per day
daily_labor  = sort_staff × hourly_wage × hours × overhead_multiplier
daily_errors = daily_volume × error_rate × error_cost
total_manual = daily_labor + daily_errors

# SortLease cost per day
daily_sl     = daily_volume × 0.10

# Net savings per day
savings      = total_manual - daily_sl

# Break-even volume
breakeven    = daily_labor / (0.10 - error_rate × error_cost)

# Payback period (months)
payback      = station_investment / (savings × 30)
```

### Known simplifications / open issues

- Model assumes steady throughput; real savings vary by shift pattern
- Error cost of $10 is industry average — range is $8–$12
- Does not model electricity, insurance (included in SortLease's $0.10)
- Volume growth not projected — compounding savings are larger in reality

Open an issue if your numbers look off. We want this accurate.

---

## 📊 Real Unit Economics (SortLease seed round data)

```
Per-station investment:        $100,000
Target volume per station:     10,000 – 30,000 parcels/day
Revenue @ $0.10/parcel:        $1,000 – $3,000/day
Monthly gross revenue:         $30,000 – $90,000
Gross margin:                  83%
Station payback:               ~6 months
Annual gross profit/station:   $300K – $900K
```

**50-station network ($5M seed round target):**

```
Total investment:        $5,000,000
Annual gross revenue:    $54,750,000
Annual gross profit:     $45,000,000
Network gross margin:    83%
```

---

## 📁 Repository Structure

```
dsp-roi-calculator/
├── README.md                  ← You are here
├── calculator.py              ← Python CLI (zero dependencies)
├── calculator.js              ← Node.js / browser version
├── calculator.html            ← Standalone browser app (just open it)
├── data/
│   └── us-dsp-market.json     ← US DSP market dataset
├── examples/
│   ├── small_dsp.py           ← 5,000 parcels/day scenario
│   ├── medium_dsp.py          ← 15,000 parcels/day scenario
│   └── large_dsp.py           ← 30,000 parcels/day scenario
└── tests/
    └── test_calculator.py     ← Unit tests
```

---

## 🌐 Market Data

Numbers driving this model:

| Metric | Value | Source |
|---|---|---|
| US last-mile market (2024) | $168.74B | GlobeNewsWire 2025 |
| US last-mile market (2031) | $303.59B | GlobeNewsWire 2025 |
| CAGR | 8.8% | GlobeNewsWire 2025 |
| US DSPs without automation | 5,000+ | Industry estimate |
| Warehouse wage increase (2020–2024) | +25% | BLS data |
| Annual sorting staff turnover | 40% | Industry surveys |
| Legacy automation entry price | $500K–$2M | Vendor pricing |
| SortLease capital cost to operator | $0 | SortLease model |

---

## 🏗️ Engineering Notes (for contributors)

SortLease's actual production architecture — discussed openly:

```
IoT Layer:        QR scanner → MQTT → AWS IoT Core
AI Engine:        Computer vision (parcel ID + routing) → real-time decision
Billing Layer:    $0.10/parcel metered → Stripe / carrier payment API
Analytics:        Throughput dashboard → PostgreSQL + Grafana  
REST API:         Carrier system integration (FedEx, UPS, Amazon DSP)
Throughput:       3,500–21,000 parcels/hour per FlowSort S15 station
```

**Interesting open engineering problems:**

1. Real-time parcel routing at sub-100ms decision latency
2. QR-based driver lane assignment (target: < 10 seconds end-to-end)
3. Metered billing integration with carrier payment systems
4. Multi-tenant analytics (multiple DSPs sharing one hub)
5. Predictive maintenance on 70%-fewer-moving-parts hardware

If you're working on IoT, logistics tech, real-time billing, or computer vision in the warehouse space — [we want to talk](https://www.sortlease.com/join-the-mission/).

---

## 🤝 Contributing

Pull requests welcome. This is a real operational problem with real messy data.

**Good first contributions:**

- Sensitivity analysis: what if wages rise 5%/yr?
- Volume growth projection: compounding savings over 5 years
- Better break-even chart in the browser version
- International market data: EU, UK, APAC DSP segments
- Anything that looks wrong — open an issue first

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 💜 About SortLease

SortLease is building the **first pay-per-parcel sorting network** for US Delivery Service Partners.

- **Product:** FlowSort S15 — 21,000 parcels/hr · 99.9% AI accuracy · 2,000 sq ft
- **Model:** $0.10/parcel (vs $0.22–$0.30 manual) · zero CAPEX to operators
- **Stage:** Seed round open · $5M target · 83% gross margin · ~6-month payback/station
- **Hiring:** CEO, Backend Engineer, IoT Engineer → [join-the-mission](https://www.sortlease.com/join-the-mission/)
- **Investing:** Accredited investors → [angel-investment](https://www.sortlease.com/angel-investment/)

| Contact | |
|---|---|
| 🌐 | [sortlease.com](https://www.sortlease.com) |
| 📧 | [info@sortlease.com](mailto:info@sortlease.com) |
| 📞 | [(406) 479-0215](tel:+14064790215) |
| 💬 | [WhatsApp](https://wa.me/14064790215?text=Hi!%20Found%20the%20DSP%20ROI%20calculator%20on%20GitHub.) |

---

## 📄 License

MIT — free to use, attribution appreciated.

---

*Numbers look wrong for your operation? Open an issue — we want this to reflect reality.*
