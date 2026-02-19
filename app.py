import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta
from datetime import datetime, timedelta

# 頁面配置
st.set_page_config(
    page_title="ETF 分析儀表板",
    page_icon="📊",
    layout="wide"
)

# 標題
st.title("📊 ETF 即時分析儀表板")
st.markdown("分析 VOO, QQQ, VT 等熱門 ETF 的即時行情與技術指標")

# 側邊欄選項
st.sidebar.header("⚙️ 設定")
ticker = st.sidebar.selectbox(
    "選擇 ETF",
    ["VOO", "QQQ", "VT", "SPY", "IVV", "VTI"],
    help="選擇要分析的 ETF"
)

period = st.sidebar.selectbox(
    "時間範圍",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3,
    help="選擇歷史數據的時間範圍"
)

interval = st.sidebar.selectbox(
    "資料間隔",
    ["1d", "1wk", "1mo"],
    help="選擇價格數據的時間間隔"
)

# 獲取數據
@st.cache_data(ttl=300)  # 快取 5 分鐘
def get_stock_data(ticker, period, interval):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    info = stock.info
    return df, info

try:
    with st.spinner(f'正在載入 {ticker} 資料...'):
        df, info = get_stock_data(ticker, period, interval)
    
    # 即時報價區塊
    st.header(f"💹 {ticker} 即時報價")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    current_price = df['Close'].iloc[-1]
    previous_close = info.get('previousClose', df['Close'].iloc[-2])
    change = current_price - previous_close
    change_percent = (change / previous_close) * 100
    
    with col1:
        st.metric(
            label="目前價格",
            value=f"${current_price:.2f}",
            delta=f"{change:.2f} ({change_percent:+.2f}%)"
        )
    
    with col2:
        st.metric(
            label="開盤價",
            value=f"${df['Open'].iloc[-1]:.2f}"
        )
    
    with col3:
        st.metric(
            label="最高價",
            value=f"${df['High'].iloc[-1]:.2f}"
        )
    
    with col4:
        st.metric(
            label="最低價",
            value=f"${df['Low'].iloc[-1]:.2f}"
        )
    
    with col5:
        volume_millions = df['Volume'].iloc[-1] / 1_000_000
        st.metric(
            label="成交量",
            value=f"{volume_millions:.1f}M"
        )
    
    # 基本資訊
    st.header("📋 基本資訊")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**全名:** {info.get('longName', 'N/A')}")
        st.write(f"**類別:** {info.get('category', 'N/A')}")
        st.write(f"**52週最高:** ${info.get('fiftyTwoWeekHigh', 'N/A')}")
    
    with col2:
        st.write(f"**資產規模:** ${info.get('totalAssets', 0)/1e9:.2f}B")
        st.write(f"**費用率:** {info.get('annualReportExpenseRatio', 0)*100:.2f}%")
        st.write(f"**52週最低:** ${info.get('fiftyTwoWeekLow', 'N/A')}")
    
    with col3:
        st.write(f"**殖利率:** {info.get('yield', 0)*100:.2f}%")
        st.write(f"**Beta:** {info.get('beta3Year', 'N/A')}")
        st.write(f"**平均成交量:** {info.get('averageVolume', 0)/1e6:.1f}M")
    
    # 計算技術指標
    df['SMA_20'] = ta.sma(df['Close'], length=20)
    df['SMA_50'] = ta.sma(df['Close'], length=50)
    df['SMA_200'] = ta.sma(df['Close'], length=200)
    
    # RSI
    df['RSI'] = ta.rsi(df['Close'], length=14)
    
    # MACD
    macd = ta.macd(df['Close'])
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']
    df['MACD_hist'] = macd['MACDh_12_26_9']
    
    # 布林通道
    bbands = ta.bbands(df['Close'], length=20)
    df['BB_upper'] = bbands['BBU_20_2.0']
    df['BB_middle'] = bbands['BBM_20_2.0']
    df['BB_lower'] = bbands['BBL_20_2.0']
    
    # 技術分析圖表
    st.header("📈 技術分析圖表")
    
    # 創建子圖
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.5, 0.2, 0.15, 0.15],
        subplot_titles=(
            f'{ticker} 價格走勢與技術指標',
            '成交量',
            'RSI (相對強弱指標)',
            'MACD'
        )
    )
    
    # 蠟燭圖
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='價格'
        ),
        row=1, col=1
    )
    
    # 移動平均線
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20',
                   line=dict(color='orange', width=1)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50',
                   line=dict(color='blue', width=1)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_200'], name='SMA 200',
                   line=dict(color='red', width=1)),
        row=1, col=1
    )
    
    # 布林通道
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_upper'], name='布林上軌',
                   line=dict(color='gray', width=1, dash='dash')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_lower'], name='布林下軌',
                   line=dict(color='gray', width=1, dash='dash'),
                   fill='tonexty', fillcolor='rgba(128,128,128,0.1)'),
        row=1, col=1
    )
    
    # 成交量
    colors = ['red' if df['Close'].iloc[i] < df['Open'].iloc[i] else 'green' 
              for i in range(len(df))]
    fig.add_trace(
        go.Bar(x=df.index, y=df['Volume'], name='成交量',
               marker_color=colors),
        row=2, col=1
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(x=df.index, y=df['RSI'], name='RSI',
                   line=dict(color='purple', width=2)),
        row=3, col=1
    )
    # RSI 超買超賣線
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    # MACD
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MACD'], name='MACD',
                   line=dict(color='blue', width=2)),
        row=4, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MACD_signal'], name='Signal',
                   line=dict(color='orange', width=2)),
        row=4, col=1
    )
    fig.add_trace(
        go.Bar(x=df.index, y=df['MACD_hist'], name='Histogram',
               marker_color=df['MACD_hist'].apply(lambda x: 'green' if x > 0 else 'red')),
        row=4, col=1
    )
    
    # 更新佈局
    fig.update_layout(
        height=1200,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="日期", row=4, col=1)
    fig.update_yaxes(title_text="價格 ($)", row=1, col=1)
    fig.update_yaxes(title_text="成交量", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)
    fig.update_yaxes(title_text="MACD", row=4, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 技術指標解讀
    st.header("🔍 技術指標解讀")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("當前訊號")
        
        # 趨勢判斷
        last_price = df['Close'].iloc[-1]
        sma_20 = df['SMA_20'].iloc[-1]
        sma_50 = df['SMA_50'].iloc[-1]
        sma_200 = df['SMA_200'].iloc[-1]
        
        if last_price > sma_20 > sma_50 > sma_200:
            trend = "🟢 強勢上漲趨勢"
        elif last_price < sma_20 < sma_50 < sma_200:
            trend = "🔴 強勢下跌趨勢"
        elif last_price > sma_50:
            trend = "🟡 中性偏多"
        else:
            trend = "🟠 中性偏空"
        
        st.write(f"**趨勢:** {trend}")
        
        # RSI 判斷
        current_rsi = df['RSI'].iloc[-1]
        if current_rsi > 70:
            rsi_signal = "🔴 超買 (考慮獲利了結)"
        elif current_rsi < 30:
            rsi_signal = "🟢 超賣 (可能是買入機會)"
        else:
            rsi_signal = "🟡 中性"
        
        st.write(f"**RSI ({current_rsi:.2f}):** {rsi_signal}")
        
        # MACD 判斷
        current_macd = df['MACD'].iloc[-1]
        current_signal = df['MACD_signal'].iloc[-1]
        if current_macd > current_signal:
            macd_signal = "🟢 多頭訊號"
        else:
            macd_signal = "🔴 空頭訊號"
        
        st.write(f"**MACD:** {macd_signal}")
    
    with col2:
        st.subheader("統計數據")
        returns = df['Close'].pct_change()
        st.write(f"**波動率 (年化):** {returns.std() * (252**0.5) * 100:.2f}%")
        st.write(f"**最大回撤:** {(df['Close'] / df['Close'].cummax() - 1).min() * 100:.2f}%")
        st.write(f"**夏普比率 (簡化):** {(returns.mean() / returns.std() * (252**0.5)):.2f}")
    
    # 歷史數據表格
    with st.expander("📊 查看原始數據"):
        st.dataframe(
            df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(20),
            use_container_width=True
        )

except Exception as e:
    st.error(f"❌ 載入數據時發生錯誤: {str(e)}")
    st.info("請確認網路連線正常，或稍後再試。")

# 頁尾
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>📊 數據來源: Yahoo Finance | ⚠️ 僅供參考，不構成投資建議</p>
        <p>最後更新: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    unsafe_allow_html=True
)
