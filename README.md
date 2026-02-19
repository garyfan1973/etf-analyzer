# 📊 ETF 分析儀表板

即時分析 VOO, QQQ, VT 等熱門 ETF 的互動式網頁應用程式

## ✨ 功能特色

- 📈 **即時報價** - 顯示最新的價格、漲跌幅、成交量等資訊
- 📊 **技術分析圖表** - 包含蠟燭圖、移動平均線、布林通道
- 📉 **技術指標** - RSI、MACD、成交量分析
- 🎯 **智能訊號** - 自動判斷趨勢、超買超賣狀態
- 📱 **響應式設計** - 支援桌面和行動裝置
- ⚡ **快速載入** - 資料快取機制，提升使用體驗

## 🚀 快速開始

### 安裝步驟

1. **Clone 專案**
```bash
git clone https://github.com/garyfan1973/etf-analyzer.git
cd etf-analyzer
```

2. **建立虛擬環境（推薦）**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

3. **安裝依賴套件**
```bash
pip install -r requirements.txt
```

4. **啟動應用程式**
```bash
streamlit run app.py
```

5. **開啟瀏覽器**
   - 自動開啟 `http://localhost:8501`
   - 或手動打開瀏覽器輸入該網址

## 📦 支援的 ETF

- **VOO** - Vanguard S&P 500 ETF
- **QQQ** - Invesco QQQ Trust (納斯達克 100)
- **VT** - Vanguard Total World Stock ETF
- **SPY** - SPDR S&P 500 ETF
- **IVV** - iShares Core S&P 500 ETF
- **VTI** - Vanguard Total Stock Market ETF

## 📊 技術指標說明

### 移動平均線 (SMA)
- **SMA 20** (橙色) - 短期趨勢
- **SMA 50** (藍色) - 中期趨勢
- **SMA 200** (紅色) - 長期趨勢

### 相對強弱指標 (RSI)
- **> 70** - 超買區，可能回調
- **< 30** - 超賣區，可能反彈
- **30-70** - 中性區間

### MACD
- **MACD 線** (藍色) - 快線
- **Signal 線** (橙色) - 慢線
- **Histogram** (柱狀圖) - 兩線差距

### 布林通道
- 顯示價格波動範圍
- 價格觸碰上軌可能回調
- 價格觸碰下軌可能反彈

## 🛠️ 技術架構

- **Frontend**: Streamlit
- **數據來源**: Yahoo Finance (yfinance)
- **圖表**: Plotly
- **技術分析**: pandas-ta
- **數據處理**: pandas, numpy

## ⚙️ 自訂設定

在側邊欄可以調整：
- 選擇不同的 ETF
- 調整時間範圍（1個月到5年）
- 選擇資料間隔（日線、週線、月線）

## ⚠️ 免責聲明

本工具僅供教育和研究用途，所提供的資訊和分析不構成任何投資建議。投資有風險，請謹慎評估自身風險承受能力。

## 📄 授權

MIT License

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request！

## 📧 聯絡方式

如有問題或建議，請開 Issue 討論。

---

**開發者**: Gary Fan  
**更新時間**: 2026-02-20
