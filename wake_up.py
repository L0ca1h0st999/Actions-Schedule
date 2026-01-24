import requests
import time
from datetime import datetime, timedelta

# 你的 Streamlit 地址
URL = "https://crop-disease-recognition-and-control-system-release.streamlit.app/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def wake_up():
    # 获取 UTC 时间并手动加 8 小时得到北京时间
    bj_time = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    
    session = requests.Session()
    print(f"[{bj_time}] 正在发起请求: {URL}")
    
    try:
        # allow_redirects=True 会自动处理那串 303 跳转
        response = session.get(URL, headers=HEADERS, timeout=30, allow_redirects=True)
        
        if response.history:
            print("重定向路径:")
            for resp in response.history:
                print(f"  <- {resp.status_code} : {resp.url}")
        
        print(f"最终落地 URL: {response.url}")
        print(f"最终状态码: {response.status_code}")

        if response.status_code == 200:
            print("✅ 成功: 页面已正常加载。")
        else:
            print(f"❌ 失败: 收到状态码 {response.status_code}")

    except Exception as e:
        print(f"💥 发生错误: {e}")

if __name__ == "__main__":
    wake_up()
