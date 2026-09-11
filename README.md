# rtdd-bench

An A/B of two agent workflows building the same Java project from the same prompt:
plain test-driven development against rtdd-guided test selection.

```
rtdd-bench/
  PROMPT.md        the prompt, identical for both runs
  ledger-tdd/      submodule — workspace for the /tdd session
  ledger-rtdd/     submodule — workspace for the /rtdd session
  bench/           collector and reporter
  results/         per-variant metrics.json
  RESULTS.md       rendered comparison
```

## How it measures

Nothing is instrumented and nothing is self-reported. Claude Code already writes every
API call's token usage and every tool call with timestamps to
`~/.claude/projects/<workspace-slug>/<session>.jsonl`. `bench/collect.py` reads those
transcripts, keeps the entries whose `cwd` is inside a variant's workspace, and derives:

| Metric | Derived from |
|---|---|
| Wall clock | last timestamp − first |
| Active time | sum of inter-event gaps, each capped at 120s, so idle time is excluded |
| Time running tests | duration of every Bash call matching a test-runner pattern |
| Selector overhead | duration of `rtdd which/status/explain/doctor` calls, which run no tests |
| Test executions | count of those same calls |
| Red→green cycles | fail→pass transitions across consecutive test runs |
| Tokens | summed `usage` per assistant message — input, output, cache read/write, thinking |
| Tests in suite | parsed from surefire / JUnit XML in the workspace |
| LOC and commits | measured from the checked-out artifact, not claimed |

A test run counts as failed if the tool result errored or the output matched a build
failure marker, so the cycle count does not depend on the agent narrating anything.

## Running it

The two variants run in **separate containers** and never share a filesystem, so neither
agent can see the harness or the other run. Clone each project repo on its own — not this
repo with `--recurse-submodules`, which would put both in one tree.

**Container A**

```
git clone https://github.com/VocanicZ/ledger-tdd.git && cd ledger-tdd
```
Invoke `/tdd`, paste the prompt from `PROMPT.md`.

**Container B**

```
git clone https://github.com/VocanicZ/ledger-rtdd.git && cd ledger-rtdd
```
Invoke `/rtdd`, paste the same prompt.

**Collect, in each container, once its session has ended.** `bench/collect.py` is a single
stdlib-only file — copy it in, or fetch it, and run it against the workspace:

```
python3 collect.py --workspace . --label tdd  > tdd.json     # container A
python3 collect.py --workspace . --label rtdd > rtdd.json    # container B
```

It must run *inside* the container: the transcripts live at `~/.claude/projects` there, and
the test count and LOC are measured from the workspace on disk. Copy both JSON files into
`results/` on the host and render:

```
bench/run.sh
```

If instead you copy the raw transcripts out of a container, collect on the host with the
path the session actually used in there:

```
python3 bench/collect.py --workspace . --label tdd   --transcripts ./copied-projects --cwd-prefix /workspace/ledger-tdd > results/tdd.json
```

Project stats (test count, LOC, commits) are reported as unavailable in that mode, since
the workspace is not present.

If a workspace saw more than one session (a resume or a retry), the collector warns and you
pin the one you meant:

```
python3 collect.py --workspace . --label x --list
python3 collect.py --workspace . --label tdd --session <id> > tdd.json
```

## Reading the result honestly

- **Cache reads dominate token totals** and are billed differently from fresh input, so
  compare `billable_tokens` (input + output + cache write) and the cache-read line separately.
- **Active time is the fairer clock.** Wall clock includes however long the terminal sat
  idle between your turns.
- **One trial is an anecdote.** Run the pair several times before believing a delta;
  these sessions are not deterministic.
- **The two variants must not see each other.** Run them in separate containers, cloning
  each project repo directly. The submodule wiring here is only so this repo pins which
  commit of each variant a given result set refers to.
