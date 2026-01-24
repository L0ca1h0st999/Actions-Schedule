import requests
import time

# 你的 Streamlit 地址
URL = "https://crop-disease-recognition-and-control-system-release.streamlit.app/"

# 模拟真实浏览器的请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

def wake_up():
    # 使用 Session 自动处理 Cookie 和重定向
    session = requests.Session()
    
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在发起请求: {URL}")
    
    try:
        # allow_redirects=True 是关键，它会跟着 303 一直跳到最后
        response = session.get(URL, headers=HEADERS, timeout=30, allow_redirects=True)
        
        # 打印重定向路径，方便在 Action 日志里排查
        if response.history:
            print("重定向路径:")
            for resp in response.history:
                print(f"  <- {resp.status_code} : {resp.url}")
        
        print(f"最终落地 URL: {response.url}")
        print(f"最终状态码: {response.status_code}")

        # 检查是否真的唤醒了
        # 如果页面内容包含 'Streamlit' 且不是 'Sign in'，通常说明成功了
        if response.status_code == 200:
            if "Sign in" in response.text and "streamlit" in response.url:
                print("⚠️ 警告: 停留在登录界面，可能需要手动授权一次。")
            elif "Yes, get this app back up" in response.text:
                print("🚨 发现休眠唤醒按钮！正在尝试触发（Session 模式可能无法点击按钮，建议观察）")
            else:
                print("✅ 成功: 页面已正常加载。")
        else:
            print(f"❌ 失败: 收到状态码 {response.status_code}")

    except Exception as e:
        print(f"💥 发生错误: {e}")

if __name__ == "__main__":
    wake_up()
