#!/bin/bash

# 從環境變數取得 port，如果沒有就用預設的 8501
PORT=${PORT:-8501}

# 啟動 Streamlit
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
