from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import time
import random
from urllib.parse import quote

def main():
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"🚀 开始 {today} Playwright Bing 精准搜索...")

    queries = [
        "免费 LLM API 2026 OR 免费大模型 API",
        "硅基流动 SiliconFlow 免费 API",
        "火山引擎 豆包免费 API OR 火山引擎免费额度",
        "Groq 免费 API 2026 OR Groq free tier",
        "OpenRouter 免费模型 OR OpenRouter free",
        "Together.ai free tier OR Fireworks AI free",
        "DeepSeek 免费 API OR DeepSeek API 无信用卡",
    ]

    all_results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for query in queries:
            try:
                url = f"https://www.bing.com/search?q={quote(query)}"
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                page.wait_for_timeout(random.randint(2500, 4500))  # 模拟真人

                results = page.locator('li.b_algo').all()
                print(f"✅ {query} → Bing 返回 {len(results)} 条结果")

                for result in results[:6]:  # 每条查询最多取6条
                    try:
                        a = result.locator('h2 a').first
                        title = a.inner_text().strip()
                        href = a.get_attribute('href')
                        snippet = result.locator('p').first.inner_text().strip() if result.locator('p').count() > 0 else ""
                        
                        if href and href.startswith('http') and href not in seen:
                            seen.add(href)
                            all_results.append({
                                "title": title,
                                "href": href,
                                "body": snippet[:280] + "..." if snippet else "（无摘要）"
                            })
                    except:
                        continue
            except Exception as e:
                print(f"⚠️ 查询失败 {query}: {e}")
            time.sleep(random.uniform(2, 4))

        browser.close()

    print(f"\n=== 最终统计 ===\n共收集到 {len(all_results)} 条高质量免费Model资源\n")

    # 生成报告
    md_content = f"# 🤖 每日免费 AI Model 使用方式报告\n\n"
    md_content += f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)\n"
    md_content += "**数据来源**：Playwright + Bing 全网搜索（2026最新）\n\n---\n\n"

    if not all_results:
        md_content += "**⚠️ 今天暂无新结果**（极少发生），明天自动重试。\n\n"
    else:
        for i, res in enumerate(all_results, 1):
            md_content += f"### {i}. {res['title']}\n\n"
            md_content += f"🔗 [立即访问]({res['href']})\n\n"
            md_content += f"{res['body']}\n\n---\n\n"

    md_content += "\n> 本报告由 GitHub Actions + Playwright + PushPlus 自动生成，每天推送微信。\n"

    with open("daily_report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    # 输出给推送
    count = len(all_results)
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"count={count}\n")

    print(f"🎉 报告生成完成！共 {count} 条")

if __name__ == "__main__":
    main()
