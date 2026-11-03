"""Token counter for a Claude Code session.

Reads a session log (~/.claude/projects/<project>/<session>.jsonl) and prints,
for every message you sent, how many tokens Claude read (input) and wrote
(output) while answering it.

Usage:
    python tools/token_counter.py              # newest session
    python tools/token_counter.py path/to/session.jsonl

Notes:
- One message from you can trigger several calls to the model (one per tool
  step). Each call re-reads the whole conversation, so "input" grows fast.
- "cached" is the part of the input that was re-read from cache (cheaper).
- The last row may be incomplete if Claude is still answering it.
"""

import json
import sys
from pathlib import Path


def newest_session():
    logs = Path.home().glob(".claude/projects/*/*.jsonl")
    return max(logs, key=lambda path: path.stat().st_mtime)


def message_text(entry):
    """Return the text you typed, or None if this entry is a tool result."""
    content = entry["message"]["content"]
    if isinstance(content, str):
        return content
    texts = [part["text"] for part in content if part.get("type") == "text"]
    if not texts:
        return None
    # Claude Code adds extra context blocks first; your text is the last one.
    return texts[-1]


def read_turns(path):
    turns = []  # one per message you sent
    for line in open(path, encoding="utf-8"):
        entry = json.loads(line)
        if entry.get("isSidechain"):
            continue  # subagent work, not this conversation

        if entry.get("type") == "user" and not entry.get("isMeta"):
            text = message_text(entry)
            if text is not None:
                turns.append({"text": text, "calls": {}})

        elif entry.get("type") == "assistant" and turns:
            message = entry["message"]
            usage = message.get("usage")
            if usage:
                # One reply is saved over several lines with the same id,
                # so store it by id to count it only once.
                turns[-1]["calls"][message["id"]] = usage
    return turns


def totals(calls):
    fresh = sum(u["input_tokens"] + u.get("cache_creation_input_tokens", 0) for u in calls)
    cached = sum(u.get("cache_read_input_tokens", 0) for u in calls)
    output = sum(u["output_tokens"] for u in calls)
    return fresh + cached, cached, output


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else newest_session()
    turns = read_turns(path)
    print(f"Session: {path.name}\n")
    print(f"{'#':>3}  {'Your message':<42} {'calls':>5} {'input':>10} {'cached':>10} {'output':>8}")
    print("-" * 84)

    all_input = all_cached = all_output = 0
    for number, turn in enumerate(turns, start=1):
        input_tokens, cached, output = totals(turn["calls"].values())
        all_input += input_tokens
        all_cached += cached
        all_output += output
        preview = " ".join(turn["text"].split())
        if len(preview) > 40:
            preview = preview[:39] + "…"
        print(f"{number:>3}  {preview:<42} {len(turn['calls']):>5} "
              f"{input_tokens:>10,} {cached:>10,} {output:>8,}")

    print("-" * 84)
    print(f"{'':>3}  {'Total':<42} {'':>5} {all_input:>10,} {all_cached:>10,} {all_output:>8,}")
    if turns:
        input_tokens, cached, output = totals(turns[-1]["calls"].values())
        print(f"\nLatest message so far: {input_tokens:,} input "
              f"({cached:,} cached), {output:,} output")


main()
