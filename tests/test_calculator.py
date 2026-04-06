"""
Unit tests for DSP ROI Calculator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run: python -m pytest tests/
  or: python tests/test_calculator.py
"""
import sys
import os
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import DSPOperation, SortLeaseConfig, DSPROICalculator


class TestCoreCalculations(unittest.TestCase):

    def _calc(self, volume, staff, wage, hours=8.0):
        op   = DSPOperation(daily_volume=volume, sort_staff=staff, hourly_wage=wage, hours_per_day=hours)
        calc = DSPROICalculator(op)
        return calc.calculate()

    # ── labor cost ──────────────────────────────

    def test_daily_labor_includes_overhead(self):
        """Labor cost must include 1.25x overhead multiplier."""
        r = self._calc(volume=10_000, staff=4, wage=20)
        expected = 4 * 20 * 8 * 1.25  # = 800.0
        self.assertAlmostEqual(r.daily_labor_cost, expected, places=2)

    def test_daily_error_cost(self):
        """Error cost = volume * 3% * $10."""
        r = self._calc(volume=10_000, staff=4, wage=20)
        expected = 10_000 * 0.03 * 10.0  # = 3000.0
        self.assertAlmostEqual(r.daily_error_cost, expected, places=2)

    # ── SortLease cost ───────────────────────────

    def test_sortlease_cost_is_ten_cents_per_parcel(self):
        """SortLease daily cost = volume * $0.10."""
        r = self._calc(volume=10_000, staff=4, wage=20)
        self.assertAlmostEqual(r.daily_sortlease_cost, 1_000.0, places=2)

    def test_annual_sortlease_cost_uses_310_days(self):
        r = self._calc(volume=10_000, staff=4, wage=20)
        self.assertAlmostEqual(r.annual_sortlease_cost, 1_000 * 310, places=0)

    # ── savings ─────────────────────────────────

    def test_high_volume_is_beneficial(self):
        """30,000 parcels/day with 11 staff should clearly be beneficial."""
        r = self._calc(volume=30_000, staff=11, wage=21)
        self.assertTrue(r.is_beneficial)
        self.assertGreater(r.daily_savings, 0)

    def test_very_low_volume_not_beneficial(self):
        """500 parcels/day with 4 staff — manual sorting cheaper."""
        r = self._calc(volume=500, staff=4, wage=18)
        self.assertFalse(r.is_beneficial)

    def test_annual_savings_equals_daily_times_310(self):
        r = self._calc(volume=15_000, staff=8, wage=20)
        self.assertAlmostEqual(r.annual_savings, r.daily_savings * 310, places=0)

    # ── break-even ───────────────────────────────

    def test_breakeven_volume_is_positive(self):
        r = self._calc(volume=10_000, staff=6, wage=18)
        self.assertGreater(r.breakeven_volume, 0)

    def test_at_breakeven_costs_are_approximately_equal(self):
        """At break-even volume, manual cost ≈ SortLease cost (within 5%)."""
        r   = self._calc(volume=10_000, staff=6, wage=18)
        bev = r.breakeven_volume
        r2  = self._calc(volume=bev, staff=6, wage=18)
        ratio = abs(r2.total_daily_manual - r2.daily_sortlease_cost) / r2.total_daily_manual
        self.assertLess(ratio, 0.05)

    # ── payback ─────────────────────────────────

    def test_payback_none_when_not_beneficial(self):
        r = self._calc(volume=500, staff=4, wage=18)
        self.assertIsNone(r.payback_months)

    def test_payback_positive_when_beneficial(self):
        r = self._calc(volume=20_000, staff=9, wage=20)
        if r.is_beneficial:
            self.assertGreater(r.payback_months, 0)

    def test_high_volume_payback_under_12_months(self):
        """Large DSPs should recover the $100K investment in under a year."""
        r = self._calc(volume=30_000, staff=11, wage=21)
        self.assertLess(r.payback_months, 12)

    # ── custom config ────────────────────────────

    def test_custom_sortlease_rate(self):
        """If rate changes, daily cost must update correctly."""
        op  = DSPOperation(daily_volume=10_000, sort_staff=6, hourly_wage=18)
        cfg = SortLeaseConfig(rate_per_parcel=0.08)  # cheaper rate
        r   = DSPROICalculator(op, cfg).calculate()
        self.assertAlmostEqual(r.daily_sortlease_cost, 10_000 * 0.08, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
