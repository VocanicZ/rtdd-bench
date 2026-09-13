# Benchmark results

| Metric                   | tdd            | rtdd           | Delta |
|--------------------------|----------------|----------------|-------|
| Wall clock (s)           | 762.7          | 765.2          | +0% |
| Active time (s)          | 670.8          | 673.8          | +0% |
| Time running tests (s)   | 20.4           | 7.4            | -64% |
| Test share of active     | 3.0%           | 1.1%           |  |
| Selector overhead (s)    | 0              | 0.6            |  |
| Test executions          | 34             | 17             | -50% |
| Selector queries         | 0              | 3              |  |
| Mean run (s)             | 0.6            | 0.43           | -28% |
| Slowest run (s)          | 6.95           | 1.42           | -80% |
| Red->green cycles        | 13             | 6              |  |
| Failed runs              | 15             | 6              |  |
| Assistant turns          | 85             | 57             | -33% |
| Billable tokens          | 222,527        | 203,681        | -8% |
|   output                 | 75,844         | 61,097         |  |
|   cache write            | 146,513        | 142,470        |  |
|   cache read             | 6,864,073      | 4,575,015      |  |
|   thinking               | 26,839         | 19,592         |  |
| Tests in suite           | 18             | 24             |  |
| Test files / LOC         | 1 / 395        | 6 / 511        |  |
| Main files / LOC         | 3 / 537        | 4 / 800        |  |
| Commits                  | 2              | 2              |  |

_Delta is the second variant relative to the first; negative is less._

> **`rtdd` ran rtdd at `static` fidelity** (go adapter, 0 map entries). A static adapter records no coverage and builds no map, so tests were chosen from declared correspondence, not from a recorded run — rtdd's weakest tier. Read the selection deltas as static selection, not as the coverage-derived selection rtdd is built around.

## Test executions

### tdd

- `go test ./... 2>&1 | head -20` — 0.22s FAIL
- `gofmt -l . ; go test ./... 2>&1 | tail -5` — 0.39s pass
- `go test ./... 2>&1 | tail -10` — 0.36s FAIL
- `gofmt -w . && go test ./... 2>&1 | tail -10` — 0.4s pass
- `go test ./... 2>&1 | tail -6` — 0.38s FAIL
- `gofmt -w . && go test ./... 2>&1 | tail -6` — 0.41s pass
- `go test ./... 2>&1 | tail -6` — 0.54s pass
- `go test ./... 2>&1 | tail -6` — 0.36s FAIL
- `gofmt -w . && go test ./... 2>&1 | tail -12` — 0.42s pass
- `go test ./... 2>&1 | tail -8` — 0.36s pass
- `go test ./... 2>&1 | tail -8` — 0.36s FAIL
- `gofmt -w . && go test ./... 2>&1 | tail -8` — 0.38s pass
- `go test ./... 2>&1 | tail -8` — 0.49s FAIL
- `gofmt -w . && go test ./... 2>&1 | tail -8` — 0.44s pass
- `go test ./... 2>&1 | tail -8` — 0.34s FAIL
- `gofmt -w . && go test ./... 2>&1 | tail -8` — 0.43s pass
- `go test ./... 2>&1 | tail -8` — 0.55s FAIL
- `go test ./... 2>&1 | tail -6` — 0.38s FAIL
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/go/tdd" && g` — 0.4s FAIL
- `go test ./... 2>&1 | tail -6` — 0.39s pass
- `go test ./... 2>&1 | head -12` — 0.46s FAIL
- `gofmt -w . && go test ./... 2>&1 | head -12` — 0.37s pass
- `go test ./... 2>&1 | head -12` — 0.43s FAIL
- `gofmt -w . && go test ./... 2>&1 | head -12` — 0.41s pass
- `go test -timeout 30s ./... 2>&1 | head -8` — 6.95s pass
- `gofmt -w . && go test -timeout 30s ./... 2>&1 | head -8` — 0.4s pass
- `go test -timeout 30s ./... 2>&1 | head -20` — 0.36s FAIL
- `gofmt -w . && go test -timeout 30s ./... 2>&1 | head -20` — 0.41s pass
- `go test -timeout 30s ./... 2>&1 | head -20` — 0.41s pass
- `go test -timeout 30s ./... 2>&1 | head -20` — 0.52s FAIL
- `go test -timeout 30s ./... 2>&1 | head -20` — 0.4s pass
- `go test -timeout 30s ./... 2>&1 | head -8` — 0.42s FAIL
- `gofmt -w . && go test -timeout 30s ./... 2>&1 | head -8` — 0.41s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/go/tdd" && g` — 0.41s pass

### rtdd

- `go test ./... 2>&1 | head -20` — 0.24s FAIL
- `go test ./... 2>&1 | tail -20` — 0.41s pass
- `sed -i 's/^import "testing"$/import (\n\t"strings"\n\t"testing"\n)/' journal_test.go; he` — 0.21s FAIL
- `go test ./... 2>&1 | tail -20` — 0.36s pass
- `go test ./... 2>&1 | tail -20` — 0.28s FAIL
- `gofmt -l . ; go test ./... 2>&1 | tail -20` — 0.36s pass
- `go test ./... 2>&1 | tail -10` — 0.24s FAIL
- `go test ./... 2>&1 | tail -10` — 0.4s pass
- `go test ./... 2>&1 | tail -30` — 0.38s FAIL
- `gofmt -l .; go test ./... 2>&1 | tail -30` — 0.46s pass
- `go test ./... 2>&1 | tail -20` — 0.42s FAIL
- `gofmt -w . && go test ./... 2>&1 | tail -20` — 0.51s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/go/rtdd" && ` — 0.33s pass
- `go test ./... 2>&1 | tail -25` — 0.47s pass
- `gofmt -w . && go vet ./... && go test ./... 2>&1 | tail -5` — 1.42s pass
- `gofmt -w . && go vet ./... && rtdd verify 2>&1 | tail -6` — 0.29s pass
- `cd "/media/nathanielsong/Sata Programming/VSCode/rtdd-bench/examples/ledger/go/rtdd" && ` — 0.61s pass

