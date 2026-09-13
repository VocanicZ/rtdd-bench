# Benchmark results

| Metric                   | tdd            | rtdd           | Delta |
|--------------------------|----------------|----------------|-------|
| Wall clock (s)           | 821.6          | 884.8          | +8% |
| Active time (s)          | 724.3          | 782.2          | +8% |
| Time running tests (s)   | 24.4           | 7.2            | -70% |
| Test share of active     | 3.4%           | 0.9%           |  |
| Selector overhead (s)    | 0              | 0.2            |  |
| Test executions          | 30             | 18             | -40% |
| Selector queries         | 0              | 1              |  |
| Mean run (s)             | 0.81           | 0.4            | -51% |
| Slowest run (s)          | 8.19           | 0.76           | -91% |
| Red->green cycles        | 12             | 5              |  |
| Failed runs              | 13             | 7              |  |
| Assistant turns          | 71             | 65             | -8% |
| Billable tokens          | 232,414        | 299,594        | +29% |
|   output                 | 83,929         | 114,068        |  |
|   cache write            | 148,343        | 185,396        |  |
|   cache read             | 5,506,474      | 5,671,086      |  |
|   thinking               | 30,277         | 56,506         |  |
| Tests in suite           | 25             | 23             |  |
| Test files / LOC         | 5 / 507        | 4 / 518        |  |
| Main files / LOC         | 5 / 572        | 5 / 569        |  |
| Commits                  | 3              | 2              |  |

_Delta is the second variant relative to the first; negative is less._

> **`rtdd` ran rtdd at `static` fidelity** (go adapter, 0 map entries). A static adapter records no coverage and builds no map, so tests were chosen from declared correspondence, not from a recorded run — rtdd's weakest tier. Read the selection deltas as static selection, not as the coverage-derived selection rtdd is built around.

## Test executions

### tdd

- `go test ./... 2>&1 | head -20` — 5.48s FAIL
- `go test ./... 2>&1 | head -20` — 0.45s pass
- `go test ./... 2>&1 | head -20` — 0.35s FAIL
- `gofmt -w cron.go && go test ./... 2>&1 | head -20` — 0.34s pass
- `go test ./... 2>&1 | head -20` — 0.31s FAIL
- `gofmt -w cron.go && go test ./... 2>&1 | head -20` — 0.36s pass
- `go test ./... 2>&1 | head -20` — 0.32s FAIL
- `gofmt -w cron.go && go test ./... 2>&1 | head -20` — 0.35s pass
- `go test ./... 2>&1 | head -20` — 0.47s FAIL
- `gofmt -w cron.go && go test ./... 2>&1 | head -20` — 0.42s pass
- `go test ./... 2>&1 | head -20` — 0.36s FAIL
- `gofmt -w cron.go && go test ./... 2>&1 | head -20` — 0.36s pass
- `go test ./... 2>&1 | head -20` — 0.35s FAIL
- `gofmt -w cron.go && go test ./... 2>&1 | head -20` — 0.56s pass
- `go test ./... 2>&1 | head -20` — 0.34s pass
- `go test ./... 2>&1 | head -20` — 0.2s FAIL
- `gofmt -w . && go test ./... 2>&1 | head -20` — 0.39s pass
- `go test ./... 2>&1 | head -30` — 0.36s FAIL
- `gofmt -w . && go test ./... 2>&1 | head -30` — 0.46s pass
- `cp /tmp/claude-1000/-media-nathanielsong-Sata-Programming-VSCode-rtdd-bench-examples-cro` — 0.37s pass
- `go test ./... 2>&1 | head -20` — 0.49s pass
- `go test ./... 2>&1 | head -10` — 0.19s FAIL
- `gofmt -w . && go test ./... 2>&1 | head -20` — 0.37s FAIL
- `gofmt -w . && go test ./... 2>&1 | head -20` — 0.44s pass
- `go test ./... 2>&1 | head -10` — 0.22s FAIL
- `gofmt -w . && go test ./... 2>&1 | head -20` — 0.52s pass
- `gofmt -w . && go test ./... 2>&1 | head -20` — 0.52s pass
- `go test ./... 2>&1 | head -20` — 0.39s FAIL
- `gofmt -w . && go test ./... 2>&1 | head -20` — 0.46s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/go/tdd"` — 8.19s pass

### rtdd

- `go test ./... 2>&1 | head -20` — 0.22s FAIL
- `go test ./... 2>&1 | head -20` — 0.35s pass
- `go test ./... 2>&1 | head -15` — 0.35s FAIL
- `gofmt -l . ; go test ./... 2>&1 | head -20` — 0.48s pass
- `go test ./... 2>&1 | head -10` — 0.23s pass
- `gofmt -l .; go test ./... 2>&1 | head -20` — 0.39s FAIL
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/go/rtdd` — 0.46s pass
- `go test ./... 2>&1 | head -5` — 0.22s FAIL
- `gofmt -l .; go test ./... 2>&1 | head -20` — 0.76s FAIL
- `go test ./... 2>&1 | head -20` — 0.39s FAIL
- `gofmt -l .; go test ./... 2>&1 | head -20` — 0.44s pass
- `go test ./... 2>&1 | head -5` — 0.21s FAIL
- `gofmt -l .; go test ./... 2>&1 | head -20` — 0.52s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/go/rtdd` — 0.4s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/go/rtdd` — 0.75s pass
- `go test ./... 2>&1 | head -10` — 0.43s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/go/rtdd` — 0.53s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/cron-parser/go/rtdd` — 0.11s pass

