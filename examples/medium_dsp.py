"""
Example: Medium DSP — 15,000 parcels/day
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Typical profile: Amazon DSP operator or mid-size UPS contractor
running 80-120 delivery routes out of a single station.

Run: python examples/medium_dsp.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import DSPOperation, DSPROICalculator

op = DSPOperation(
    daily_volume  = 15_000,
    sort_staff    = 8,
    hourly_wage   = 20.0,
    hours_per_day = 8.0,
)

calc = DSPROICalculator(op)
calc.print_report()
