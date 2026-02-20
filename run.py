import os
import sys
from streamlit.web import cli as stcli

if __name__ == '__main__':
    # 從環境變數讀取 port，沒有的話用 8501
    port = int(os.environ.get('PORT', 8501))
    
    # 設定 Streamlit 啟動參數
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        f"--server.port={port}",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
    ]
    
    sys.exit(stcli.main())
