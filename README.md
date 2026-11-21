# Solana Flash Trade Dynamic Backing Pool (FLB) & Perpetual Risk Radar

[![Python Unit Tests](https://img.shields.io/badge/Unit%20Tests-5%2F5%20Passing-brightgreen.svg)]()
[![Solana](https://img.shields.io/badge/Solana-Mainnet--Beta-blueviolet.svg)]()
[![Flash Trade](https://img.shields.io/badge/Protocol-Flash%20Trade%20Perps-amber.svg)]()
[![Live Visualizer](https://img.shields.io/badge/Live%20Dashboard-GitHub%20Pages-blue.svg)](https://someoneee918.github.io/solana-flash-trade-radar/)

Commercial DeFi intelligence engine analyzing:
1. **Multi-Asset Liquidity Pool (FLP) Long vs Short Open Interest Skew on Solana**
2. **Flash Backup (FLB) Solvency Cushion & Systemic Trader Insolvency Buffer**
3. **High-Leverage (Up to 100x) Exact Liquidation Price Boundaries**
4. **Atomic Liquidator Fee & Jito MEV Tip Clearance Economics**
5. **Non-Custodial VIP Sentinel License Generator (5 Base USDC / 0.03 SOL)**

---

## Live Interactive Dashboard
🌐 **Access the live dashboard at**: [https://someoneee918.github.io/solana-flash-trade-radar/](https://someoneee918.github.io/solana-flash-trade-radar/)

---

## Key Mathematical Models

### 1. FLP Open Interest Skew & Dynamic Borrow Fee
$$\text{Skew}_{ratio} = \frac{\text{Long OI} - \text{Short OI}}{\text{Pool TVL}}$$
$$R_{borrow} = R_{base} + \max(0, \text{Skew}_{ratio} \times 5.0)$$

When long positions dominate the pool, longs pay dynamic hourly skew carry fees to compensate liquidity providers for asymmetric directional risk.

### 2. High-Leverage Liquidation Boundary Precision
For a long position with leverage $L$ and maintenance margin $MM$:
$$P_{liq} = P_{entry} \times \left(1 - \frac{1}{L} + MM\right)$$

For $L = 50.0\text{x}$ and $MM = 1.00\%$:
$$P_{liq} = \$140.00 \times (1 - 0.02 + 0.01) = \$138.60\text{ USD}$$
- Triggered by just a **$1.00\%$ adverse price movement**.

---

## Unit Test Verification
Run the 5/5 unit test suite:
```bash
python3 -m unittest test_flash_trade_radar.py
```

---

## Non-Custodial VIP Sentinel License
Unlock automated TypeScript `@flash-trade/sdk` liquidation sentinels and Jito tip execution scripts by sending **5 Base USDC** or **0.03 SOL** to our verified receive addresses:
- **Solana:** `DW2MdHEq3qZ6nh9b5YFUoaPnBuuxC8Gz2785kwbbjSAM`
- **Base EVM:** `0xF0E0D361bBE899F3089f0a968506eF2B97693c01`
