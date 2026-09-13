# Benchmark results

| Metric                   | tdd            | rtdd           | Delta |
|--------------------------|----------------|----------------|-------|
| Wall clock (s)           | 774.3          | 785.5          | +1% |
| Active time (s)          | 684.8          | 695.1          | +2% |
| Time running tests (s)   | 26.4           | 32.7           | +24% |
| Test share of active     | 3.9%           | 4.7%           |  |
| Selector overhead (s)    | 0              | 0.5            |  |
| Test executions          | 48             | 25             | -48% |
| Selector queries         | 0              | 2              |  |
| Mean run (s)             | 0.55           | 1.31           | +138% |
| Slowest run (s)          | 0.93           | 5.0            | +438% |
| Red->green cycles        | 20             | 6              |  |
| Failed runs              | 21             | 7              |  |
| Assistant turns          | 95             | 66             | -31% |
| Billable tokens          | 187,409        | 210,542        | +12% |
|   output                 | 59,277         | 68,243         |  |
|   cache write            | 127,942        | 142,167        |  |
|   cache read             | 7,554,272      | 5,315,503      |  |
|   thinking               | 17,816         | 27,600         |  |
| Tests in suite           | 25             | 36             |  |
| Test files / LOC         | 7 / 482        | 6 / 444        |  |
| Main files / LOC         | 4 / 245        | 5 / 378        |  |
| Commits                  | 3              | 4              |  |

_Delta is the second variant relative to the first; negative is less._

> `rtdd` ran rtdd at `execution-derived` fidelity (python adapter, 36 map entries).

## Test executions

### tdd

- `.venv/bin/python -m pytest -q 2>&1 | tail -5` — 0.46s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.5s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -5` — 0.51s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -5` — 0.55s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.5s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.66s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.48s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.47s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.47s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.44s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.53s FAIL
- `sed -n '1,60p' ledger/cli.py && .venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.49s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.62s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.5s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.62s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.53s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.51s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.46s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.47s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.47s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.52s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.5s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.51s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.46s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -6` — 0.54s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.53s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.56s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.5s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.5s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.66s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.5s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.5s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.6s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.56s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.57s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.51s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.52s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -3` — 0.53s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.65s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.58s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.47s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.54s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.61s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.93s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.71s pass
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.63s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -6` — 0.85s FAIL
- `.venv/bin/python -m pytest -q 2>&1 | tail -4` — 0.59s pass

### rtdd

- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | tail -20` — 0.59s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | tail -12` — 0.77s FAIL
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/python/rtdd"` — 0.48s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/python/rtdd"` — 1.1s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/python/rtdd"` — 0.16s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/python/rtdd"` — 0.43s pass
- `chmod +x $SP/shim/$n; done; rm -f $SP/argv.log; PATH="$SP/shim:$PWD/.venv/bin:$PATH" rtd` — 0.46s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/python/rtdd"` — 3.53s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|tail -8` — 1.06s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/python/rtdd"` — 0.84s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|FAIL'|head` — 0.88s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)'` — 1.0s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/python/rtdd"` — 0.9s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|FAILED|assert'|hea` — 1.12s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|ModuleNotFound'|he` — 1.02s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|FAILED'|head` — 0.97s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|invalid choice'|he` — 5.0s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|FAILED'|head` — 0.98s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|invalid choice'|he` — 4.21s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|FAILED'|head` — 1.18s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|FAILED'|head` — 1.3s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1|grep -E '^(tier|[0-9]+ ran)|FAILED'|head` — 1.4s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd seed 2>&1|tail -2 && PATH="$PWD/.venv/bin:$PATH" rtdd v` — 1.1s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/python/rtdd"` — 1.45s pass
- `printf '.coverage*\n' >> .gitignore && git status --porcelain -uall && echo "=== suite =` — 0.78s pass

