from __future__ import annotations

import os
import numpy as np
import pandas as pd


def load_finlab_data(symbols: list[str], periods: int = 260) -> pd.DataFrame:
    """載入價格資料。

    實務上可替換為 FinLab API。
    目前以隨機漫步產生範例資料。
    """
    _ = os.getenv("FINLAB_API_TOKEN", "")

    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=periods)
    rows = []
    rng = np.random.default_rng(42)

    for sym in symbols:
        rets = rng.normal(0.0005, 0.02, size=periods)
        close = 100 * np.cumprod(1 + rets)
        df = pd.DataFrame({"date": dates, "symbol": sym, "close": close})
        rows.append(df)

    return pd.concat(rows, ignore_index=True)


def load_tdcc_data(symbols: list[str], periods: int = 260) -> pd.DataFrame:
    """載入 TDCC 大戶持股比例範例資料。"""
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=periods)
    rng = np.random.default_rng(7)
    rows = []

    for sym in symbols:
        base = rng.uniform(0.12, 0.35)
        noise = rng.normal(0, 0.003, size=periods)
        ratio = np.clip(base + np.cumsum(noise), 0.05, 0.6)
        df = pd.DataFrame(
            {
                "date": dates,
                "symbol": sym,
                "large_holder_ratio": ratio,
            }
        )
        rows.append(df)

    return pd.concat(rows, ignore_index=True)
