import requests
import time
import random
import os
from datetime import datetime, timedelta, timezone

URL = "https://crop-disease-recognition-and-control-system-release.streamlit.app/"
LOG_FILE = "visit_log.log"

HEADERS = {
    "authority": "crop-disease-recognition-and-control-system-release.streamlit.app",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
}

def write_to_log(content):
    """将信息写入本地 log 文件"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(content + "\n")

def print_step_info(step_name, resp):
    info = f"\n{'='*15} {step_name} {'='*15}\n"
    if resp.history:
        for i, hist in enumerate(resp.history, 1):
            info += f"[跳转 {i}] {hist.status_code} URL: {hist.url}\n"
    info += f"[落地] {resp.status_code} URL: {resp.url}\n"
    
    cookies = resp.cookies.get_dict()
    if cookies:
        info += "当前 Session Cookies:\n"
        for k, v in cookies.items():
            info += f"  - {k}: {v}\n"
    
    print(info) # 打印到 Action 控制台
    return info # 返回给 log 文件

def wake_up():
    bj_time = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"\n# >>> 任务开始时间: {bj_time}\n"
    session = requests.Session()
    
    try:
        # 第一层请求
        r1 = session.get(URL, headers=HEADERS, timeout=30, allow_redirects=True)
        log_entry += print_step_info("第一层：主页加载", r1)

        if r1.status_code == 200:
            time.sleep(random.uniform(1, 3))
            
            # 第二层请求 (资源)
            asset_url = f"{URL}favicon.ico"
            r2 = session.get(asset_url, headers=HEADERS, timeout=20)
            log_entry += f"\n第二层：静态资源请求 -> {asset_url} | 结果: {r2.status_code}\n"

            # 第三层请求 (确认)
            time.sleep(1)
            r3 = session.get(URL, headers=HEADERS, timeout=30)
            log_entry += print_step_info("第三层：Session 稳固确认", r3)
            
            log_entry += "✅ 流程全部完成\n"
        else:
            log_entry += f"❌ 访问异常，状态码: {r1.status_code}\n"

    except Exception as e:
        log_entry += f"💥 发生错误: {str(e)}\n"
    
    log_entry += "-"*50 + "\n"
    write_to_log(log_entry)

if __name__ == "__main__":
    wake_up()
