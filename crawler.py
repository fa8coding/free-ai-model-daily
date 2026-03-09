from duckduckgo_search import DDGS
from datetime import datetime
import os
import time
import random

def main():
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"🚀 开始 {today} 精准搜索免费 AI Model...")

    # 2026年真实有效精准查询词（已过滤无关内容）
    queries = [
        "免费 LLM API 2026 OR 免费大模型 API",
        "硅基流动 SiliconFlow 免费 API",
        "火山引擎 免费大模型 API OR 豆包免费额度",
        "Groq 免费 API OR Groq free tier 2026",
        "OpenRouter free models OR OpenRouter 免费",
        "Together.ai free tier OR Fireworks AI free",
        "DeepSeek 免费 API OR DeepSeek API 无信用卡",
        "免费 Grok API OR Gemini 免费层 2026",
    ]

    all_results = []
    seen = set()

    with DDGS() as ddgs:
        for query in queries:
            try:
                results = list(ddgs.text(query, max_results=8))
                print(f"✅ {query} → 找到 {len(results)} 条")
                for r in results:
                    href = r.get("href")
                    if href and href not in seen:
                        seen.add(href)
                        title = r.get("title", "")
                        body = r.get("body", "")[:280]
                        # 额外过滤无关英语语法帖
                        if any(word in title.lower() for word in ["grammar", "english language", "opposite of free", "for free"]):
                            continue
                        all_results.append({
                            "title": title,
                            "href": href,
                            "body": body
                        })
                time.sleep(random.uniform(1.5, 3))
            except Exception as e:
                print(f"⚠️ 查询失败: {e}")

    print(f"\n=== 最终统计 ===\n共收集到 {len(all_results)} 条高质量免费Model资源\n")

    # 生成报告
    md_content = f"# 🤖 每日免费 AI Model 使用方式报告\n\n"
    md_content += f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)\n"
    md_content += "**数据来源**：DuckDuckGo 全网精准搜索（2026最新免费平台）\n\n---\n\n"

    if not all_results:
        md_content += "**⚠️ 今天暂无新结果**，明天自动重试。\n\n"
    else:
        for i, res in enumerate(all_results, 1):
            md_content += f"### {i}. {res['title']}\n\n"
            md_content += f"🔗 [立即访问]({res['href']})\n\n"
            md_content += f"{res['body']}\n\n---\n\n"

    md_content += "\n> 本报告由 GitHub Actions + PushPlus 自动生成，每天推送微信。\n"

    with open("daily_report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    # 输出给推送
    count = len(all_results)
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"count={count}\n")

    print(f"🎉 报告生成完成！共 {count} 条高质量资源")

if __name__ == "__main__":
    main()
