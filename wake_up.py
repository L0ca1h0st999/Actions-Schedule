import requests
import time
from datetime import datetime, timedelta, timezone

# 你的 Streamlit 地址
URL = "https://crop-disease-recognition-and-control-system-release.streamlit.app/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def wake_up():
    # 现代写法：获取北京时间 (UTC+8)
    bj_time = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    
    session = requests.Session()
    
    try:
        # --- 第一次尝试 ---
        print(f"[{bj_time}] 正在发起第一次请求（叫醒）...")
        response1 = session.get(URL, headers=HEADERS, timeout=30, allow_redirects=True)
        print(f"第一次结果: {response1.status_code} | 落地: {response1.url}")

        if response1.status_code == 200:
            print("✅ 第一次请求成功，正在进行第二次确认请求...")
            
            # 稍等 2 秒，模拟人的操作间隔
            time.sleep(2)
            
            # --- 第二次确认 ---
            response2 = session.get(URL, headers=HEADERS, timeout=30, allow_redirects=True)
            print(f"第二次结果: {response2.status_code} | 落地: {response2.url}")
            
            if response2.status_code == 200:
                print("🎯 二次确认成功！应用应已保持活跃。")
            else:
                print(f"⚠️ 第二次请求异常，状态码: {response2.status_code}")
        else:
            print(f"❌ 第一次请求失败，状态码: {response1.status_code}")

    except Exception as e:
        print(f"💥 发生错误: {e}")

if __name__ == "__main__":
    wake_up()
