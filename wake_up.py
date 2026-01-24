import requests
import time
from datetime import datetime, timedelta, timezone

URL = "https://crop-disease-recognition-and-control-system-release.streamlit.app/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def print_step_info(step_name, resp):
    """打印单次请求的详细跳转过程和 Session 状态"""
    print(f"\n--- {step_name} 详细过程 ---")
    
    # 1. 打印重定向历史 (如果有)
    if resp.history:
        for i, hist in enumerate(resp.history, 1):
            print(f"跳转层级 [{i}]:")
            print(f"  状态码: {hist.status_code}")
            print(f"  URL: {hist.url}")
    
    # 2. 打印最终落地信息
    print(f"最终落地:")
    print(f"  状态码: {resp.status_code}")
    print(f"  URL: {resp.url}")
    
    # 3. 打印当前 Session 中的 Cookies
    cookies = resp.cookies.get_dict()
    if cookies:
        print(f"当前 Session 携带的 Cookies:")
        for k, v in cookies.items():
            print(f"  - {k}: {v}")
    else:
        print("当前步骤未发现有效 Cookies")

def wake_up():
    bj_time = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    session = requests.Session()
    
    try:
        # --- 第一次尝试 ---
        print(f"[{bj_time}] === 开始全流程保活测试 ===")
        r1 = session.get(URL, headers=HEADERS, timeout=30, allow_redirects=True)
        print_step_info("第一次请求 (叫醒与身份交换)", r1)

        if r1.status_code == 200:
            print("\n" + "="*50)
            print("等待 2 秒后发起第二次确认访问...")
            time.sleep(2)
            
            # --- 第二次确认 ---
            r2 = session.get(URL, headers=HEADERS, timeout=30, allow_redirects=True)
            print_step_info("第二次请求 (Session 维持确认)", r2)
            
            if r2.status_code == 200:
                print("\n✅ 流程全部完成，应用已成功唤醒并维持 Session。")
        else:
            print(f"\n❌ 流程中断，初次请求状态码: {r1.status_code}")

    except Exception as e:
        print(f"\n💥 运行时异常: {e}")

if __name__ == "__main__":
    wake_up()
