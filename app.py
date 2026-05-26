import streamlit as st

from src.backtest import run_top_n_backtest
from src.data_loader import load_finlab_data, load_tdcc_data
from src.etf_rotation import run_etf_rotation
from src.signals import build_scores

st.set_page_config(page_title="台股主力追蹤系統", layout="wide")
st.title("台股主力追蹤系統（FinLab + TDCC）")

symbols_input = st.text_input("股票/ETF代碼（逗號分隔）", "0050,0056,00878,00919")
symbols = [s.strip() for s in symbols_input.split(",") if s.strip()]

col1, col2, col3 = st.columns(3)
with col1:
    periods = st.slider("資料天數", 120, 800, 260, 20)
with col2:
    top_n = st.slider("主力策略持股數", 1, min(6, max(1, len(symbols))), min(3, len(symbols)))
with col3:
    etf_top_n = st.slider("ETF輪動持有檔數", 1, min(4, max(1, len(symbols))), min(2, len(symbols)))

if st.button("執行分析"):
    price_df = load_finlab_data(symbols, periods=periods)
    tdcc_df = load_tdcc_data(symbols, periods=periods)
    score_df = build_scores(price_df, tdcc_df)

    latest = score_df.sort_values("date").groupby("symbol").tail(1)
    st.subheader("最新主力分數")
    st.dataframe(latest[["symbol", "chip_score", "trend_score", "total_score"]].sort_values("total_score", ascending=False))

    st.subheader("主力 Top-N 回測")
    bt_df, _ = run_top_n_backtest(score_df, top_n=top_n)
    st.line_chart(bt_df["equity"])
    st.dataframe(bt_df.tail(15))

    st.subheader("ETF 輪動回測")
    rot_df = run_etf_rotation(price_df, lookback=60, rebalance_freq=20, top_n=etf_top_n)
    st.line_chart(rot_df["equity"])
    st.dataframe(rot_df.tail(15))

    st.caption("此畫面使用模擬資料示範，請替換 data_loader 後再用於實盤研究。")
