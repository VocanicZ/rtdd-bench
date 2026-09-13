#!/usr/bin/env python3
"""Extract session metrics for one benchmark variant from Claude Code transcripts.

Everything is derived from ~/.claude/projects/**/*.jsonl, which records every API
call's token usage and every tool call with timestamps. Nothing depends on the
agent self-reporting, and no shim or PATH manipulation is involved.

  python3 bench/collect.py --workspace ledger-tdd --label tdd > results/tdd.json
"""
import argparse, datetime as dt, glob, json, os, re, subprocess, sys
from collections import Counter

# A gap longer than this between two events is human think time, not work.
IDLE_CAP_S = 120.0

# Commands that actually execute tests.
TEST_EXEC = re.compile(
    # the runner may be invoked by path -- ./mvnw, ~/.local/bin/mvn, /usr/bin/gradle
    r"(?:^|[;&|]\s*|\s)[\w./~-]*(?:mvnw?|gradlew?)\b[^;&|]*\b(?:test|verify|check)\b"
    r"|(?:^|[;&|]\s*|\s)rtdd\s+(?:run|verify|seed)\b",
    re.I,
)
# rtdd queries that run no tests -- the selector's own overhead.
SELECTOR_QUERY = re.compile(r"(?:^|[;&|]\s*|\s)rtdd\s+(?:which|status|explain|doctor|map)\b", re.I)

# A bare "failed" is not a marker: rtdd run reports "5 ran, 0 failed" on success.
FAIL_MARKERS = re.compile(
    r"BUILD FAILURE|Tests run:.*?Failures: [1-9]|Tests run:.*?Errors: [1-9]"
    r"|FAILURES!|There are test failures"
    r"|\b[1-9]\d* (?:tests? )?failed\b"
    r"|(?-i:\bFAILED\b)",
    re.I,
)


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def text_of(block):
    c = block.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(p.get("text", "") for p in c if isinstance(p, dict))
    return ""


def scan(since=None, until=None, transcripts=None):
    """Every transcript entry grouped by session, plus each entry's cwd."""
    home = os.path.expanduser(transcripts or "~/.claude/projects")
    by_session = {}
    for f in glob.glob(f"{home}/*/*.jsonl"):
        with open(f, errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if not (d.get("timestamp") and d.get("sessionId")):
                    continue
                if since and d["timestamp"] < since:
                    continue
                if until and d["timestamp"] > until:
                    continue
                by_session.setdefault(d["sessionId"], []).append(d)
    return by_session


def in_workspace(d, ws):
    cwd = d.get("cwd")
    if not cwd:
        return False
    cands = {cwd, os.path.realpath(cwd)} if os.path.exists(cwd) else {cwd}
    return any(c == ws or c.startswith(ws + os.sep) for c in cands)


def rank_sessions(workspace, since=None, until=None, transcripts=None,
                  cwd_prefix=None):
    """Sessions that worked in this workspace, most entries there first.

    A session is filed under the cwd it started in, which is not always the
    workspace: a session launched at the bench root and then working inside a
    submodule lands under the root's slug. So every transcript is read and
    scored by cwd instead of trusting the directory name."""
    ws = cwd_prefix or os.path.realpath(workspace)
    by_session = scan(since, until, transcripts)
    scores = Counter({s: sum(1 for d in ds if in_workspace(d, ws)) for s, ds in by_session.items()})
    ranked = [(s, n) for s, n in scores.most_common() if n]
    return ranked, by_session


def load_entries(workspace, session=None, since=None, until=None,
                 transcripts=None, cwd_prefix=None):
    """The whole of the session that worked in this workspace, in time order.

    Entries of that session whose cwd is the parent directory are kept: the run
    opens there, and dropping those turns would lose their time and tokens."""
    ranked, by_session = rank_sessions(workspace, since, until, transcripts, cwd_prefix)
    if session:
        chosen = session
    elif not ranked:
        return []
    else:
        chosen = ranked[0][0]
        if len(ranked) > 1:
            others = ", ".join(f"{s} ({n})" for s, n in ranked[1:])
            print(f"warning: {len(ranked)} sessions worked in {workspace}; using "
                  f"{chosen} ({ranked[0][1]} entries there). Others: {others}. "
                  f"Pin one with --session <id>.", file=sys.stderr)
    return sorted(by_session.get(chosen, []), key=lambda d: d["timestamp"])


def collect(workspace, label, session=None, since=None, until=None,
            transcripts=None, cwd_prefix=None):
    entries = load_entries(workspace, session, since, until, transcripts, cwd_prefix)
    if not entries:
        sys.exit(
            f"no transcript entries with cwd under {cwd_prefix or os.path.realpath(workspace)}\n"
            f"  transcripts searched: {os.path.expanduser(transcripts or '~/.claude/projects')}\n"
            f"  if the session ran elsewhere (another container), pass --cwd-prefix "
            f"with the path it used there")
    sessions = sorted({d.get("sessionId") for d in entries if d.get("sessionId")})
    if len(sessions) > 1 and not session:
        print(f"warning: {len(sessions)} sessions in this workspace; "
              f"pin one with --session <id>", file=sys.stderr)

    tok = Counter()
    turns = 0
    tools = Counter()
    models = Counter()
    pending = {}        # tool_use_id -> (timestamp, command)
    runs = []           # executed test runs
    queries = []        # selector queries

    for d in entries:
        m = d.get("message") or {}
        if d.get("type") == "assistant":
            u = m.get("usage") or {}
            if u:
                turns += 1
                models[m.get("model", "?")] += 1
                for k in ("input_tokens", "output_tokens",
                          "cache_read_input_tokens", "cache_creation_input_tokens"):
                    tok[k] += u.get(k) or 0
                tok["thinking_tokens"] += (u.get("output_tokens_details") or {}).get("thinking_tokens") or 0

        content = m.get("content")
        if not isinstance(content, list):
            continue
        for b in content:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_use":
                tools[b.get("name", "?")] += 1
                if b.get("name") == "Bash":
                    pending[b["id"]] = (d["timestamp"], (b.get("input") or {}).get("command", ""))
            elif b.get("type") == "tool_result" and b.get("tool_use_id") in pending:
                t0, cmd = pending.pop(b["tool_use_id"])
                dur = (ts(d["timestamp"]) - ts(t0)).total_seconds()
                body = text_of(b)
                rec = {
                    "command": cmd,
                    "seconds": round(dur, 2),
                    "failed": bool(b.get("is_error")) or bool(FAIL_MARKERS.search(body)),
                    "at": t0,
                }
                if TEST_EXEC.search(cmd):
                    runs.append(rec)
                elif SELECTOR_QUERY.search(cmd):
                    queries.append(rec)

    # Red -> green transitions across consecutive test executions.
    cycles, prev_failed = 0, False
    for r in runs:
        if prev_failed and not r["failed"]:
            cycles += 1
        prev_failed = r["failed"]

    stamps = [ts(d["timestamp"]) for d in entries]
    wall = (stamps[-1] - stamps[0]).total_seconds()
    active = sum(min((b - a).total_seconds(), IDLE_CAP_S) for a, b in zip(stamps, stamps[1:]))
    test_s = sum(r["seconds"] for r in runs)
    query_s = sum(q["seconds"] for q in queries)

    billable = tok["input_tokens"] + tok["output_tokens"] + tok["cache_creation_input_tokens"]

    return {
        "label": label,
        "workspace": os.path.realpath(workspace),
        "sessions": sessions,
        "started": entries[0]["timestamp"],
        "ended": entries[-1]["timestamp"],
        "models": dict(models),
        "wall_clock_s": round(wall, 1),
        "active_s": round(active, 1),
        "test_seconds": round(test_s, 1),
        "selector_seconds": round(query_s, 1),
        "test_share_of_active": round(test_s / active, 3) if active else None,
        "test_runs": len(runs),
        "selector_queries": len(queries),
        "failed_runs": sum(1 for r in runs if r["failed"]),
        "red_green_cycles": cycles,
        "mean_run_s": round(test_s / len(runs), 2) if runs else None,
        "slowest_run_s": max((r["seconds"] for r in runs), default=None),
        "assistant_turns": turns,
        "tokens": dict(tok),
        "billable_tokens": billable,
        "tool_calls": dict(tools.most_common()),
        "project": project_stats(workspace),
        "rtdd": rtdd_state(workspace),
        "runs": runs,
    }


def rtdd_state(ws):
    """How rtdd was set up here, so the report can label its own fidelity.

    A static adapter records no coverage and builds no map, so its selection is
    derived from declared correspondence rather than from a recorded run. That
    is a weaker claim and the report has to say so."""
    cfg = os.path.join(ws, ".rtdd", "config.yaml")
    if not os.path.exists(cfg):
        return None
    text = open(cfg, errors="replace").read()
    fidelity = re.findall(r"^\s*fidelity:\s*(\S+)", text, re.M)
    mapfile = os.path.join(ws, ".rtdd", "map.jsonl")
    return {
        "adapters": re.findall(r"^\s*-?\s*name:\s*(\S+)", text, re.M),
        "fidelity": fidelity[0] if fidelity else "unknown",
        "map_entries": sum(1 for _ in open(mapfile, errors="replace")) if os.path.exists(mapfile) else 0,
    }


def project_stats(ws):
    """Test count and repo size, measured from the artifact rather than claimed."""
    if not os.path.isdir(ws):
        return {"unavailable": f"{ws} not present; collect inside the container "
                               f"where the session ran to get these"}

    def sh(*a):
        try:
            return subprocess.run(a, cwd=ws, capture_output=True, text=True, timeout=30).stdout.strip()
        except Exception:
            return ""

    tests = suites = 0
    for x in glob.glob(f"{ws}/**/surefire-reports/*.xml", recursive=True) + \
             glob.glob(f"{ws}/**/test-results/**/*.xml", recursive=True):
        try:
            import xml.etree.ElementTree as ET
            r = ET.parse(x).getroot()
            if r.tag == "testsuite":
                tests += int(r.get("tests", 0)); suites += 1
        except Exception:
            pass

    src = glob.glob(f"{ws}/**/src/main/**/*.java", recursive=True)
    tst = glob.glob(f"{ws}/**/src/test/**/*.java", recursive=True)
    loc = lambda fs: sum(sum(1 for _ in open(f, errors="replace")) for f in fs)

    return {
        "tests_reported": tests,
        "test_suites": suites,
        "main_files": len(src),
        "test_files": len(tst),
        "main_loc": loc(src),
        "test_loc": loc(tst),
        "commits": len([l for l in sh("git", "log", "--oneline").splitlines() if l]),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--workspace", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--session", help="sessionId to pin (see --list)")
    p.add_argument("--since", help="ISO timestamp lower bound")
    p.add_argument("--until", help="ISO timestamp upper bound")
    p.add_argument("--transcripts", help="transcript root (default ~/.claude/projects)")
    p.add_argument("--cwd-prefix", help="match this cwd instead of the workspace's real path, "
                                        "for transcripts copied out of another machine")
    p.add_argument("--list", action="store_true", help="list sessions and exit")
    a = p.parse_args()
    if a.list:
        ranked, by_session = rank_sessions(a.workspace, a.since, a.until,
                                           a.transcripts, a.cwd_prefix)
        for sid, n in ranked:
            ds = by_session[sid]
            print(f"{sid}  first={ds[0]['timestamp']}  entries={len(ds)}  in-workspace={n}")
        sys.exit(0)
    json.dump(collect(a.workspace, a.label, a.session, a.since, a.until,
                      a.transcripts, a.cwd_prefix), sys.stdout, indent=2)
    print()
