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

1. Start a session in `ledger-tdd/`, invoke `/tdd`, paste the prompt from `PROMPT.md`.
2. Start a session in `ledger-rtdd/`, invoke `/rtdd`, paste the same prompt.
3. When both finish: `bench/run.sh`

If a workspace saw more than one session (a resume or a retry), the collector warns and
you pin the one you meant:

```
python3 bench/collect.py --workspace ledger-tdd --label x --list
bench/run.sh <tdd-session-id> <rtdd-session-id>
```

## Reading the result honestly

- **Cache reads dominate token totals** and are billed differently from fresh input, so
  compare `billable_tokens` (input + output + cache write) and the cache-read line separately.
- **Active time is the fairer clock.** Wall clock includes however long the terminal sat
  idle between your turns.
- **One trial is an anecdote.** Run the pair several times before believing a delta;
  these sessions are not deterministic.
- **The two variants must not see each other.** Each session opens its own submodule and
  nothing above it.
