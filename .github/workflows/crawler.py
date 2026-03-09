from duckduckgo_search import DDGS
from datetime import datetime
import os

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"🚀 开始 {today} 全网搜索...")

    queries = [
        "免费 LLM API OR 大模型免费调用 2026",
        "free LLM API free tier OR Groq free OR Together.ai free OR Fireworks free",
        "免费开源模型推理平台 OR HuggingFace free inference",
        "免费 AI model hosting no credit card OR free Llama3 API",
        "免费大模型 API 限额 OR 免费 Claude Gemini Grok API 替代",
    ]

    all_results = []
    seen = set()

    with DDGS() as ddgs:
        for query in queries:
            try:
                results = list(ddgs.text(query, max_results=6, timelimit="d"))
                for r in results:
                    href = r.get("href")
                    if href and href not in seen:
                        seen.add(href)
                        all_results.append({
                            "query": query,
                            "title": r.get("title", "无标题"),
                            "href": href,
                            "body": r.get("body", "")[:300] + "..."
                        })
                print(f"✅ {query} 找到 {len(results)} 条")
            except Exception as e:
                print(f"⚠️ 查询失败: {e}")

    # 生成 Markdown 报告
    md_content = f"# 🤖 每日免费 AI Model 使用方式报告\n\n"
    md_content += f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)\n"
    md_content += "**数据来源**：DuckDuckGo 全网实时搜索（过去24小时）\n\n---\n\n"

    for i, res in enumerate(all_results, 1):
        md_content += f"### {i}. {res['title']}\n\n"
        md_content += f"**查询**：{res['query']}\n"
        md_content += f"🔗 [立即访问]({res['href']})\n\n"
        md_content += f"{res['body']}\n\n---\n\n"

    md_content += "\n> 本报告由 GitHub Actions + PushPlus 自动生成，每天微信推送通知。\n"

    with open("daily_report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    # 输出数量给 GitHub Actions（用于微信推送）
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"count={len(all_results)}\n")

    print(f"🎉 报告生成完成！共 {len(all_results)} 条")

if __name__ == "__main__":
    main()
