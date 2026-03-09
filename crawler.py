from duckduckgo_search import DDGS
from datetime import datetime
import os
import time
import random

def search_with_retry(ddgs, query, max_results=8, retries=3):
    for attempt in range(retries):
        try:
            results = list(ddgs.text(query, max_results=max_results))
            print(f"  查询: {query} | 尝试 {attempt+1} | 返回 {len(results)} 条")
            if results:
                for i, r in enumerate(results[:3]):  # 只打印前3条预览
                    print(f"    {i+1}. {r.get('title', '')[:80]}...")
            return results
        except Exception as e:
            print(f"  查询失败 (尝试 {attempt+1}/{retries}): {e}")
            time.sleep(3 + attempt * 2)
    print(f"  查询最终失败: {query}")
    return []

def main():
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"🚀 开始 {today} 全网搜索免费 AI Model...")

    queries = [
        "free LLM API 2026 OR Groq free tier",
        "free inference API Together.ai OR Fireworks.ai OR DeepSeek API",
        "OpenRouter free models 2026",
        "free Llama 4 OR Qwen3 API no credit card",
        "best free LLM API March 2026",
        "Groq Llama3 free limit",
        "free AI API without credit card 2026",
        "HuggingFace inference endpoints free",
    ]

    all_results = []
    seen = set()

    with DDGS() as ddgs:
        for query in queries:
            results = search_with_retry(ddgs, query)
            for r in results:
                href = r.get("href")
                if href and href not in seen:
                    seen.add(href)
                    all_results.append({
                        "title": r.get("title", "无标题"),
                        "href": href,
                        "body": r.get("body", "")[:280]
                    })
            time.sleep(random.uniform(2, 4))  # 随机延时防封

    print(f"\n=== 最终统计 ===\n共收集到 {len(all_results)} 条唯一结果\n")

    # 生成报告
    md_content = f"# 🤖 每日免费 AI Model 使用方式报告\n\n"
    md_content += f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)\n"
    md_content += "**数据来源**：DuckDuckGo 全网搜索（最新相关）\n\n---\n\n"

    if not all_results:
        md_content += "**⚠️ 今天暂无新结果**（搜索引擎可能临时限制）。明天会自动重试。\n\n"
    else:
        for i, res in enumerate(all_results, 1):
            md_content += f"### {i}. {res['title']}\n\n"
            md_content += f"🔗 [立即访问]({res['href']})\n\n"
            md_content += f"{res['body']}\n\n---\n\n"

    md_content += "\n> 本报告由 GitHub Actions + PushPlus 自动生成，每天微信推送通知。\n"

    with open("daily_report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    # 输出数量给微信推送
    count = len(all_results)
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"count={count}\n")

    print(f"🎉 报告生成完成！共 {count} 条")

if __name__ == "__main__":
    main()
