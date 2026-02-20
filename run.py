import os
import sys
from streamlit.web import cli as stcli

if __name__ == '__main__':
    # 印出所有環境變數來調試
    print("=" * 50)
    print("環境變數調試資訊:")
    print(f"PORT = {os.environ.get('PORT', 'NOT SET')}")
    print(f"ZEABUR_PORT = {os.environ.get('ZEABUR_PORT', 'NOT SET')}")
    print(f"All env vars containing 'PORT':")
    for key, value in os.environ.items():
        if 'PORT' in key.upper():
            print(f"  {key} = {value}")
    print("=" * 50)
    
    # 從環境變數讀取 port，沒有的話用 8501
    port = int(os.environ.get('PORT', os.environ.get('ZEABUR_PORT', 8501)))
    
    print(f"使用 port: {port}")
    
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
