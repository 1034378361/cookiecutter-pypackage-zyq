#!/usr/bin/env python
"""
生成项目变更日志脚本。

此脚本分析git提交历史，生成格式化的变更日志。
支持按标签筛选提交范围，并输出到指定文件。
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime


def parse_args():
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="生成格式化的变更日志")
    parser.add_argument("--since", help="起始标签/提交")
    parser.add_argument("--until", help="结束标签/提交", required=True)
    parser.add_argument("--output", help="输出文件路径", required=True)
    return parser.parse_args()


def get_commit_log(since=None, until=None):
    """获取git提交日志。"""
    cmd = ["git", "log", "--no-merges", "--pretty=format:%h|%an|%s"]
    if since and until:
        cmd.append(f"{since}..{until}")
    elif until:
        cmd.append(until)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"获取git日志时出错: {e}", file=sys.stderr)
        return []


def categorize_commits(commits):
    """将提交按类型分类。"""
    categories = {
        "新功能": [],
        "修复": [],
        "文档": [],
        "样式": [],
        "重构": [],
        "性能": [],
        "测试": [],
        "构建": [],
        "其他": []
    }

    patterns = {
        "新功能": r"^feat(\(.*\))?:",
        "修复": r"^fix(\(.*\))?:",
        "文档": r"^docs(\(.*\))?:",
        "样式": r"^style(\(.*\))?:",
        "重构": r"^refactor(\(.*\))?:",
        "性能": r"^perf(\(.*\))?:",
        "测试": r"^test(\(.*\))?:",
        "构建": r"^(build|chore)(\(.*\))?:"
    }

    for commit in commits:
        if not commit:
            continue

        try:
            hash_id, author, message = commit.split("|", 2)
        except ValueError:
            continue

        categorized = False
        for category, pattern in patterns.items():
            if re.search(pattern, message):
                categories[category].append((hash_id, author, message))
                categorized = True
                break

        if not categorized:
            categories["其他"].append((hash_id, author, message))

    return categories


def generate_markdown(categories, until_tag):
    """生成Markdown格式的变更日志。"""
    version = until_tag.lstrip("v")
    now = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# {version} ({now})",
        ""
    ]

    for category, commits in categories.items():
        if not commits:
            continue

        lines.append(f"## {category}")
        lines.append("")

        for hash_id, author, message in commits:
            # 清理提交消息，移除前缀
            cleaned_message = re.sub(r"^(feat|fix|docs|style|refactor|perf|test|build|chore)(\(.*\))?:\s*", "", message)
            lines.append(f"* {cleaned_message} ({hash_id[:7]})")

        lines.append("")

    return "\n".join(lines)


def main():
    """主函数。"""
    args = parse_args()

    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    commits = get_commit_log(args.since, args.until)
    categories = categorize_commits(commits)
    markdown = generate_markdown(categories, args.until)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"变更日志已生成至 {args.output}")


if __name__ == "__main__":
    main()
