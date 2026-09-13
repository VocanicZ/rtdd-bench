#!/usr/bin/env python3
"""Roll every collected project up into one table.

  python3 bench/summary.py > RESULTS.md

Reads results/<example>/<project>/{tdd,rtdd}.json -- whatever has been collected so
far -- and gives each project one row. The rtdd fidelity tier rides along in the last
column, so a `static` row is never mistaken for the coverage-derived selection rtdd
is actually about.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HEAD = ["Project", "Test executions", "Time in tests", "Billable tokens",
        "Red->green", "Fidelity"]


def pct(a, b):
    """rtdd relative to tdd; negative is less."""
    return f"{(b - a) / a * 100:+.0f}%" if a else "-"


def row(name, tdd, rtdd):
    return [
        f"[{name}](examples/{name}/RESULTS.md)",
        pct(tdd["test_runs"], rtdd["test_runs"]),
        pct(tdd["test_seconds"], rtdd["test_seconds"]),
        pct(tdd["billable_tokens"], rtdd["billable_tokens"]),
        f'{tdd["red_green_cycles"]} -> {rtdd["red_green_cycles"]}',
        (rtdd.get("rtdd") or {}).get("fidelity", "-"),
    ]


def pairs(root=ROOT):
    for d in sorted((root / "results").glob("*/*")):
        a, b = d / "tdd.json", d / "rtdd.json"
        if a.is_file() and b.is_file():
            yield (f"{d.parent.name}/{d.name}",
                   json.loads(a.read_text()), json.loads(b.read_text()))


def table(rows):
    w = [max(len(str(r[i])) for r in [HEAD] + rows) for i in range(len(HEAD))]
    out = ["| " + " | ".join(h.ljust(w[i]) for i, h in enumerate(HEAD)) + " |",
           "|" + "|".join("-" * (n + 2) for n in w) + "|"]
    out += ["| " + " | ".join(str(c).ljust(w[i]) for i, c in enumerate(r)) + " |"
            for r in rows]
    return "\n".join(out)


def render(root=ROOT):
    rows = [row(*p) for p in pairs(root)]
    if not rows:
        return "# Benchmark results\n\nNothing collected yet.\n"
    body = ["# Benchmark results\n",
            "One row per project: the same task, the same stack, `/tdd` against `/rtdd`. "
            "Percentages are rtdd relative to tdd, so negative is less. Each project links "
            "to its full table.\n",
            table(rows)]
    if any(r[-1] != "execution" for r in rows):
        body.append(
            "\n> Rows below `execution` fidelity ran rtdd against an adapter that records no "
            "coverage and builds no map (maven is one), so their tests were chosen from declared "
            "correspondence rather than from a recorded run. Read those selection deltas as "
            "static selection.")
    body.append("\n_One trial is an anecdote; these sessions are not deterministic._")
    return "\n".join(body) + "\n"


def demo():
    import tempfile
    def blob(runs, secs, toks, cycles, fid=None):
        d = {"test_runs": runs, "test_seconds": secs, "billable_tokens": toks,
             "red_green_cycles": cycles}
        if fid:
            d["rtdd"] = {"fidelity": fid}
        return d

    assert pct(36, 18) == "-50%"
    assert pct(100, 139) == "+39%"
    assert pct(0, 5) == "-"
    r = row("ledger/java-maven", blob(36, 100.2, 235186, 11),
            blob(18, 50.6, 325779, 6, "static"))
    assert r[1:] == ["-50%", "-50%", "+39%", "11 -> 6", "static"], r
    assert r[0] == "[ledger/java-maven](examples/ledger/java-maven/RESULTS.md)"

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        assert "Nothing collected yet" in render(root)
        d = root / "results/ledger/python"
        d.mkdir(parents=True)
        (d / "tdd.json").write_text(json.dumps(blob(20, 40.0, 100, 8)))
        (d / "rtdd.json").write_text(json.dumps(blob(10, 12.0, 112, 5, "execution")))
        # a half-collected project is skipped rather than crashing the roll-up
        (root / "results/ledger/go").mkdir(parents=True)
        (root / "results/ledger/go/tdd.json").write_text(json.dumps(blob(1, 1, 1, 1)))
        out = render(root)
        assert "ledger/python" in out and "ledger/go" not in out, out
        assert "-70%" in out and "execution" in out
        assert "static selection" not in out, "no sub-execution row, so no caveat"
    print("summary.py ok")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        demo()
    else:
        sys.stdout.write(render())
