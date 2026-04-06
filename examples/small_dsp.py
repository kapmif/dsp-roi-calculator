"""
Example: Small DSP — 5,000 parcels/day
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Typical profile: FedEx Ground contractor or regional courier
running a single sort facility with 4 sorting staff.

Run: python examples/small_dsp.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import DSPOperation, DSPROICalculator

op = DSPOperation(
    daily_volume  = 5_000,
    sort_staff    = 4,
    hourly_wage   = 17.0,
    hours_per_day = 8.0,
)

calc = DSPROICalculator(op)
calc.print_report()
