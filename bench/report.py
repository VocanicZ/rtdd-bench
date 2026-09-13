#!/usr/bin/env python3
"""Render collected variant metrics side by side.

  python3 bench/report.py results/tdd.json results/rtdd.json > RESULTS.md
"""
import json, re, sys

RUNNER = re.compile(r"\b(?:mvnw?|gradlew?|rtdd|pytest|go test|gotestsum)\b")

ROWS = [
    ("Wall clock (s)",            lambda d: d["wall_clock_s"], "lower"),
    ("Active time (s)",           lambda d: d["active_s"], "lower"),
    ("Time running tests (s)",    lambda d: d["test_seconds"], "lower"),
    ("Test share of active",      lambda d: f'{d["test_share_of_active"]:.1%}' if d["test_share_of_active"] else "-", None),
    ("Selector overhead (s)",     lambda d: d["selector_seconds"], "lower"),
    ("Test executions",           lambda d: d["test_runs"], "lower"),
    ("Selector queries",          lambda d: d["selector_queries"], None),
    ("Mean run (s)",              lambda d: d["mean_run_s"], "lower"),
    ("Slowest run (s)",           lambda d: d["slowest_run_s"], "lower"),
    ("Red->green cycles",         lambda d: d["red_green_cycles"], None),
    ("Failed runs",               lambda d: d["failed_runs"], None),
    ("Assistant turns",           lambda d: d["assistant_turns"], "lower"),
    ("Billable tokens",           lambda d: f'{d["billable_tokens"]:,}', "lower"),
    ("  output",                  lambda d: f'{d["tokens"]["output_tokens"]:,}', None),
    ("  cache write",             lambda d: f'{d["tokens"]["cache_creation_input_tokens"]:,}', None),
    ("  cache read",              lambda d: f'{d["tokens"]["cache_read_input_tokens"]:,}', None),
    ("  thinking",                lambda d: f'{d["tokens"]["thinking_tokens"]:,}', None),
    ("Tests in suite",            lambda d: d["project"]["tests_reported"], None),
    ("Test files / LOC",          lambda d: f'{d["project"]["test_files"]} / {d["project"]["test_loc"]}', None),
    ("Main files / LOC",          lambda d: f'{d["project"]["main_files"]} / {d["project"]["main_loc"]}', None),
    ("Commits",                   lambda d: d["project"]["commits"], None),
]


def main(paths):
    ds = [json.load(open(p)) for p in paths]
    labels = [d["label"] for d in ds]
    w = max(24, *(len(r[0]) for r in ROWS))

    print("# Benchmark results\n")
    print("| " + "Metric".ljust(w) + " | " + " | ".join(l.ljust(14) for l in labels) + " | Delta |")
    print("|" + "-" * (w + 2) + "|" + "|".join("-" * 16 for _ in labels) + "|-------|")

    for name, fn, better in ROWS:
        vals = []
        for d in ds:
            try:
                v = fn(d)
                vals.append("-" if v is None else v)
            except Exception:
                vals.append("-")
        delta = ""
        if better and len(ds) == 2:
            try:
                a, b = (float(str(v).replace(",", "")) for v in vals)
                if a:
                    pct = (b - a) / a * 100
                    delta = f"{pct:+.0f}%"
            except Exception:
                pass
        print("| " + name.ljust(w) + " | " + " | ".join(str(v).ljust(14) for v in vals) + f" | {delta} |")

    print("\n_Delta is the second variant relative to the first; negative is less._")

    for d in ds:
        r = d.get("rtdd")
        if not r:
            continue
        adapters = ", ".join(r["adapters"]) or "none"
        if not r["fidelity"].startswith("execution"):
            print(f"\n> **`{d['label']}` ran rtdd at `{r['fidelity']}` fidelity** ({adapters} adapter, "
                  f"{r['map_entries']} map entries). A static adapter records no coverage and builds no "
                  f"map, so tests were chosen from declared correspondence, not from a recorded run — "
                  f"rtdd's weakest tier. Read the selection deltas as static selection, not as the "
                  f"coverage-derived selection rtdd is built around.")
        else:
            print(f"\n> `{d['label']}` ran rtdd at `{r['fidelity']}` fidelity "
                  f"({adapters} adapter, {r['map_entries']} map entries).")
    print("\n## Test executions\n")
    for d in ds:
        print(f"### {d['label']}\n")
        for r in d["runs"]:
            mark = "FAIL" if r["failed"] else "pass"
            # show the line that ran the tests, not the heredoc it was bundled with
            lines = [l for l in r["command"].splitlines() if RUNNER.search(l)]
            cmd = " ".join((lines[-1] if lines else r["command"]).split())[:88]
            print(f"- `{cmd}` — {r['seconds']}s {mark}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
