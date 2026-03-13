#!/usr/bin/env python3
"""
Yuque URL Parser
Extracts namespace and slug from Yuque document URLs

Supports formats:
- https://yuque.com/{user}/{book}/{doc}
- https://yuque.antfin.com/{user}/{book}/{doc}
- https://www.yuque.com/{namespace}/{slug}
"""

import sys
import re
from urllib.parse import urlparse


def parse_yuque_url(url):
    """
    Parse Yuque URL to extract namespace and slug

    Args:
        url: Yuque document URL string

    Returns:
        dict: Contains 'namespace' and 'slug' keys, or error message
    """
    try:
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        parts = path.split('/')

        # Handle different URL formats
        if len(parts) == 3:
            # Format: user/book/doc
            user, book, doc = parts
            namespace = f"{user}/{book}"
            slug = doc
        elif len(parts) == 2:
            # Format: namespace/slug (less common)
            namespace, slug = parts
        else:
            return {
                'error': f'Invalid URL format. Expected 2-3 path segments, got {len(parts)}',
                'url': url
            }

        return {
            'namespace': namespace,
            'slug': slug,
            'url': url
        }

    except Exception as e:
        return {
            'error': str(e),
            'url': url
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_yuque_url.py <yuque_url>")
        print("\nExample:")
        print("  python parse_yuque_url.py 'https://yuque.antfin.com/aimoyu/kg7h1z/mw4dpwx835mx54zn'")
        sys.exit(1)

    url = sys.argv[1]
    result = parse_yuque_url(url)

    if 'error' in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    print(f"Namespace: {result['namespace']}")
    print(f"Slug: {result['slug']}")

    # Output in format easy to copy for tool calls
    print("\nFor yuque-mcp tool calls:")
    print(f"  namespace: \"{result['namespace']}\"")
    print(f"  slug: \"{result['slug']}\"")


if __name__ == '__main__':
    main()
