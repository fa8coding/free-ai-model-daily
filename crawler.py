from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import time
import random
from urllib.parse import quote

def main():
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"🚀 开始 {today} Google 精准搜索 + 强过滤...")

    queries = [
        "免费 LLM API 2026 OR Groq free tier",
        "硅基流动 SiliconFlow 免费 API",
        "火山引擎 豆包免费 API OR 火山引擎免费额度",
        "OpenRouter free models OR OpenRouter 免费 LLM",
        "DeepSeek 免费 API OR DeepSeek API 无信用卡",
        "Together.ai free tier OR Fireworks AI free LLM",
        "免费大模型推理平台 2026 Groq SiliconFlow",
    ]

    whitelist = ["LLM", "API", "大模型", "Groq", "SiliconFlow", "OpenRouter", "DeepSeek", "Together", "Fireworks", "豆包", "火山引擎", "Llama", "Qwen"]
    blacklist = ["知乎", "图片", "思维导图", "短剧", "PPT", "追剧", "模板", "英语", "grammar"]

    all_results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()

        for query in queries:
            try:
                url = f"https://www.google.com/search?q={quote(query)}&hl=zh-CN"
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(random.randint(3000, 5000))

                results = page.locator('div.g').all()
                print(f"✅ {query} → Google 返回 {len(results)} 条原始结果")

                for result in results[:8]:
                    try:
                        title_elem = result.locator('h3').first
                        title = title_elem.inner_text().strip()
                        href = result.locator('a').first.get_attribute('href')
                        body = result.locator('div.VwiC3b').first.inner_text().strip() if result.locator('div.VwiC3b').count() > 0 else ""

                        # 强过滤：必须含白名单 + 不含黑名单
                        if not any(w.lower() in (title + body).lower() for w in whitelist):
                            continue
                        if any(b.lower() in (title + body).lower() for b in blacklist):
                            continue

                        if href and href.startswith('http') and href not in seen:
                            seen.add(href)
                            all_results.append({
                                "title": title,
                                "href": href,
                                "body": body[:280] + "..." if body else "（无摘要）"
                            })
                    except:
                        continue
            except Exception as e:
                print(f"⚠️ 查询失败 {query}: {e}")
            time.sleep(random.uniform(2, 4))

        browser.close()

    print(f"\n=== 最终统计 ===\n共收集到 {len(all_results)} 条**高质量AI免费Model资源**\n")

    # 生成报告
    md_content = f"# 🤖 每日免费 AI Model 使用方式报告\n\n"
    md_content += f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)\n"
    md_content += "**数据来源**：Playwright + Google 强过滤搜索（只保留AI相关）\n\n---\n\n"

    if not all_results:
        md_content += "**⚠️ 今天暂无新结果**，明天自动重试。\n\n"
    else:
        for i, res in enumerate(all_results, 1):
            md_content += f"### {i}. {res['title']}\n\n"
            md_content += f"🔗 [立即访问]({res['href']})\n\n"
            md_content += f"{res['body']}\n\n---\n\n"

    md_content += "\n> 本报告由 GitHub Actions + Google强过滤 + PushPlus 自动生成。\n"

    with open("daily_report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    count = len(all_results)
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"count={count}\n")

    print(f"🎉 报告生成完成！共 {count} 条")

if __name__ == "__main__":
    main()
