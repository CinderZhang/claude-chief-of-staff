#!/usr/bin/env bash
# Tavily web search wrapper
# Usage: tavily-search.sh "search query" [max_results]
# Reads TAVILY_API_KEY from ~/.claude/substack-auth.env

set -euo pipefail

QUERY="${1:?Usage: tavily-search.sh \"search query\" [max_results]}"
MAX_RESULTS="${2:-5}"
AUTH_FILE="$HOME/.claude/substack-auth.env"

if [ ! -f "$AUTH_FILE" ]; then
    echo "Error: $AUTH_FILE not found" >&2
    exit 1
fi

source "$AUTH_FILE"

if [ -z "${TAVILY_API_KEY:-}" ]; then
    echo "Error: TAVILY_API_KEY not set in $AUTH_FILE" >&2
    exit 1
fi

curl -s -X POST "https://api.tavily.com/search" \
    -H "Content-Type: application/json" \
    -d "{\"api_key\": \"$TAVILY_API_KEY\", \"query\": \"$QUERY\", \"max_results\": $MAX_RESULTS, \"search_depth\": \"advanced\"}"
