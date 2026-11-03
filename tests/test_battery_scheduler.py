"""Verification cases from blueprint Section 4.3. Run: python -m unittest -v"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from battery_scheduler import (  # noqa: E402
    BatteryParams, simulate, exact_schedule, baseline_no_battery,
)

DEMAND = [1.0, 1.0, 1.0, 1.0]


class TestSimulator(unittest.TestCase):
    def test_zero_battery_activity(self):
        p = BatteryParams()
        solar = [0.0, 0.5, 2.0, 0.0]
        tariff = [0.2, 0.2, 0.3, 0.3]
        tr = simulate((0, 0, 0, 0), DEMAND, solar, tariff, p)
        expected = 0.2 * 1.0 + 0.2 * 0.5 + 0.3 * 0.0 + 0.3 * 1.0
        self.assertTrue(tr.feasible)
        self.assertAlmostEqual(tr.cost, expected)
        self.assertEqual(tr.energy, [2.5] * 5)
        self.assertAlmostEqual(tr.curtailment[2], 1.0)  # 2.0 solar, 1.0 used

    def test_zero_solar_import_equals_net_load(self):
        p = BatteryParams(terminal_min_kwh=None)
        tr = simulate((1, 0, -1, 0), DEMAND, [0] * 4, [0.1] * 4, p)
        self.assertEqual(tr.grid_import, [2.0, 1.0, 0.0, 1.0])

    def test_battery_upper_bound(self):
        p = BatteryParams(initial_kwh=5.0, terminal_min_kwh=None)
        tr = simulate((1, 0, 0, 0), DEMAND, [0] * 4, [0.1] * 4, p)
        self.assertFalse(tr.feasible)
        self.assertIn("bound", tr.reason)

    def test_battery_lower_bound(self):
        p = BatteryParams(initial_kwh=0.5, terminal_min_kwh=None)
        tr = simulate((-1, 0, 0, 0), [2.0] * 4, [0] * 4, [0.1] * 4, p)
        self.assertFalse(tr.feasible)

    def test_export_disabled_in_planning(self):
        p = BatteryParams(terminal_min_kwh=None)
        tr = simulate((-2, 0, 0, 0), [1.0] * 4, [0] * 4, [0.1] * 4, p)
        self.assertFalse(tr.feasible)
        self.assertIn("export", tr.reason)

    def test_manual_energy_balance(self):
        """Hand calculation, eta = 0.9, E0 = 2.0 kWh, no terminal rule.
        t0 charge 2: E=2+1.8=3.8, import=1+2-0=3, cost 0.1*3=0.3
        t1 idle:     import=1, cost 0.1
        t2 discharge 1 with 2 kW solar: net=0, import=0, curtail=2,
                     E=3.8-1/0.9=2.68889
        t3 idle:     import=1, cost 0.3     total = 0.7
        """
        p = BatteryParams(initial_kwh=2.0, eta_charge=0.9, eta_discharge=0.9,
                          terminal_min_kwh=None)
        tr = simulate((2, 0, -1, 0), DEMAND, [0, 0, 2, 0], [0.1, 0.1, 0.3, 0.3], p)
        self.assertTrue(tr.feasible)
        self.assertAlmostEqual(tr.energy[1], 3.8)
        self.assertAlmostEqual(tr.energy[3], 3.8 - 1 / 0.9)
        self.assertEqual(tr.grid_import, [3.0, 1.0, 0.0, 1.0])
        self.assertAlmostEqual(tr.curtailment[2], 2.0)
        self.assertAlmostEqual(tr.cost, 0.7)
        self.assertAlmostEqual(tr.throughput_kwh, 3.0)

    def test_execution_clips_discharge_under_forecast_error(self):
        p = BatteryParams(terminal_min_kwh=None)
        # planned for demand 1.0 (discharge 1 is fine); actual demand is 0.4
        tr = simulate((-1, 0, 0, 0), [0.4, 1, 1, 1], [0] * 4, [0.1] * 4, p, strict=False)
        self.assertAlmostEqual(tr.discharge_clipped_kwh, 0.6)
        self.assertAlmostEqual(tr.grid_import[0], 0.0)
        self.assertAlmostEqual(tr.energy[1], 2.5 - 0.4 / 0.95)


class TestExactScheduler(unittest.TestCase):
    def test_enumeration_count(self):
        p = BatteryParams()
        _, n_total, n_feas = exact_schedule(DEMAND, [0] * 4, [0.1] * 4, p)
        self.assertEqual(n_total, 5 ** 4)
        self.assertGreater(n_feas, 0)

    def test_flat_prices_optimum_is_do_nothing(self):
        """Round-trip losses mean cycling cannot help when prices are flat."""
        p = BatteryParams()
        best, _, _ = exact_schedule(DEMAND, [0] * 4, [0.25] * 4, p)
        base = baseline_no_battery(DEMAND, [0] * 4, [0.25] * 4, p)
        self.assertAlmostEqual(best.cost, base.cost)
        self.assertEqual(best.actions, (0.0, 0.0, 0.0, 0.0))

    def test_cheap_then_expensive_shifts_energy(self):
        p = BatteryParams()
        tariff = [0.10, 0.10, 0.40, 0.40]
        best, _, _ = exact_schedule(DEMAND, [0] * 4, tariff, p)
        base = baseline_no_battery(DEMAND, [0] * 4, tariff, p)
        self.assertLess(best.cost, base.cost)
        self.assertTrue(any(a > 0 for a in best.actions[:2]))   # charges cheap
        self.assertTrue(any(a < 0 for a in best.actions[2:]))   # discharges dear

    def test_terminal_rule_prevents_emptying_battery(self):
        tariff = [0.10, 0.40, 0.40, 0.40]
        with_rule = BatteryParams(terminal_min_kwh=2.5)
        no_rule = BatteryParams(terminal_min_kwh=None)
        a, _, _ = exact_schedule(DEMAND, [0] * 4, tariff, with_rule)
        b, _, _ = exact_schedule(DEMAND, [0] * 4, tariff, no_rule)
        self.assertGreaterEqual(a.energy[-1], 2.5 - 1e-9)
        self.assertLess(b.energy[-1], 2.5)       # unconstrained empties it
        self.assertLess(b.cost, a.cost)          # ...and "saves" artificially

    def test_returned_optimum_is_feasible_and_cost_consistent(self):
        p = BatteryParams()
        solar = [0.0, 1.5, 2.5, 0.5]
        tariff = [0.12, 0.15, 0.30, 0.35]
        best, _, _ = exact_schedule(DEMAND, solar, tariff, p)
        re = simulate(best.actions, DEMAND, solar, tariff, p)
        self.assertTrue(re.feasible)
        self.assertAlmostEqual(re.cost, best.cost)

    def test_optimum_not_beaten_by_any_feasible_schedule(self):
        from itertools import product
        p = BatteryParams()
        solar = [0.0, 1.0, 2.0, 0.0]
        tariff = [0.10, 0.20, 0.35, 0.30]
        best, _, _ = exact_schedule(DEMAND, solar, tariff, p)
        for s in product(p.actions_kw, repeat=4):
            tr = simulate(s, DEMAND, solar, tariff, p)
            if tr.feasible:
                self.assertGreaterEqual(tr.cost, best.cost - 1e-9)

    def test_infeasible_instance_returns_none(self):
        p = BatteryParams(initial_kwh=0.5, terminal_min_kwh=5.0,
                          actions_kw=(0.0,))
        best, n_total, n_feas = exact_schedule(DEMAND, [0] * 4, [0.1] * 4, p)
        self.assertIsNone(best)
        self.assertEqual(n_feas, 0)


if __name__ == "__main__":
    unittest.main()
