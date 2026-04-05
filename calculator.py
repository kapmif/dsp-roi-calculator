#!/usr/bin/env python3
"""
DSP Parcel Sorting ROI Calculator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Open-source ROI model for Delivery Service Providers (DSPs)
evaluating automated parcel sorting vs manual operations.

Built from real deployment data at SortLease.com
GitHub:  https://github.com/kapmif/dsp-roi-calculator
License: MIT
Python:  3.8+ — zero external dependencies
"""

from dataclasses import dataclass, field
from typing import Optional
import sys


# ────────────────────────────────────────────────
#  DATA CLASSES
# ────────────────────────────────────────────────

@dataclass
class DSPOperation:
    """Describes a DSP sorting operation."""
    daily_volume: int           # parcels per operating day
    sort_staff: int             # sorting headcount
    hourly_wage: float          # average USD/hour
    hours_per_day: float = 8.0
    days_per_year: int = 310    # ~310 operating days after holidays
    error_rate: float = 0.03    # mis-sort rate — 3% industry average
    error_cost: float = 10.0   # USD per corrected mis-sort
    overhead_multiplier: float = 1.25  # benefits + mgmt overhead on labor


@dataclass
class SortLeaseConfig:
    """SortLease pricing and investment configuration."""
    rate_per_parcel: float = 0.10        # $0.10 per parcel
    station_investment: float = 100_000  # $100K per installed station
    gross_margin: float = 0.83           # 83% gross margin


@dataclass
class ROIResult:
    """Complete ROI analysis output."""
    # Manual costs
    daily_labor_cost: float
    daily_error_cost: float
    total_daily_manual: float
    annual_manual_cost: float

    # SortLease costs
    daily_sortlease_cost: float
    annual_sortlease_cost: float

    # Savings
    daily_savings: float
    monthly_savings: float
    annual_savings: float

    # ROI
    payback_months: Optional[float]
    five_year_net: float
    roi_5yr_pct: float

    # Break-even
    breakeven_volume: int
    pct_above_breakeven: Optional[float]
    is_beneficial: bool


# ────────────────────────────────────────────────
#  CORE CALCULATOR CLASS
# ────────────────────────────────────────────────

class DSPROICalculator:
    """
    Calculate ROI for a DSP switching from manual sorting
    to SortLease's pay-per-parcel model.

    Usage:
        op   = DSPOperation(daily_volume=15000, sort_staff=8, hourly_wage=20)
        calc = DSPROICalculator(op)
        result = calc.calculate()
        calc.print_report(result)
    """

    def __init__(
        self,
        operation: DSPOperation,
        config: SortLeaseConfig = None,
    ):
        self.op = operation
        self.cfg = config or SortLeaseConfig()

    # ── main calculation ────────────────────────

    def calculate(self) -> ROIResult:
        op  = self.op
        cfg = self.cfg

        # Manual costs
        base_labor    = op.sort_staff * op.hourly_wage * op.hours_per_day
        daily_labor   = base_labor * op.overhead_multiplier
        daily_errors  = op.daily_volume * op.error_rate * op.error_cost
        total_manual  = daily_labor + daily_errors
        annual_manual = total_manual * op.days_per_year

        # SortLease costs
        daily_sl   = op.daily_volume * cfg.rate_per_parcel
        annual_sl  = daily_sl * op.days_per_year

        # Savings
        daily_savings   = total_manual - daily_sl
        monthly_savings = daily_savings * 30
        annual_savings  = daily_savings * op.days_per_year

        # ROI
        if daily_savings > 0:
            payback = cfg.station_investment / (daily_savings * 30)
        else:
            payback = None

        five_year_net = (annual_savings * 5) - cfg.station_investment
        roi_5yr = (five_year_net / cfg.station_investment * 100) if daily_savings > 0 else -100.0

        # Break-even volume
        # Solve:  volume * sl_rate  =  fixed_labor + volume * error_rate * error_cost
        variable_saving = cfg.rate_per_parcel - (op.error_rate * op.error_cost)
        if variable_saving > 0:
            breakeven = int(daily_labor / variable_saving)
        else:
            breakeven = 9_999_999  # never breaks even

        if daily_savings > 0 and breakeven > 0:
            pct_above = (op.daily_volume - breakeven) / breakeven * 100
        else:
            pct_above = None

        return ROIResult(
            daily_labor_cost      = daily_labor,
            daily_error_cost      = daily_errors,
            total_daily_manual    = total_manual,
            annual_manual_cost    = annual_manual,
            daily_sortlease_cost  = daily_sl,
            annual_sortlease_cost = annual_sl,
            daily_savings         = daily_savings,
            monthly_savings       = monthly_savings,
            annual_savings        = annual_savings,
            payback_months        = payback,
            five_year_net         = five_year_net,
            roi_5yr_pct           = roi_5yr,
            breakeven_volume      = breakeven,
            pct_above_breakeven   = pct_above,
            is_beneficial         = daily_savings > 0,
        )

    # ── formatted report ────────────────────────

    def print_report(self, result: ROIResult = None) -> None:
        """Print a full formatted ROI report to stdout."""
        if result is None:
            result = self.calculate()

        op = self.op
        r  = result
        W  = 56   # line width

        def line(label="", value="", color=""):
            if not label:
                print()
                return
            print(f"  {label:<34}{value:>18}")

        print()
        print("═" * W)
        print("  📦  DSP PARCEL SORTING ROI ANALYSIS")
        print("═" * W)

        print("\n  OPERATION PROFILE")
        line("Daily parcel volume:", f"{op.daily_volume:,}")
        line("Sorting staff:", f"{op.sort_staff}")
        line("Average hourly wage:", f"${op.hourly_wage:,.2f}")
        line("Operating hours/day:", f"{op.hours_per_day:.1f}")

        print("\n  CURRENT MANUAL SORTING COSTS")
        line("Daily labor cost (w/ overhead):", f"${r.daily_labor_cost:,.2f}")
        line("Daily error correction cost:", f"${r.daily_error_cost:,.2f}")
        line("Total daily manual cost:", f"${r.total_daily_manual:,.2f}")
        line("Annual manual cost:", f"${r.annual_manual_cost:,.0f}")

        print(f"\n  SORTLEASE PAY-PER-PARCEL ($0.10/parcel)")
        line("Daily SortLease cost:", f"${r.daily_sortlease_cost:,.2f}")
        line("Annual SortLease cost:", f"${r.annual_sortlease_cost:,.0f}")

        print("\n  SAVINGS ANALYSIS")
        if r.is_beneficial:
            line("Daily savings:", f"${r.daily_savings:,.2f}  ✅")
            line("Monthly savings:", f"${r.monthly_savings:,.0f}")
            line("Annual savings:", f"${r.annual_savings:,.0f}")
        else:
            line("Daily net position:", f"${r.daily_savings:,.2f}  ⚠️")
            print("  Manual sorting cheaper at this volume.")

        print("\n  ROI METRICS")
        if r.payback_months and r.payback_months < 120:
            emoji = "🚀" if r.payback_months < 9 else "✅"
            line("Station investment:", "$100,000")
            line("Payback period:", f"{r.payback_months:.1f} months  {emoji}")
            line("5-year net benefit:", f"${r.five_year_net:,.0f}")
            line("5-year ROI:", f"{r.roi_5yr_pct:.0f}%")
        else:
            print("  Not recommended at current volume.")
            print(f"  Consider deploying at {r.breakeven_volume:,}+ parcels/day.")

        print("\n  BREAK-EVEN ANALYSIS")
        line("Break-even daily volume:", f"{r.breakeven_volume:,}")
        if r.pct_above_breakeven is not None:
            emoji = "🚀" if r.pct_above_breakeven > 50 else "✅"
            line("Your volume above break-even:", f"{r.pct_above_breakeven:.0f}%  {emoji}")
        elif not r.is_beneficial:
            gap = r.breakeven_volume - op.daily_volume
            pct = gap / r.breakeven_volume * 100
            line("Volume below break-even by:", f"{pct:.0f}%")

        print()
        print("═" * W)
        if r.is_beneficial:
            print("  ✅  RECOMMENDATION: SortLease is cost-effective")
            print("      sortlease.com  |  (406) 479-0215")
        else:
            print(f"  💡  Evaluate at {r.breakeven_volume:,}+ parcels/day")
            print("      sortlease.com  |  (406) 479-0215")
        print("═" * W)
        print()


# ────────────────────────────────────────────────
#  BATCH MARKET ANALYSIS
# ────────────────────────────────────────────────

def market_analysis() -> None:
    """
    Run the ROI model across all US DSP segments.
    Shows a table: volume × savings × payback × ROI.
    """
    segments = [
        {
            "label": "SMALL DSPs  —  3K–8K parcels/day  |  4 staff  |  $17/hr",
            "volumes": range(3_000, 9_000, 1_000),
            "staff": 4, "wage": 17.0,
        },
        {
            "label": "MEDIUM DSPs  —  8K–20K parcels/day  |  7 staff  |  $19/hr",
            "volumes": range(8_000, 22_000, 2_000),
            "staff": 7, "wage": 19.0,
        },
        {
            "label": "LARGE DSPs  —  20K–35K parcels/day  |  11 staff  |  $21/hr",
            "volumes": range(20_000, 36_000, 5_000),
            "staff": 11, "wage": 21.0,
        },
    ]

    print("\n📊  US DSP MARKET SEGMENT ANALYSIS")
    print("    SortLease ROI by operation size\n")

    hdr = f"  {'Volume':>8}  {'Daily Save':>10}  {'Annual Save':>12}  {'Payback':>9}  {'5yr ROI':>8}  {'Status':>6}"

    for seg in segments:
        print("─" * 62)
        print(f"  {seg['label']}")
        print("─" * 62)
        print(hdr)
        print("  " + "─" * 60)

        for vol in seg["volumes"]:
            op   = DSPOperation(daily_volume=vol, sort_staff=seg["staff"], hourly_wage=seg["wage"])
            calc = DSPROICalculator(op)
            r    = calc.calculate()

            if r.is_beneficial and r.payback_months:
                flag = "🚀" if r.payback_months < 9 else "✅"
                print(
                    f"  {vol:>8,}  "
                    f"${r.daily_savings:>9,.0f}  "
                    f"${r.annual_savings:>11,.0f}  "
                    f"{r.payback_months:>7.1f}mo  "
                    f"{r.roi_5yr_pct:>7.0f}%  "
                    f"{flag}"
                )
            else:
                print(f"  {vol:>8,}  {'— not viable —':>43}")

        print()


# ────────────────────────────────────────────────
#  INTERACTIVE MODE
# ────────────────────────────────────────────────

def interactive() -> None:
    """Ask for inputs and print a full report."""
    print("\n🔢  DSP Parcel Sorting ROI Calculator")
    print("    github.com/kapmif/dsp-roi-calculator\n")

    try:
        volume = int(input("  Enter daily parcel volume: ").strip())
        staff  = int(input("  Enter number of sorting staff: ").strip())
        wage   = float(input("  Enter average hourly wage ($): ").strip())
        hours_input = input("  Enter operating hours per day [8]: ").strip()
        hours  = float(hours_input) if hours_input else 8.0

        op   = DSPOperation(daily_volume=volume, sort_staff=staff, hourly_wage=wage, hours_per_day=hours)
        calc = DSPROICalculator(op)
        calc.print_report()

    except ValueError:
        print("\n  ⚠️  Please enter valid numbers.\n")
    except KeyboardInterrupt:
        print("\n  Exited.\n")


# ────────────────────────────────────────────────
#  ENTRY POINT
# ────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--market":
        market_analysis()
    else:
        interactive()
