import requests
import time
from datetime import datetime, timedelta, timezone

# 你的 Streamlit 地址
URL = "https://crop-disease-recognition-and-control-system-release.streamlit.app/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def wake_up():
    # 使用现代写法获取北京时间
    bj_time = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    
    # 建立会话对象
    session = requests.Session()
    
    try:
        # --- 第一次尝试 ---
        print(f"[{bj_time}] === 正在发起第一次请求（叫醒服务） ===")
        response1 = session.get(URL, headers=HEADERS, timeout=30, allow_redirects=True)
        
        print(f"结果状态码: {response1.status_code}")
        print(f"最终落地页: {response1.url}")
        
        # 打印获取到的 Session/Cookies
        cookies_dict = session.cookies.get_dict()
        if cookies_dict:
            print("已获取 Session Cookies:")
            for key, value in cookies_dict.items():
                # 为了安全，敏感信息较长时只显示前后几位
                display_value = f"{value[:10]}...{value[-10:]}" if len(value) > 20 else value
                print(f"  - {key}: {display_value}")
        else:
            print("未发现 Cookies (可能是无状态响应)")

        if response1.status_code == 200:
            print("\n✅ 第一次成功，正在等待 2 秒后发起第二次 Session 确认...")
            time.sleep(2)
            
            # --- 第二次确认 ---
            # 这次请求会带上上面打印出来的所有 Cookies
            response2 = session.get(URL, headers=HEADERS, timeout=30, allow_redirects=True)
            
            print(f"第二次结果: {response2.status_code}")
            print(f"最终落地页: {response2.url}")
            
            if response2.status_code == 200:
                print("🎯 二次确认成功！Session 已保持活跃。")
            else:
                print(f"⚠️ 第二次请求异常，状态码: {response2.status_code}")
        else:
            print(f"❌ 第一次请求失败，状态码: {response1.status_code}")

    except Exception as e:
        print(f"💥 发生错误: {e}")

if __name__ == "__main__":
    wake_up()
