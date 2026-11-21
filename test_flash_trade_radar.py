#!/usr/bin/env python3
"""
Unit Tests for Solana Flash Trade Dynamic Backing Pool & Perpetual Risk Radar
"""

import unittest
from flash_trade_radar import (
    calculate_pool_utilization_skew,
    calculate_flb_insolvency_buffer,
    calculate_position_liquidation_boundary,
    calculate_liquidator_flash_fee,
    generate_vip_sentinel_script,
    SOL_RECEIVE_ADDRESS,
    BASE_RECEIVE_ADDRESS
)

class TestFlashTradeRadar(unittest.TestCase):

    def test_pool_utilization_skew(self):
        # Long OI: $6M, Short OI: $2M, Pool TVL: $10M
        # Net skew: +$4M. Skew ratio: 4M / 10M = 40%
        # Utilization: 8M / 10M = 80%
        # Dynamic skew fee: 0.40 * 5.0 = 2.0 bps/hr.
        # Total long cost: 1.0 (base) + 2.0 = 3.0 bps/hr.
        res = calculate_pool_utilization_skew(
            long_oi_usd=6000000.0,
            short_oi_usd=2000000.0,
            pool_tvl_usd=10000000.0,
            base_borrow_fee_bps_hr=1.0
        )
        self.assertEqual(res["net_skew_usd"], 4000000.0)
        self.assertEqual(res["pool_utilization_pct"], 80.0)
        self.assertEqual(res["skew_ratio_pct"], 40.0)
        self.assertEqual(res["dominant_side"], "LONGS_HEAVY")
        self.assertEqual(res["total_long_hourly_cost_bps"], 3.0)

    def test_flb_insolvency_buffer(self):
        # Case 1: Healthy buffer ($5M reserve, $200k trader profit -> $4.8M net reserve = 96% ratio)
        healthy = calculate_flb_insolvency_buffer(5000000.0, 200000.0)
        self.assertTrue(healthy["is_safe"])
        self.assertEqual(healthy["buffer_ratio_pct"], 96.0)
        self.assertEqual(healthy["max_permitted_leverage"], 100.0)
        
        # Case 2: Stressed buffer ($5M reserve, $1M trader profit -> $4M net reserve = 80% ratio)
        stressed = calculate_flb_insolvency_buffer(5000000.0, 1000000.0)
        self.assertFalse(stressed["is_safe"])
        self.assertEqual(stressed["buffer_ratio_pct"], 80.0)
        self.assertEqual(stressed["max_permitted_leverage"], 50.0)

    def test_position_liquidation_boundary(self):
        # 50x Long on SOL @ $140.00. Maintenance margin 1.0% (0.01)
        # Margin reciprocal = 1 / 50 = 0.02 (2.0%)
        # Liq price = 140 * (1 - 0.02 + 0.01) = 140 * 0.99 = $138.60 (1.0% drop)
        long_pos = calculate_position_liquidation_boundary(
            entry_price=140.0,
            leverage=50.0,
            is_long=True,
            maintenance_margin_pct=0.01
        )
        self.assertEqual(long_pos["liquidation_price"], 138.6)
        self.assertEqual(long_pos["distance_to_liq_pct"], 1.0)
        
        # 50x Short on SOL @ $140.00.
        # Liq price = 140 * (1 + 0.02 - 0.01) = 140 * 1.01 = $141.40 (1.0% rise)
        short_pos = calculate_position_liquidation_boundary(
            entry_price=140.0,
            leverage=50.0,
            is_long=False,
            maintenance_margin_pct=0.01
        )
        self.assertEqual(short_pos["liquidation_price"], 141.4)
        self.assertEqual(short_pos["distance_to_liq_pct"], 1.0)

    def test_liquidator_flash_fee(self):
        # Position: $25,000. Fee: 25 bps (0.25%) = $62.50. Jito tip: $0.05 -> Net: $62.45
        fee = calculate_liquidator_flash_fee(
            position_size_usd=25000.0,
            liquidator_fee_bps=25.0,
            jito_tip_usd=0.05,
            sol_price_usd=140.0
        )
        self.assertEqual(fee["gross_reward_usd"], 62.5)
        self.assertEqual(fee["net_reward_usd"], 62.45)
        self.assertTrue(fee["is_profitable"])
        self.assertAlmostEqual(fee["net_reward_sol"], 62.45 / 140.0, places=4)

    def test_generate_vip_script(self):
        script = generate_vip_sentinel_script(SOL_RECEIVE_ADDRESS, BASE_RECEIVE_ADDRESS)
        self.assertIn("Flash Sentinel", script)
        self.assertIn(SOL_RECEIVE_ADDRESS, script)
        self.assertIn(BASE_RECEIVE_ADDRESS, script)
        self.assertIn("@flash-trade/sdk", script)

if __name__ == "__main__":
    unittest.main()
