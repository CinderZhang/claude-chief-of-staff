#!/usr/bin/env python3
"""Push a markdown article to Substack as a draft."""

import sys
import os
from dotenv import load_dotenv
import frontmatter
from substack import Api
from substack.post import Post

AUTH_FILE = os.path.expanduser("~/.claude/substack-auth.env")
PUBLICATION = "cinderzhang"

def main():
    if len(sys.argv) < 2:
        print("Usage: substack-publish.py <markdown-file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    # Load auth
    if not os.path.exists(AUTH_FILE):
        print(f"Auth file missing: {AUTH_FILE}")
        print("Create it with: SUBSTACK_COOKIE=your_substack_sid_value")
        sys.exit(1)

    load_dotenv(AUTH_FILE)
    cookie = os.getenv("SUBSTACK_COOKIE")
    if not cookie:
        print("SUBSTACK_COOKIE not set in auth file")
        sys.exit(1)

    # Parse markdown
    fm = frontmatter.load(filepath)
    title = fm.get("title", "Untitled")
    subtitle = fm.get("subtitle", "")

    # Connect to Substack
    api = Api(cookies_string=f"substack.sid={cookie}")
    user_id = api.get_user_id()

    # Build post using Post class with markdown conversion
    post = Post(title=title, subtitle=subtitle, user_id=user_id, audience="everyone")
    post.from_markdown(fm.content, api=api)

    # Push as draft (POST creates shell, PUT sets body content)
    draft_data = post.get_draft()
    result = api.post_draft(draft_data)
    draft_id = result.get("id")

    # Substack ignores draft_body on POST — must PUT to persist content
    api.put_draft(draft_id, draft_body=draft_data["draft_body"])

    # Verify content was saved
    saved = api.get_draft(draft_id)
    body = saved.get("draft_body", "")
    import json
    if isinstance(body, str):
        body = json.loads(body)
    content_blocks = len(body.get("content", [])) if isinstance(body, dict) else 0

    if content_blocks > 0:
        print(f"Draft created ({content_blocks} content blocks): https://{PUBLICATION}.substack.com/publish/post/{draft_id}")
    else:
        print(f"WARNING: Draft created but body may be empty. Check: https://{PUBLICATION}.substack.com/publish/post/{draft_id}")

if __name__ == "__main__":
    main()
