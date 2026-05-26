# 台股主力追蹤系統（FinLab + TDCC + Streamlit）

此專案提供一個可擴充的「台股主力追蹤 + ETF 輪動 + 回測」基礎框架，目標是：

- 使用 **FinLab** 取得台股資料（價格、籌碼、財報等）。
- 使用 **TDCC（集保戶股權分散）** 資料做主力籌碼觀察。
- 以 **Streamlit** 建立互動式儀表板。
- 用 **Docker** 一鍵啟動。
- 內建 **回測模組** 與 **ETF 輪動策略樣板**。

> 注意：本專案預設為研究/教育用途，非投資建議。

## 功能架構

- `src/data_loader.py`
  - FinLab/TDCC 資料讀取介面（可替換成真實 API 實作）
- `src/signals.py`
  - 主力指標計算（籌碼分數、趨勢分數）
- `src/backtest.py`
  - 向量化回測（簡化版）
- `src/etf_rotation.py`
  - ETF 輪動策略（動能排序 + 持有前 N 檔）
- `app.py`
  - Streamlit 視覺化與策略執行

## 快速開始

### 1) 本機執行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### 2) Docker 執行

```bash
docker build -t tw-main-force-tracker .
docker run --rm -p 8501:8501 tw-main-force-tracker
```

瀏覽器開啟：`http://localhost:8501`

## 策略邏輯（預設）

### 主力追蹤分數

對每檔標的計算：

- `chip_score`：
  - TDCC 大戶持股比例變動（近 1 週 vs 4 週平均）
- `trend_score`：
  - 價格動能（20 日報酬 + 60 日報酬）

總分：

```text
total_score = 0.6 * chip_score + 0.4 * trend_score
```

### ETF 輪動

每次再平衡日（例如每 20 個交易日）：

1. 計算 ETF 近 `lookback` 日動能。
2. 排序後選擇前 `top_n` 檔。
3. 等權配置。
4. 持有至下一次再平衡。

## FinLab/TDCC 串接建議

請在 `src/data_loader.py` 的 `load_finlab_data()` 與 `load_tdcc_data()` 中替換為你自己的資料來源（API / CSV / DB）。

若你有 FinLab token：

- 可在 Docker 或本機環境設定：`FINLAB_API_TOKEN`
- 在資料載入函式中讀取環境變數後初始化 API client。

## 免責聲明

- 本系統僅為策略研究範例。
- 過去績效不代表未來結果。
- 投資前請自行評估風險。
