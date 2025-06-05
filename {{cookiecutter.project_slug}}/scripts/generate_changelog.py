#!/usr/bin/env python
"""
自动从git提交历史生成CHANGELOG。

使用方法:
    python scripts/generate_changelog.py [--output CHANGELOG.md] [--since <commit/tag>] [--until <commit/tag>] [--config <config_file>]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import yaml
import traceback
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# 日志颜色
class ColorLog:
    """终端彩色日志输出。"""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    @staticmethod
    def error(msg: str) -> None:
        """输出错误信息"""
        print(f"{ColorLog.RED}错误: {msg}{ColorLog.RESET}")

    @staticmethod
    def warning(msg: str) -> None:
        """输出警告信息"""
        print(f"{ColorLog.YELLOW}警告: {msg}{ColorLog.RESET}")

    @staticmethod
    def info(msg: str) -> None:
        """输出信息"""
        print(f"{ColorLog.BLUE}信息: {msg}{ColorLog.RESET}")

    @staticmethod
    def success(msg: str) -> None:
        """输出成功信息"""
        print(f"{ColorLog.GREEN}成功: {msg}{ColorLog.RESET}")

# 默认提交类型分类
DEFAULT_COMMIT_TYPES = {
    "feat": "新功能",
    "fix": "Bug修复",
    "docs": "文档更新",
    "style": "代码风格",
    "refactor": "重构",
    "perf": "性能优化",
    "test": "测试相关",
    "build": "构建系统",
    "ci": "CI配置",
    "chore": "其他变更",
    "revert": "回退提交"
}

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """从配置文件加载配置。

    支持JSON和YAML格式，如果文件不存在或加载失败，返回默认配置。

    Args:
        config_path: 配置文件路径

    Returns:
        Dict[str, Any]: 配置字典
    """
    config = {
        "commit_types": DEFAULT_COMMIT_TYPES,
        "default_type": "chore",
        "header": "# 变更日志\n\n"
    }

    if not config_path:
        # 尝试查找默认配置文件
        default_paths = [
            ".changelog.json",
            ".changelog.yaml",
            ".changelog.yml",
            "changelog.config.json",
            "changelog.config.yaml",
            "changelog.config.yml"
        ]

        for path in default_paths:
            if os.path.exists(path):
                config_path = path
                ColorLog.info(f"使用默认配置文件: {path}")
                break

    if not config_path:
        ColorLog.warning("未指定配置文件且未找到默认配置文件，使用内置默认配置")
        return config

    if not os.path.exists(config_path):
        ColorLog.error(f"配置文件不存在: {config_path}")
        ColorLog.info("使用内置默认配置")
        return config

    try:
        suffix = Path(config_path).suffix.lower()
        with open(config_path, 'r', encoding='utf-8') as f:
            if suffix in ['.yaml', '.yml']:
                try:
                    custom_config = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    ColorLog.error(f"YAML格式错误: {str(e)}")
                    if hasattr(e, 'problem_mark'):
                        mark = e.problem_mark
                        ColorLog.error(f"错误位置: 行 {mark.line + 1}, 列 {mark.column + 1}")
                    raise
            elif suffix == '.json':
                try:
                    custom_config = json.load(f)
                except json.JSONDecodeError as e:
                    ColorLog.error(f"JSON格式错误: {str(e)}")
                    raise
            else:
                ColorLog.error(f"不支持的配置文件格式: {suffix}")
                ColorLog.info("支持的格式: .json, .yaml, .yml")
                return config

        # 更新配置
        if not custom_config:
            ColorLog.warning(f"配置文件为空: {config_path}")
            return config

        if not isinstance(custom_config, dict):
            ColorLog.error(f"配置文件格式无效: 应为字典/对象格式，但得到了 {type(custom_config).__name__}")
            return config

        # 验证并更新配置
        if 'commit_types' in custom_config:
            if isinstance(custom_config['commit_types'], dict):
                config['commit_types'] = custom_config['commit_types']
            else:
                ColorLog.error(f"commit_types 应为字典格式，但得到了 {type(custom_config['commit_types']).__name__}")

        if 'default_type' in custom_config:
            config['default_type'] = custom_config['default_type']
            # 验证default_type是否在commit_types中
            if config['default_type'] not in config['commit_types']:
                ColorLog.warning(f"default_type '{config['default_type']}' 不在已定义的提交类型中")

        if 'header' in custom_config:
            config['header'] = custom_config['header']

        ColorLog.success(f"已成功加载配置: {config_path}")
        return config
    except Exception as e:
        ColorLog.error(f"加载配置文件失败: {e}")
        ColorLog.error(traceback.format_exc())
        ColorLog.info("使用内置默认配置")
        return config

def get_git_log(since: Optional[str] = None, until: Optional[str] = None) -> List[str]:
    """获取git日志。

    Args:
        since: 起始提交或标签
        until: 结束提交或标签

    Returns:
        List[str]: git日志条目
    """
    cmd = ["git", "log", "--pretty=format:%h %ad %s [%an]", "--date=short"]

    if since:
        cmd.append(f"{since}...")

    if until:
        cmd.append(f"...{until}")

    try:
        git_log = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.PIPE)
        return git_log.splitlines() if git_log else []
    except subprocess.CalledProcessError as e:
        ColorLog.error(f"获取git日志失败: {e}")
        ColorLog.error(f"命令: {' '.join(cmd)}")
        ColorLog.error(f"错误输出: {e.stderr if e.stderr else '无'}")
        return []

def get_latest_tag() -> Optional[str]:
    """获取最新的git标签。

    Returns:
        Optional[str]: 最新标签名称，如果没有则返回None
    """
    try:
        return subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            universal_newlines=True,
            stderr=subprocess.PIPE
        ).strip()
    except subprocess.SubprocessError as e:
        if hasattr(e, 'stderr') and e.stderr and "No names found" not in e.stderr:
            ColorLog.warning(f"获取最新标签失败: {e.stderr.strip()}")
        else:
            ColorLog.warning("仓库中没有标签")
        return None

def get_version_from_tag(tag: str) -> str:
    """从标签名提取版本号。

    Args:
        tag: 标签名称

    Returns:
        str: 版本号
    """
    if tag.startswith('v'):
        return tag[1:]
    return tag

def parse_commit(commit_line: str) -> Tuple[str, str, str, str, str]:
    """解析提交行。

    Args:
        commit_line: git log的一行输出

    Returns:
        Tuple[str, str, str, str, str]: (hash, date, type, scope, message)
    """
    # 解析hash和日期
    match = re.match(r"([a-f0-9]+) (\d{4}-\d{2}-\d{2}) (.*) \[(.*)\]", commit_line)
    if not match:
        return "", "", "", "", commit_line

    commit_hash, date, message, author = match.groups()

    # 解析类型和作用域
    type_match = re.match(r"([\w:]+)(?:\(([^)]+)\))?: (.*)", message)
    if type_match:
        commit_type, scope, msg = type_match.groups()
    else:
        commit_type, scope, msg = "", "", message

    return commit_hash, date, commit_type.lower(), scope or "", msg

def categorize_commits(commits: List[str], config: Dict[str, Any]) -> Dict[str, List[Tuple[str, str, str, str]]]:
    """将提交信息按类型分类。

    Args:
        commits: 提交信息列表
        config: 配置信息，包含提交类型映射

    Returns:
        Dict[str, List]: 按类型分类的提交信息
    """
    categorized = defaultdict(list)
    commit_types = config.get('commit_types', DEFAULT_COMMIT_TYPES)
    default_type = config.get('default_type', 'chore')

    for commit in commits:
        commit_hash, date, commit_type, scope, message = parse_commit(commit)
        if not commit_type:
            commit_type = default_type

        if commit_type in commit_types:
            categorized[commit_type].append((commit_hash, date, scope, message))
        else:
            categorized[default_type].append((commit_hash, date, scope, message))

    return categorized

def generate_markdown(categorized_commits: Dict, version: str, date: str, config: Dict[str, Any]) -> str:
    """生成Markdown格式的变更日志。

    Args:
        categorized_commits: 分类后的提交信息
        version: 版本号
        date: 发布日期
        config: 配置信息，包含提交类型映射

    Returns:
        str: Markdown格式的变更日志
    """
    commit_types = config.get('commit_types', DEFAULT_COMMIT_TYPES)
    markdown = f"## {version} ({date})\n\n"

    # 按照特定顺序显示提交类型
    # 首先，确保重要的更改类型（新功能、修复等）排在前面
    priority_types = ['feat', 'fix', 'perf', 'refactor']

    # 创建提交类型的有序列表
    ordered_types = []
    # 先添加优先类型
    for type_name in priority_types:
        if type_name in categorized_commits and categorized_commits[type_name]:
            ordered_types.append(type_name)

    # 然后添加其他类型
    for commit_type in categorized_commits:
        if commit_type not in ordered_types and categorized_commits[commit_type]:
            ordered_types.append(commit_type)

    # 按顺序生成Markdown
    for commit_type in ordered_types:
        commits = categorized_commits[commit_type]
        if not commits:
            continue

        type_name = commit_types.get(commit_type, "其他变更")
        markdown += f"### {type_name}\n\n"

        for commit_hash, _, scope, message in commits:
            scope_text = f"**{scope}:** " if scope else ""
            markdown += f"* {scope_text}{message} ({commit_hash})\n"

        markdown += "\n"

    return markdown

def update_changelog(changelog_content: str, new_content: str, config: Dict[str, Any]) -> str:
    """更新变更日志内容。

    Args:
        changelog_content: 现有的变更日志内容
        new_content: 新的变更日志内容
        config: 配置信息，包含header等

    Returns:
        str: 更新后的变更日志内容
    """
    header = config.get('header', "# 变更日志\n\n")

    if not changelog_content or changelog_content.strip() == header.strip() or changelog_content.strip() == "":
        return header + new_content

    # 提取头部（如果有）
    if changelog_content.startswith(header.strip()):
        # 在头部后面插入新内容
        parts = changelog_content.split("\n\n", 1)
        if len(parts) > 1:
            return parts[0] + "\n\n" + new_content + "\n\n" + parts[1]
        else:
            return parts[0] + "\n\n" + new_content
    else:
        # 没有标准头部，直接在前面加上
        return header + new_content + "\n\n" + changelog_content

def main():
    """主函数。"""
    parser = argparse.ArgumentParser(description="从git提交历史生成CHANGELOG")
    parser.add_argument("--output", default="CHANGELOG.md", help="输出文件路径")
    parser.add_argument("--since", help="起始提交或标签")
    parser.add_argument("--until", help="结束提交或标签")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    args = parser.parse_args()

    try:
        # 检查是否在git仓库中
        try:
            subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            ColorLog.error("当前目录不在git仓库中")
            return 1

        # 加载配置
        config = load_config(args.config)

        # 获取版本和日期
        today = datetime.now().strftime("%Y-%m-%d")

        if not args.until:
            # 如果没有指定结束标签，使用最新的标签或HEAD
            latest_tag = get_latest_tag()
            if latest_tag:
                version = get_version_from_tag(latest_tag)
                ColorLog.info(f"使用最新标签: {latest_tag} (版本: {version})")
            else:
                version = "未发布"
                ColorLog.info("未找到标签，使用'未发布'作为版本")
        else:
            version = get_version_from_tag(args.until)
            ColorLog.info(f"使用指定标签: {args.until} (版本: {version})")

        # 获取提交日志
        if args.verbose:
            ColorLog.info(f"获取提交记录 - 从: {args.since or '仓库起始'} 到: {args.until or 'HEAD'}")

        commits = get_git_log(args.since, args.until)
        if not commits:
            ColorLog.warning("未发现新的提交")
            return 0

        if args.verbose:
            ColorLog.info(f"找到 {len(commits)} 个提交")

        # 分类提交
        categorized = categorize_commits(commits, config)

        if args.verbose:
            for commit_type, commits in categorized.items():
                type_name = config['commit_types'].get(commit_type, "其他")
                ColorLog.info(f"类型 {commit_type} ({type_name}): {len(commits)} 个提交")

        # 生成Markdown
        new_content = generate_markdown(categorized, version, today, config)

        # 读取现有的CHANGELOG
        output_path = Path(args.output)
        if output_path.exists():
            try:
                existing_content = output_path.read_text(encoding="utf-8")
                if args.verbose:
                    ColorLog.info(f"已读取现有的CHANGELOG: {output_path}")
            except Exception as e:
                ColorLog.error(f"读取现有CHANGELOG失败: {e}")
                existing_content = ""
        else:
            if args.verbose:
                ColorLog.info(f"CHANGELOG文件不存在，将创建新文件: {output_path}")
            existing_content = ""

        # 更新CHANGELOG
        updated_content = update_changelog(existing_content, new_content, config)

        # 写入文件
        try:
            output_path.write_text(updated_content, encoding="utf-8")
            ColorLog.success(f"已更新 {args.output}")
            return 0
        except Exception as e:
            ColorLog.error(f"写入CHANGELOG失败: {e}")
            return 1

    except KeyboardInterrupt:
        ColorLog.warning("操作被用户中断")
        return 130
    except Exception as e:
        ColorLog.error(f"发生意外错误: {e}")
        ColorLog.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
