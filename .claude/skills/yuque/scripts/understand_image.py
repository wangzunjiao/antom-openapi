#!/usr/bin/env python3
"""
语雀文档图片理解脚本
使用 GLM-4.6V 模型理解和描述图片内容
"""

import os
import sys
import json
import requests
from pathlib import Path


def load_api_config():
    """
    从配置文件中加载 API Key
    优先级: 当前目录/.claude/settings.json > ~/.claude/settings.json
    需要 ANTHROPIC_BASE_URL 包含 antchat.alipay.com 才认为 key 可用

    Returns:
        str: api_key 或 None
    """
    search_paths = [
        Path.cwd() / ".claude" / "settings.json",
        Path.home() / ".claude" / "settings.json",
    ]

    for settings_path in search_paths:
        if settings_path.exists():
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

                # 检查 ANTHROPIC_BASE_URL 是否包含 antchat.alipay.com
                base_url = settings.get('env', {}).get('ANTHROPIC_BASE_URL', '')
                if 'antchat.alipay.com' in base_url:
                    api_key = settings.get('env', {}).get('ANTHROPIC_AUTH_TOKEN')
                    if api_key:
                        print(f"✓ 从 {settings_path} 加载 API Key", file=sys.stderr)
                        return api_key
            except Exception as e:
                print(f"读取配置文件 {settings_path} 失败: {e}", file=sys.stderr)
                continue

    return None


def understand_image(image_url, prompt="请详细描述一下这个图片的内容", api_key=None):
    """
    使用 GLM-4.6V 模型理解图片

    Args:
        image_url: 图片 URL 或 base64 数据
        prompt: 对图片的提问
        api_key: API 密钥,如果不提供则从配置文件加载

    Returns:
        str: 图片理解结果
    """
    if not api_key:
        api_key = load_api_config()
        if not api_key:
            return "错误: 无法获取 API Key。请确保在 .claude/settings.json 或 ~/.claude/settings.json 中配置了 ANTHROPIC_AUTH_TOKEN，且 ANTHROPIC_BASE_URL 包含 antchat.alipay.com"

    # 使用固定的 OpenAI 风格 API URL
    url = "https://antchat.alipay.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "GLM-4.6V",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": image_url
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "stream": False
    }

    try:
        print(f"→ 发送请求...", file=sys.stderr)
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        print(f"✓ 响应状态码: {response.status_code}", file=sys.stderr)

        response.raise_for_status()

        result = response.json()

        # 调试: 输出响应结构
        print(f"→ 响应键: {list(result.keys())}", file=sys.stderr)

        # 提取返回的内容
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0].get('message', {}).get('content', '')
            print(f"✓ 成功获取图片理解结果", file=sys.stderr)
            return content
        else:
            return f"错误: API 返回格式异常 - {json.dumps(result, ensure_ascii=False, indent=2)}"

    except requests.exceptions.RequestException as e:
        print(f"✗ 请求失败详情: {type(e).__name__}", file=sys.stderr)
        return f"错误: 请求失败 - {str(e)}"
    except Exception as e:
        print(f"✗ 异常: {type(e).__name__}", file=sys.stderr)
        return f"错误: {str(e)}"


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python understand_image.py <image_url> [prompt]", file=sys.stderr)
        print("示例: python understand_image.py 'https://example.com/image.jpg' '描述图片中的主要内容'", file=sys.stderr)
        sys.exit(1)

    image_url = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "请详细描述一下这个图片的内容"

    result = understand_image(image_url, prompt)
    print(result)


if __name__ == "__main__":
    main()
