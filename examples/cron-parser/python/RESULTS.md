# Benchmark results

| Metric                   | tdd            | rtdd           | Delta |
|--------------------------|----------------|----------------|-------|
| Wall clock (s)           | 1089.7         | 857.7          | -21% |
| Active time (s)          | 994.1          | 764.7          | -23% |
| Time running tests (s)   | 53.2           | 22.0           | -59% |
| Test share of active     | 5.3%           | 2.9%           |  |
| Selector overhead (s)    | 0              | 0.8            |  |
| Test executions          | 60             | 25             | -58% |
| Selector queries         | 0              | 3              |  |
| Mean run (s)             | 0.89           | 0.88           | -1% |
| Slowest run (s)          | 18.71          | 1.35           | -93% |
| Red->green cycles        | 24             | 7              |  |
| Failed runs              | 26             | 8              |  |
| Assistant turns          | 131            | 64             | -51% |
| Billable tokens          | 267,272        | 194,975        | -27% |
|   output                 | 95,311         | 56,676         |  |
|   cache write            | 171,699        | 138,171        |  |
|   cache read             | 11,128,649     | 5,229,148      |  |
|   thinking               | 39,089         | 19,998         |  |
| Tests in suite           | 52             | 34             |  |
| Test files / LOC         | 8 / 384        | 6 / 329        |  |
| Main files / LOC         | 1 / 345        | 6 / 456        |  |
| Commits                  | 2              | 4              |  |

_Delta is the second variant relative to the first; negative is less._

> `rtdd` ran rtdd at `execution-derived` fidelity (python adapter, 53 map entries).

## Test executions

### tdd

- `.venv/bin/pytest -q 2>&1 | tail -5` — 0.65s pass
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.57s pass
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.52s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.42s pass
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.5s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.39s pass
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.47s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.45s pass
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.81s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.44s pass
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.47s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.51s pass
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.59s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.45s pass
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.45s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.51s pass
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.54s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.61s pass
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.56s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -5` — 0.6s pass
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.43s pass
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.53s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.42s pass
- `.venv/bin/pytest -q tests/test_errors.py 2>&1 | tail -4` — 0.48s pass
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.44s pass
- `.venv/bin/pytest -q tests/test_errors.py 2>&1 | tail -5` — 0.54s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.45s pass
- `.venv/bin/pytest -q tests/test_next_runs.py 2>&1 | tail -4` — 0.51s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.44s pass
- `.venv/bin/pytest -q tests/test_dst.py 2>&1 | tail -4` — 0.48s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.55s pass
- `.venv/bin/pytest -q tests/test_dst.py 2>&1 | tail -4` — 0.4s pass
- `.venv/bin/pytest -q tests/test_describe.py 2>&1 | tail -3` — 0.72s pass
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.49s pass
- `.venv/bin/pytest -q tests/test_describe.py 2>&1 | tail -4` — 0.47s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.51s pass
- `.venv/bin/pytest -q tests/test_describe.py 2>&1 | tail -5` — 0.46s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.55s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.43s pass
- `.venv/bin/pytest -q tests/test_cli.py 2>&1 | tail -4` — 0.47s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.5s pass
- `.venv/bin/pytest -q tests/test_cli.py 2>&1 | tail -4` — 0.49s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.51s pass
- `.venv/bin/pytest -q tests/test_cli.py 2>&1 | tail -4` — 0.59s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.61s pass
- `.venv/bin/pytest -q tests/test_cli.py 2>&1 | tail -5` — 0.78s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.83s pass
- `.venv/bin/pytest -q tests/test_cli.py 2>&1 | tail -5` — 0.88s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -4` — 0.94s pass
- `.venv/bin/pytest -q tests/test_cli.py 2>&1 | tail -4` — 0.96s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.94s pass
- `.venv/bin/pytest -q tests/test_errors.py 2>&1 | tail -4` — 0.44s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.94s pass
- `.venv/bin/pytest -q tests/test_cli.py 2>&1 | tail -4` — 18.71s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.97s pass
- `.venv/bin/pytest -q tests/test_describe.py 2>&1 | tail -4` — 0.4s FAIL
- `.venv/bin/pytest -q 2>&1 | tail -4` — 1.02s FAIL
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 0.44s pass
- `.venv/bin/pytest -q 2>&1 | tail -3` — 0.95s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 0.98s pass

### rtdd

- `PATH="$PWD/.venv/bin:$PATH" pytest -q 2>&1 | tail -8` — 0.62s pass
- `PATH="$PWD/.venv/bin:$PATH" pytest -q 2>&1 | tail -3` — 0.56s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 0.5s FAIL
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 0.16s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 0.36s pass
- `uv pip install --python .venv/bin/python pytest-cov pytest-reportlog 2>&1 | tail -3 && P` — 1.21s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 1.03s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 0.76s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|passed|selected|UNCOV` — 0.88s pass
- `sed -i 's/"minute""minute"/"minute"/' tests/test_errors.py && PATH="$PWD/.venv/bin:$PATH` — 0.86s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|error|selected" | hea` — 1.02s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|selected|Error" | hea` — 0.91s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|assert|selected" | he` — 0.97s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|error|selected" | hea` — 1.14s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|assert|Error|failed|selected` — 1.25s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|selected" | head` — 1.08s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|error|selected" | hea` — 0.95s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|assert|failed|selected" | he` — 1.35s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|selected" | head` — 1.23s FAIL
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|selected|assert" | he` — 1.05s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 0.24s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 0.69s FAIL
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 1.06s pass
- `PATH="$PWD/.venv/bin:$PATH" rtdd run 2>&1 | grep -E "FAILED|failed|selected" | head -3` — 1.17s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/python/` — 0.98s pass

