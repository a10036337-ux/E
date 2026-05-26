from __future__ import annotations

import numpy as np
import pandas as pd


def zscore(series: pd.Series, window: int = 60) -> pd.Series:
    mean = series.rolling(window).mean()
    std = series.rolling(window).std(ddof=0)
    return (series - mean) / std.replace(0, np.nan)


def build_scores(price_df: pd.DataFrame, tdcc_df: pd.DataFrame) -> pd.DataFrame:
    df = price_df.merge(tdcc_df, on=["date", "symbol"], how="inner").sort_values(
        ["symbol", "date"]
    )

    grouped = df.groupby("symbol", group_keys=False)

    df["ret_20"] = grouped["close"].pct_change(20)
    df["ret_60"] = grouped["close"].pct_change(60)
    df["trend_raw"] = df["ret_20"].fillna(0) + df["ret_60"].fillna(0)
    df["trend_score"] = grouped["trend_raw"].transform(lambda x: zscore(x, 60)).fillna(0)

    df["lh_5"] = grouped["large_holder_ratio"].transform(lambda x: x.rolling(5).mean())
    df["lh_20"] = grouped["large_holder_ratio"].transform(lambda x: x.rolling(20).mean())
    df["chip_raw"] = (df["lh_5"] - df["lh_20"]).fillna(0)
    df["chip_score"] = grouped["chip_raw"].transform(lambda x: zscore(x, 60)).fillna(0)

    df["total_score"] = 0.6 * df["chip_score"] + 0.4 * df["trend_score"]

    return df
