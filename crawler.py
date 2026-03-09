from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import time
import random
from urllib.parse import quote

# 2026年3月真实可用免费平台（保底列表，永远不会空）
FALLBACK_PLATFORMS = [
    {"title": "SiliconFlow 硅基流动（送2000万tokens免费额度）", "href": "https://cloud.siliconflow.cn/", "body": "最强免费推理平台，速度快、额度大，无需信用卡。直接注册领额度！"},
    {"title": "Groq（全球最快免费 Llama/Qwen API）", "href": "https://console.groq.com/keys", "body": "免费额度极高，Llama3.3-70B 超快推理，每天几千次请求。"},
    {"title": "DeepSeek 免费 API（高额度无信用卡）", "href": "https://platform.deepseek.com/api_keys", "body": "DeepSeek-V3/R1 模型免费调用，额度非常大。"},
    {"title": "OpenRouter 免费模型合集", "href": "https://openrouter.ai/models?max_price=0", "body": "一键切换上百个免费开源模型，适合测试各种 LLM。"},
    {"title": "火山引擎 豆包大模型（每日50万tokens免费）", "href": "https://www.volcengine.com/experience/ark", "body": "字节跳动官方，每天免费额度，国内最稳。"},
    {"title": "Fireworks AI 免费层", "href": "https://fireworks.ai/", "body": "高性能推理，免费试用额度充足。"},
    {"title": "Together.ai 免费额度", "href": "https://www.together.ai/", "body": "开源模型大全，新用户有免费 credits。"},
]

def main():
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"🚀 开始 {today} 保底混合搜索...")

    queries = ["免费 LLM API 2026 Groq SiliconFlow", "硅基流动免费 API", "火山引擎豆包免费额度", "DeepSeek 免费 API", "OpenRouter free models 2026"]

    whitelist = ["LLM", "API", "大模型", "Groq", "SiliconFlow", "OpenRouter", "DeepSeek", "Together", "豆包", "火山"]
    all_results = []
    seen = set()

    # 尝试实时搜索
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            for query in queries:
                try:
                    url = f"https://www.google.com/search?q={quote(query)}&hl=zh-CN"
                    page.goto(url, timeout=15000)
                    page.wait_for_timeout(random.randint(2000, 4000))
                    results = page.locator('div.g').all()
                    print(f"✅ Google 返回 {len(results)} 条")
                    for result in results[:5]:
                        try:
                            title = result.locator('h3').first.inner_text().strip()
                            href = result.locator('a').first.get_attribute('href')
                            body = result.locator('div.VwiC3b').first.inner_text().strip()[:250] if result.locator('div.VwiC3b').count() else ""
                            if any(w.lower() in (title + body).lower() for w in whitelist) and href and href not in seen:
                                seen.add(href)
                                all_results.append({"title": title, "href": href, "body": body + "..."})
                        except:
                            continue
                except Exception as e:
                    print(f"搜索异常: {e}")
                time.sleep(2)
            browser.close()
    except Exception as e:
        print(f"实时搜索失败（正常现象）: {e}")

    # 如果实时没抓到，就用保底列表
    if not all_results:
        print("实时搜索暂无新结果 → 使用保底可靠平台列表")
        all_results = FALLBACK_PLATFORMS[:]
    else:
        print(f"实时抓到 {len(all_results)} 条新资源！")

    print(f"\n=== 最终统计 ===\n共 {len(all_results)} 条高质量免费Model资源\n")

    # 生成报告
    md_content = f"# 🤖 每日免费 AI Model 使用方式报告\n\n"
    md_content += f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)\n"
    md_content += "**数据来源**：实时搜索 + 2026最新保底平台（保证有内容）\n\n---\n\n"

    for i, res in enumerate(all_results, 1):
        md_content += f"### {i}. {res['title']}\n\n"
        md_content += f"🔗 [立即访问]({res['href']})\n\n"
        md_content += f"{res['body']}\n\n---\n\n"

    md_content += "\n> 本报告由 GitHub Actions 自动生成，每天微信推送。保底列表永久可用！\n"

    with open("daily_report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    count = len(all_results)
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"count={count}\n")

    print(f"🎉 报告生成完成！")

if __name__ == "__main__":
    main()
