import os
import time
from datetime import datetime, timedelta, timezone
from playwright.sync_api import sync_playwright

URL = "https://crop-disease-recognition-and-control-system-release.streamlit.app/"
LOG_FILE = "visit_log.log"

def get_bj_time():
    return (datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

def log(message):
    bj_time = get_bj_time()
    line = f"[{bj_time}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def run():
    log("=== 启动 Playwright 无头浏览器渲染模式 ===")
    
    with sync_playwright() as p:
        # 启动 Chromium 浏览器
        browser = p.chromium.launch(headless=True)
        # 模拟真实浏览器上下文
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        try:
            log(f"正在访问: {URL}")
            # 等待网络空闲，确保 JS 加载完成
            page.goto(URL, wait_until="networkidle", timeout=60000)
            
            # 方案 A: 根据 data-testid 定位 (最精准)
            # 方案 B: 根据文本内容定位
            wakeup_button = page.locator('button:has-text("Yes, get this app back up!")').or_(
                page.locator('[data-testid="wakeup-button-viewer"]')
            ).or_(
                page.locator('[data-testid="wakeup-button-owner"]')
            )

            if wakeup_button.is_visible(timeout=10000):
                log("🚨 检测到休眠按钮，正在执行点击唤醒...")
                wakeup_button.click()
                log("已点击唤醒按钮，等待 5 秒让容器启动...")
                page.wait_for_timeout(5000)  # 给容器一点启动时间
                log(f"唤醒后最终 URL: {page.url}")
            else:
                log("✅ 未发现唤醒按钮，应用可能已经处于活跃状态。")
                
            log(f"当前页面标题: {page.title()}")
            
        except Exception as e:
            log(f"💥 运行异常: {str(e)}")
        finally:
            browser.close()
            log("=== 任务结束 ===")
            with open(LOG_FILE, "a") as f: f.write("-" * 50 + "\n")

if __name__ == "__main__":
    run()