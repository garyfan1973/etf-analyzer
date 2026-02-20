FROM python:3.10-slim

WORKDIR /app

# 複製 requirements 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式檔案
COPY . .

# 暴露 port（使用環境變數，預設 8501 配合 Zeabur）
ENV PORT=8501
EXPOSE ${PORT}

# 啟動應用
CMD python3 run.py
