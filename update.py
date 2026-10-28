#!/usr/bin/env python3
"""每天从 titles.txt 随机抽 10 个标题，更新 README.md"""

import random
import datetime
import re
import os
import sys

SAMPLE_SIZE = 10
TZ = datetime.timezone(datetime.timedelta(hours=8))

def main():
    today = datetime.datetime.now(TZ).date()

    # 读取标题
    if not os.path.exists("titles.txt"):
        sys.exit("❌ 找不到 titles.txt")
    with open("titles.txt", encoding="utf-8") as f:
        titles = [line.strip() for line in f if line.strip()]
    
    if len(titles) < SAMPLE_SIZE:
        sys.exit(f"❌ 标题数量不足 {SAMPLE_SIZE} 个")

    selected = random.sample(titles, SAMPLE_SIZE)

    # 生成今日内容
    lines = [
        f"> 📅 **{today.isoformat()} 今日随机推荐 · 共 {len(selected)} 个**",
        "",
        "| 序号 | 标题 |",
        "| :---: | --- |",
    ]
    for i, title in enumerate(selected, 1):
        lines.append(f"| {i} | {title.replace('|', '\\|')} |")
    
    lines.append("")
    lines.append(f"> 数据来源：titles.txt（共 {len(titles)} 个标题）")
    new_section = "\n".join(lines)

    # 更新 README
    with open("README.md", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- DAILY:START -->\n(.*?)\n<!-- DAILY:END -->"
    match = re.search(pattern, content, re.S)
    if not match:
        sys.exit("❌ README.md 缺少 <!-- DAILY:START --> 和 <!-- DAILY:END --> 标记")

    new_content = content[:match.start(1)] + new_section + content[match.end(1):]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ 已更新，今日抽取了 {len(selected)} 个标题")

if __name__ == "__main__":
    main()
