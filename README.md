# rtdd-bench

[RESULTS](RESULTS.md)

An A/B of two agent workflows building the same project from the same prompt: plain
test-driven development against rtdd-guided test selection. One example is one task;
each example is built in several stacks, and each stack runs the pair.

```
rtdd-bench/
  examples/
    ledger/
      PROMPT.md              the task, identical for every stack under it
      java-maven/
        STACK.md             the stack constraint, appended to the task
        tdd/                 submodule — workspace for the /tdd session
        rtdd/                submodule — workspace for the /rtdd session
        RESULTS.md           rendered comparison for this project
      python/  go/           same shape
    cron-parser/  ...
  bench/          collector, reporter, roll-up, prompt assembler
  results/<example>/<project>/{tdd,rtdd}.json
  RESULTS.md      roll-up, one row per project
```

The task text lives once per example and the stack constraint once per project, so
every stack of an example is driven by provably identical task wording.
`bench/prompt.py --write` assembles the two and plants the result as `PROMPT.md` in
each workspace, printing a digest per file — the pair shares one digest, so the two
variants are identical by construction rather than by careful pasting. Commit and push
that file before running a session; the agent reads it from its own clone.

```
bench/prompt.py ledger/python            print it
bench/prompt.py --write ledger/python    plant it in tdd/ and rtdd/
bench/prompt.py --write                  ... for every checked-out project
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

## Running one project

The two variants run in **separate containers** and never share a filesystem, so neither
agent can see the harness or the other run. Clone each variant repo on its own — not this
repo with `--recurse-submodules`, which would put both in one tree.

Starting a session one directory up and pointing the skill at the workspace works too: the
collector picks the session by where its turns actually ran, not by where it was launched.

Clone into a neutrally named directory so the variant is not in the shell prompt:

```
git clone https://github.com/VocanicZ/<example>-<stack>-tdd.git work && cd work    # container A
git clone https://github.com/VocanicZ/<example>-<stack>-rtdd.git work && cd work   # container B
```

Each clone already contains its `PROMPT.md`. Send two messages, and the only difference
between the containers is the first one:

```
/tdd          (container A)   or   /rtdd   (container B)
@PROMPT.md
```

Two messages, not one line: a slash command takes the rest of the line as its arguments,
so `/tdd @PROMPT.md` risks the mention being passed as an argument instead of expanded.
The `@` mention inlines the file rather than making the agent read it, so no tool call
separates the two variants' opening turns.

Container A needs the `/tdd` skill installed in the image; container B gets the `/rtdd`
skill from the workspace itself, planted by `rtdd init`, and needs `rtdd` on PATH. Run
`rtdd doctor` there before starting and confirm it reports `execution-derived`.

Nothing else in the message. Do not mention the benchmark, the other variant, or any
metric to the agent, and do not steer mid-session; everything is measured afterwards
from the transcript.

**Collect, in each container, once its session has ended.** `bench/collect.py` is a single
stdlib-only file. Fetch it (this repo is private, so via the API rather than a raw URL):

```
gh api repos/VocanicZ/rtdd-bench/contents/bench/collect.py -q .content | base64 -d > collect.py
```

or `docker cp` it in. Then run it against the workspace:

```
python3 collect.py --workspace . --label tdd  > tdd.json     # container A
python3 collect.py --workspace . --label rtdd > rtdd.json    # container B
```

It must run *inside* the container: the transcripts live at `~/.claude/projects` there, and
the test count and LOC are measured from the workspace on disk. Copy both JSON files into
`results/<example>/<project>/` on the host and render:

```
bench/run.sh                      # every project with results, plus the roll-up
bench/run.sh ledger/java-maven    # just one
```

If instead you copy the raw transcripts out of a container, collect on the host with the
path the session actually used in there:

```
python3 bench/collect.py --workspace . --label tdd --transcripts ./copied-projects \
  --cwd-prefix /workspace/ledger-tdd > results/ledger/java-maven/tdd.json
```

Project stats (test count, LOC, commits) are reported as unavailable in that mode, since
the workspace is not present.

If a workspace saw more than one session (a resume or a retry), the collector warns and you
pin the one you meant:

```
python3 collect.py --workspace . --label x --list
bench/run.sh ledger/java-maven <tdd-session-id> <rtdd-session-id>
```

## Adding a project

1. `mkdir -p examples/<example>/<project>` and write its `STACK.md`. A new example also
   needs a stack-free `PROMPT.md` beside its projects.
2. Create the two variant repos, each holding only the stack manifest, and add them as
   submodules at `examples/<example>/<project>/{tdd,rtdd}`.
3. In the rtdd workspace run `rtdd init`, then `rtdd doctor`. **If it does not report
   `execution-derived`, stop** — that stack cannot measure selection, and the run would
   report prompt discipline instead. Commit `.rtdd/` and the skill files it plants.
4. `bench/prompt.py --write <example>/<project>`, then commit and push `PROMPT.md` in
   both workspaces.
5. Run the pair, collect into `results/<example>/<project>/`, then `bench/run.sh`.

Only the leaves are submodules. `examples/` and everything down to the project directory
are plain directories in this repo, so there is one `.gitmodules` and one level of init.

## Reading the result honestly

- **Cache reads dominate token totals** and are billed differently from fresh input, so
  compare `billable_tokens` (input + output + cache write) and the cache-read line separately.
- **Active time is the fairer clock.** Wall clock includes however long the terminal sat
  idle between your turns.
- **Check the fidelity column.** The roll-up states which tier rtdd actually ran at per
  project. A `static` adapter records no coverage and builds no map, so its selection deltas
  measure declared correspondence, not the coverage-derived selection rtdd is about.
  As of rtdd 0.1.3, **`python` is the only adapter that reaches `execution-derived`**;
  go, jest, vitest, cargo-nextest, maven, gradle, dotnet, phpunit and rspec all declare
  `selection: static, coverage: none`. Verify for yourself with `rtdd doctor` in the
  workspace. A non-python project therefore measures the effect of the skill's prompt on
  agent behaviour, not test selection — useful as a control, not as the headline.
- **One trial is an anecdote.** Run a pair several times before believing a delta; these
  sessions are not deterministic.
- **The two variants must not see each other.** Run them in separate containers, cloning
  each variant repo directly. The submodule wiring here is only so this repo pins which
  commit of each variant a given result set refers to.
