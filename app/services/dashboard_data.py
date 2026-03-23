"""
Dashboard data service — generates realistic mock metrics and chart data.
Swap the return values here for real DB / API calls without touching the UI.
"""

import random
from datetime import datetime, timedelta


# ── KPI cards (Fundamental Metrics) ────────────────────────────────────────────

def get_kpis() -> dict:
    return {
        "current_ratio":    {"value": round(random.uniform(1.2, 2.8), 2), "delta": round(random.uniform(-0.3, 0.3), 2), "unit": ""},
        "quick_ratio":      {"value": round(random.uniform(0.8, 1.8), 2), "delta": round(random.uniform(-0.2, 0.2), 2), "unit": ""},
        "roe":              {"value": round(random.uniform(8, 22), 1),   "delta": round(random.uniform(-3, 5), 1),   "unit": "%"},
        "asset_turnover":   {"value": round(random.uniform(0.6, 1.6), 2), "delta": round(random.uniform(-0.1, 0.2), 2), "unit": "x"},
    }


# ── Price Trend line chart — last 30 days ──────────────────────────────────────

def get_price_series() -> dict:
    days = [(datetime.today() - timedelta(days=29 - i)).strftime("%d %b") for i in range(30)]
    # Generate realistic price movement with some trend
    base_price = random.uniform(100, 200)
    prices = []
    for i in range(30):
        change = random.uniform(-5, 5) + (i * 0.1)  # Slight upward trend
        base_price = max(50, base_price + change)
        prices.append(round(base_price, 2))

    # Calculate 7-day moving average
    ma = [None] * 6 + [round(sum(prices[i-6:i+1]) / 7, 2) for i in range(6, 30)]

    return {"days": days, "price": prices, "ma": ma}


# ── Sector Allocation donut ────────────────────────────────────────────────────

def get_sector_allocation() -> list[dict]:
    tech     = random.randint(25, 40)
    finance  = random.randint(15, 25)
    healthcare = random.randint(10, 20)
    energy   = random.randint(8, 15)
    consumer = 100 - tech - finance - healthcare - energy
    return [
        {"name": "Technology", "value": tech},
        {"name": "Finance",    "value": finance},
        {"name": "Healthcare", "value": healthcare},
        {"name": "Energy",     "value": energy},
        {"name": "Consumer",   "value": consumer},
    ]


# ── Volume Analysis bar — last 7 trading days ───────────────────────────────────

def get_volume_analysis() -> dict:
    days = [(datetime.today() - timedelta(days=6 - i)).strftime("%a") for i in range(7)]
    buy_volume  = [random.randint(150, 400) for _ in range(7)]
    sell_volume = [random.randint(100, 300) for _ in range(7)]
    return {"days": days, "buy_volume": buy_volume, "sell_volume": sell_volume}


# ── RSI Indicator area — last 24 periods ────────────────────────────────────────

def get_rsi_series() -> dict:
    periods = [f"T{i}" for i in range(1, 25)]
    rsi = [round(random.uniform(35, 75), 1) for _ in range(24)]
    overbought = [70] * 24
    oversold = [30] * 24
    return {"periods": periods, "rsi": rsi, "overbought": overbought, "oversold": oversold}