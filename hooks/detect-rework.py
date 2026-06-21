#!/usr/bin/env python3
"""
never-again — automatic rework detector (Stop hook).

Scans the just-finished session transcript for high-signal "we made an avoidable
mistake" patterns and stages 0-3 candidate lessons into the INBOX for the model to
review next session. Detection is automatic; phrasing + approval stay with the model
and user. Zero network, zero API, zero DB — just reads the transcript and appends
markdown. Fails open (silent exit) on anything unexpected so it can never block a stop.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
INBOX = os.path.join(HOME, ".claude", "never-again", "INBOX.md")
LEDGER = os.path.join(HOME, ".claude", "never-again", "LESSONS.md")
MAX_CANDIDATES = 3
TAIL_MESSAGES = 60  # only look at the recent part of the session

# Conservative, high-precision rework phrases (EN + ES). Precision over recall: a
# missed lesson is cheap; a noisy false positive erodes trust in the inbox.
CORRECTION_RE = re.compile(
    r"(?i)\b("
    r"no,|nope\b|that'?s wrong|that is wrong|that'?s not right|"
    r"revert|roll ?back|undo that|you (keep|again)|again you|"
    r"don'?t do that|stop doing|that broke|broke (it|the)|you broke|"
    r"not what i (asked|wanted|said)|wrong again|"
    r"otra vez|revert[ií]|revertilo|est[áa] mal|eso est[áa] mal|"
    r"no era eso|no es lo que ped[íi]|te equivocaste|de nuevo el"
    r")\b"
)


def log_exit():
    sys.exit(0)


def read_stdin_json():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def iter_messages(transcript_path):
    """Yield (role, text, tool_uses, tool_results) per transcript line, defensively."""
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception:
        return
    for line in lines[-TAIL_MESSAGES * 2:]:  # generous slice; refined below
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        msg = obj.get("message", obj)
        role = msg.get("role") or obj.get("type") or ""
        content = msg.get("content")
        text_parts, tool_uses, tool_results = [], [], []
        if isinstance(content, str):
            text_parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "text" and block.get("text"):
                    text_parts.append(block["text"])
                elif btype == "tool_use":
                    tool_uses.append(block)
                elif btype == "tool_result":
                    tool_results.append(block)
        yield role, " ".join(text_parts), tool_uses, tool_results


def collect_signals(transcript_path):
    msgs = list(iter_messages(transcript_path))[-TAIL_MESSAGES:]
    candidates = []

    # 1) User corrections — the strongest signal that Claude got something wrong.
    for role, text, _tu, tres in msgs:
        if role != "user" or not text or tres:
            continue  # skip tool-result-carrying user turns; we want genuine human turns
        m = CORRECTION_RE.search(text)
        if m:
            snippet = " ".join(text.split())[:160]
            candidates.append(("correction", snippet))

    # 2) Same file edited 3+ times — churn usually means a wrong first approach.
    edit_counts = {}
    for role, _t, tool_uses, _tr in msgs:
        for tu in tool_uses:
            if tu.get("name") in ("Edit", "Write", "NotebookEdit"):
                fp = (tu.get("input") or {}).get("file_path") or (tu.get("input") or {}).get("notebook_path")
                if fp:
                    edit_counts[fp] = edit_counts.get(fp, 0) + 1
    for fp, n in edit_counts.items():
        if n >= 3:
            candidates.append(("rework", f"{os.path.basename(fp)} edited {n}x in one session — likely a wrong first approach"))

    # 3) A tool/command errored — possible avoidable failure.
    for role, _t, _tu, tres in msgs:
        for tr in tres:
            if tr.get("is_error"):
                c = tr.get("content")
                if isinstance(c, list):
                    c = " ".join(b.get("text", "") for b in c if isinstance(b, dict))
                c = " ".join(str(c or "").split())[:140]
                if c:
                    candidates.append(("error", c))

    return candidates


def existing_keys():
    keys = set()
    for path in (LEDGER, INBOX):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for ln in f:
                    keys.add(re.sub(r"[^a-z0-9]", "", ln.lower())[:40])
        except Exception:
            pass
    return keys


def main():
    data = read_stdin_json()
    if data.get("stop_hook_active"):
        log_exit()  # avoid feedback loops
    tpath = data.get("transcript_path") or ""
    if not tpath or not os.path.isfile(tpath):
        log_exit()

    cwd = data.get("cwd") or os.getcwd()
    candidates = collect_signals(tpath)
    if not candidates:
        log_exit()

    seen = existing_keys()
    fresh, used = [], set()
    for kind, snippet in candidates:
        key = re.sub(r"[^a-z0-9]", "", snippet.lower())[:40]
        if not key or key in seen or key in used:
            continue
        used.add(key)
        fresh.append((kind, snippet))
        if len(fresh) >= MAX_CANDIDATES:
            break
    if not fresh:
        log_exit()

    os.makedirs(os.path.dirname(INBOX), exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    header_needed = not os.path.isfile(INBOX)
    try:
        with open(INBOX, "a", encoding="utf-8") as f:
            if header_needed:
                f.write("# never-again — INBOX (auto-detected candidates)\n\n"
                        "> Review with the `never-again` skill: turn the real ones into one-line lessons,\n"
                        "> discard the noise, then delete them from here. These are signals, not lessons yet.\n\n")
            f.write(f"## {stamp} — from `{cwd}`\n")
            for kind, snippet in fresh:
                f.write(f"- [ ] ({kind}) {snippet}\n")
            f.write("\n")
    except Exception:
        pass
    log_exit()


if __name__ == "__main__":
    main()
