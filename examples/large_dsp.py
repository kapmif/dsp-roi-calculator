"""
Example: Large DSP — 30,000 parcels/day
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Typical profile: Large regional carrier or multi-route Amazon
delivery station. Clearest ROI case — payback under 3 months.

Run: python examples/large_dsp.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import DSPOperation, DSPROICalculator

op = DSPOperation(
    daily_volume  = 30_000,
    sort_staff    = 11,
    hourly_wage   = 21.0,
    hours_per_day = 8.0,
)

calc = DSPROICalculator(op)
calc.print_report()
