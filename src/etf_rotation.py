from __future__ import annotations

import pandas as pd


def run_etf_rotation(
    price_df: pd.DataFrame,
    lookback: int = 60,
    rebalance_freq: int = 20,
    top_n: int = 2,
) -> pd.DataFrame:
    """ETF 輪動：每 rebalance_freq 天，依 lookback 動能選前 top_n 等權持有。"""
    df = price_df.sort_values(["symbol", "date"]).copy()
    df["mom"] = df.groupby("symbol")["close"].pct_change(lookback)
    df["ret_1d"] = df.groupby("symbol")["close"].pct_change().shift(-1)

    all_dates = sorted(df["date"].unique())
    rebalance_dates = set(all_dates[::rebalance_freq])

    holdings_by_date: dict[pd.Timestamp, list[str]] = {}
    current_holdings: list[str] = []

    for d in all_dates:
        daily = df[df["date"] == d].dropna(subset=["mom"])
        if d in rebalance_dates and not daily.empty:
            current_holdings = (
                daily.sort_values("mom", ascending=False).head(top_n)["symbol"].tolist()
            )
        holdings_by_date[d] = current_holdings.copy()

    out = []
    for d in all_dates:
        holds = holdings_by_date[d]
        if not holds:
            out.append((d, 0.0))
            continue
        r = df[(df["date"] == d) & (df["symbol"].isin(holds))]["ret_1d"].mean()
        out.append((d, 0.0 if pd.isna(r) else float(r)))

    res = pd.DataFrame(out, columns=["date", "strategy_ret"]).set_index("date")
    res["equity"] = (1 + res["strategy_ret"]).cumprod()
    return res
