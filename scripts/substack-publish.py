#!/usr/bin/env python3
"""Push a markdown article to Substack as a draft.

Converts markdown to Substack's ProseMirror JSON format and creates
a draft via the Substack API.
"""

import sys
import os
import re
import json
import requests
from dotenv import load_dotenv

# Check CoS config first, then fallback to ~/.claude
_COS_AUTH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", ".env")
_CLAUDE_AUTH = os.path.expanduser("~/.claude/substack-auth.env")
AUTH_FILE = _COS_AUTH if os.path.exists(_COS_AUTH) else _CLAUDE_AUTH
PUBLICATION = "cinderzhang"
BASE_URL = f"https://{PUBLICATION}.substack.com"


def parse_frontmatter(filepath):
    """Parse YAML frontmatter and return (metadata_dict, body_text)."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.startswith("---"):
        return {}, text

    end = text.find("---", 3)
    if end == -1:
        return {}, text

    fm_block = text[3:end].strip()
    body = text[end + 3:].strip()

    meta = {}
    for line in fm_block.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            val = val.strip().strip('"').strip("'")
            # Handle arrays like ["tag1", "tag2"]
            if val.startswith("["):
                val = [v.strip().strip('"').strip("'") for v in val.strip("[]").split(",")]
            meta[key.strip()] = val

    return meta, body


def md_to_prosemirror(md_text):
    """Convert markdown to Substack ProseMirror JSON (doc format).

    Handles: headings, bold, italic, bold+italic, links, blockquotes,
    horizontal rules, bullet lists, tables, and paragraphs.
    """
    lines = md_text.split("\n")
    content = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^---+\s*$", line.strip()):
            content.append({"type": "horizontal_rule"})
            i += 1
            continue

        # Heading
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            content.append({
                "type": "heading",
                "attrs": {"level": level},
                "content": parse_inline(text),
            })
            i += 1
            continue

        # Table (| ... | ... |)
        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            table_node = parse_table(table_lines)
            if table_node:
                content.append(table_node)
            continue

        # Bullet list
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                item_text = re.sub(r"^[-*]\s+", "", lines[i])
                items.append({
                    "type": "list_item",
                    "content": [{"type": "paragraph", "content": parse_inline(item_text)}],
                })
                i += 1
            content.append({"type": "bullet_list", "content": items})
            continue

        # Blockquote
        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].startswith(">"):
                quote_lines.append(lines[i].lstrip("> "))
                i += 1
            quote_text = " ".join(quote_lines)
            content.append({
                "type": "blockquote",
                "content": [{"type": "paragraph", "content": parse_inline(quote_text)}],
            })
            continue

        # Italic-only line (starts with * and ends with *)
        if line.startswith("*") and not line.startswith("**") and line.endswith("*") and not line.endswith("**"):
            inner = line.strip("*").strip()
            content.append({
                "type": "paragraph",
                "content": [{"type": "text", "marks": [{"type": "em"}], "text": inner}],
            })
            i += 1
            continue

        # Regular paragraph — collect consecutive non-empty, non-special lines
        para_lines = []
        while i < len(lines):
            l = lines[i]
            if not l.strip():
                break
            if re.match(r"^#{1,6}\s+", l):
                break
            if re.match(r"^---+\s*$", l.strip()):
                break
            if l.strip().startswith("|"):
                break
            if re.match(r"^[-*]\s+", l) and not l.startswith("**"):
                break
            if l.startswith(">"):
                break
            para_lines.append(l)
            i += 1

        if para_lines:
            text = " ".join(para_lines)
            inline = parse_inline(text)
            if inline:
                content.append({"type": "paragraph", "content": inline})

    return {"type": "doc", "content": content}


def parse_inline(text):
    """Parse inline markdown (bold, italic, links) into ProseMirror marks."""
    nodes = []
    # Pattern: links, bold+italic, bold, italic, or plain text
    pattern = re.compile(
        r"\[([^\]]+)\]\(([^)]+)\)"       # [text](url)
        r"|(\*\*\*(.+?)\*\*\*)"          # ***bold+italic***
        r"|(\*\*(.+?)\*\*)"              # **bold**
        r"|(\*(.+?)\*)"                  # *italic*
        r"|([^[*]+)"                      # plain text
    )

    for m in pattern.finditer(text):
        if m.group(1) is not None:
            # Link
            node = {"type": "text", "text": m.group(1),
                    "marks": [{"type": "link", "attrs": {"href": m.group(2)}}]}
            nodes.append(node)
        elif m.group(4) is not None:
            # Bold + italic
            nodes.append({"type": "text", "text": m.group(4),
                          "marks": [{"type": "strong"}, {"type": "em"}]})
        elif m.group(6) is not None:
            # Bold
            nodes.append({"type": "text", "text": m.group(6),
                          "marks": [{"type": "strong"}]})
        elif m.group(8) is not None:
            # Italic
            nodes.append({"type": "text", "text": m.group(8),
                          "marks": [{"type": "em"}]})
        elif m.group(9) is not None:
            # Plain text
            t = m.group(9)
            if t:
                nodes.append({"type": "text", "text": t})

    return nodes if nodes else [{"type": "text", "text": text}]


def parse_table(table_lines):
    """Convert markdown table lines to ProseMirror table node."""
    if len(table_lines) < 2:
        return None

    rows = []
    for idx, line in enumerate(table_lines):
        line = line.strip().strip("|")
        cells = [c.strip() for c in line.split("|")]

        # Skip separator row (|---|---|)
        if all(re.match(r"^[-:]+$", c) for c in cells):
            continue

        is_header = idx == 0
        cell_type = "table_header" if is_header else "table_cell"
        row_cells = []
        for cell in cells:
            row_cells.append({
                "type": cell_type,
                "content": [{"type": "paragraph", "content": parse_inline(cell)}],
            })
        rows.append({"type": "table_row", "content": row_cells})

    if not rows:
        return None

    return {"type": "table", "content": rows}


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
    meta, body = parse_frontmatter(filepath)
    title = meta.get("title", "Untitled")
    subtitle = meta.get("subtitle", "")

    # Convert to ProseMirror
    draft_body = md_to_prosemirror(body)
    content_blocks = len(draft_body.get("content", []))

    # Connect to Substack
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": f"substack.sid={cookie}",
        "Content-Type": "application/json",
    })

    # Get user ID from published posts
    user_id = None
    r_archive = session.get(f"{BASE_URL}/api/v1/archive?limit=1")
    if r_archive.status_code == 200 and r_archive.json():
        bylines = r_archive.json()[0].get("publishedBylines", [])
        if bylines:
            user_id = bylines[0].get("id")
    if not user_id:
        print("ERROR: Could not determine user_id from published posts")
        sys.exit(1)

    # Create draft
    draft_payload = {
        "draft_title": title,
        "draft_subtitle": subtitle,
        "draft_body": json.dumps(draft_body),
        "draft_bylines": [{"id": user_id, "is_guest": False}],
        "type": "newsletter",
        "audience": "everyone",
    }

    r = session.post(f"{BASE_URL}/api/v1/drafts", json=draft_payload)
    if r.status_code not in (200, 201):
        print(f"ERROR creating draft: {r.status_code} {r.text[:300]}")
        sys.exit(1)

    result = r.json()
    draft_id = result.get("id")

    # PUT to ensure body persists (Substack sometimes ignores body on POST)
    put_payload = {"draft_body": json.dumps(draft_body)}
    r2 = session.put(f"{BASE_URL}/api/v1/drafts/{draft_id}", json=put_payload)
    if r2.status_code not in (200, 201):
        print(f"WARNING: Draft created but PUT failed: {r2.status_code} {r2.text[:200]}")
        print(f"Check: {BASE_URL}/publish/post/{draft_id}")
        sys.exit(1)

    # Verify content was saved
    r3 = session.get(f"{BASE_URL}/api/v1/drafts/{draft_id}")
    saved = r3.json()
    saved_body = saved.get("draft_body", "")
    if isinstance(saved_body, str) and saved_body:
        saved_body = json.loads(saved_body)
    verified_blocks = len(saved_body.get("content", [])) if isinstance(saved_body, dict) else 0

    if verified_blocks > 0:
        print(f"Draft created ({verified_blocks} content blocks): {BASE_URL}/publish/post/{draft_id}")
    else:
        print(f"WARNING: Draft created but body may be empty. Check: {BASE_URL}/publish/post/{draft_id}")


if __name__ == "__main__":
    main()
