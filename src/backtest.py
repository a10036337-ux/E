from __future__ import annotations

import pandas as pd


def run_top_n_backtest(score_df: pd.DataFrame, top_n: int = 3) -> tuple[pd.DataFrame, pd.Series]:
    """每日選擇 total_score 前 N 名，隔日等權持有。"""
    df = score_df.copy().sort_values(["date", "symbol"])
    df["next_ret"] = df.groupby("symbol")["close"].pct_change().shift(-1)

    rank = df.groupby("date")["total_score"].rank(ascending=False, method="first")
    df["selected"] = rank <= top_n

    daily = (
        df[df["selected"]]
        .groupby("date")["next_ret"]
        .mean()
        .fillna(0)
        .rename("strategy_ret")
    )

    equity = (1 + daily).cumprod().rename("equity")

    result = pd.concat([daily, equity], axis=1)
    return result, equity
