# Benchmark results

| Metric                   | tdd            | rtdd           | Delta |
|--------------------------|----------------|----------------|-------|
| Wall clock (s)           | 939.9          | 847.5          | -10% |
| Active time (s)          | 877.6          | 785.4          | -11% |
| Time running tests (s)   | 100.2          | 50.6           | -50% |
| Test share of active     | 11.4%          | 6.4%           |  |
| Selector overhead (s)    | 0              | 0.6            |  |
| Test executions          | 36             | 18             | -50% |
| Selector queries         | 0              | 4              |  |
| Mean run (s)             | 2.78           | 2.81           | +1% |
| Slowest run (s)          | 4.35           | 5.48           | +26% |
| Red->green cycles        | 11             | 6              |  |
| Failed runs              | 13             | 6              |  |
| Assistant turns          | 86             | 79             | -8% |
| Billable tokens          | 235,186        | 325,779        | +39% |
|   output                 | 81,201         | 114,074        |  |
|   cache write            | 153,813        | 211,547        |  |
|   cache read             | 7,192,474      | 6,739,730      |  |
|   thinking               | 29,077         | 45,305         |  |
| Tests in suite           | 21             | 30             |  |
| Test files / LOC         | 3 / 531        | 5 / 552        |  |
| Main files / LOC         | 7 / 409        | 10 / 607       |  |
| Commits                  | 1              | 3              |  |

_Delta is the second variant relative to the first; negative is less._

> **`rtdd` ran rtdd at `static` fidelity** (maven adapter, 0 map entries). A static adapter records no coverage and builds no map, so tests were chosen from declared correspondence, not from a recorded run — rtdd's weakest tier. Read the selection deltas as static selection, not as the coverage-derived selection rtdd is built around.

## Test executions

### tdd

- `~/.local/bin/mvn -q -o test 2>&1 | tail -20 || ~/.local/bin/mvn test 2>&1 | grep -E "ERR` — 1.95s pass
- `~/.local/bin/mvn -q -o test 2>&1 | tail -15; echo "EXIT:$?"` — 2.76s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "expected|Tests run|ERROR.*Test" | head -5; e` — 2.47s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | tail -8; echo "EXIT:$?"` — 2.68s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected|ERROR\] " | head -6` — 2.46s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|ERROR\] " | head -6; echo "EXIT:$` — 2.68s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|ERROR\] |symbol" | head -8` — 1.83s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|ERROR\] " | head -6; echo "EXIT:$` — 2.62s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|ERROR\] |expected" | head -8` — 2.64s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|ERROR\] |expected" | head -8; ech` — 2.87s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|ERROR\] |symbol:" | head -8` — 2.02s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|ERROR\] |expected" | head -8; ech` — 2.76s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|symbol:" | head -5` — 1.93s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected|ERROR\] " | head -6; ech` — 2.77s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected" | head -4` — 2.66s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected|ERROR\] " | head -6; ech` — 2.87s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected" | head -3` — 3.34s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected|ERROR\] " | head -5; ech` — 3.34s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected" | head -3` — 2.61s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected:|but was:" | head -4; ec` — 2.91s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected:" | head -3` — 3.17s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected:|ERROR\] " | head -4; ec` — 2.97s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected:" | head -3` — 2.79s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|expected:|ERROR\] " | head -4; ec` — 3.24s FAIL
- `cd "$PWD" && ~/.local/bin/mvn -q -o test 2>&1 | grep -A3 "but was" | head -8` — 2.16s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|but was" | head -3; echo "EXIT:$?` — 3.27s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|ERROR\] " | head -5` — 2.7s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|but was|ERROR\] " | head -6; echo` — 3.05s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|but was|ERROR\] " | head -5; echo` — 2.88s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|but was" | head -5` — 2.71s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|but was" | head -5; echo "EXIT:$?` — 3.05s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|but was" | head -5; echo "EXIT:$?` — 2.88s pass
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|but was" | head -3` — 2.71s FAIL
- `~/.local/bin/mvn -q -o test 2>&1 | grep -E "Tests run:|but was" | head -3; echo "EXIT:$?` — 3.0s pass
- `cd "$PWD" && ~/.local/bin/mvn -o -q clean test 2>&1 | tail -5; echo "BUILD_EXIT=$?"; ~/.` — 3.06s pass
- `cd "$PWD" && ~/.local/bin/mvn -q clean verify 2>&1 | grep -E "ERROR|Tests run" | head -5` — 4.35s pass

### rtdd

- `mvn -q -o test 2>&1 | tail -20 || mvn -q test 2>&1 | tail -25` — 1.14s pass
- `cd '/media/nathanielsong/Sata Programming/VSCode/Character-Generation-API/rtdd-bench/led` — 5.48s pass
- `cd '/media/nathanielsong/Sata Programming/VSCode/Character-Generation-API/rtdd-bench/led` — 4.96s pass
- `cd '/media/nathanielsong/Sata Programming/VSCode/Character-Generation-API/rtdd-bench/led` — 2.7s FAIL
- `rtdd run 2>&1 | tail -12` — 2.82s pass
- `rtdd which 2>&1 | tail -6; rtdd run 2>&1 | tail -12` — 2.0s FAIL
- `rtdd run 2>&1 | tail -12` — 2.92s pass
- `rtdd run 2>&1 | tail -8` — 2.13s FAIL
- `rtdd run 2>&1 | tail -10` — 2.99s pass
- `rtdd run 2>&1 | tail -6` — 2.67s FAIL
- `rtdd run 2>&1 | tail -8` — 3.64s pass
- `cd '/media/nathanielsong/Sata Programming/VSCode/Character-Generation-API/rtdd-bench/led` — 2.52s FAIL
- `rtdd run 2>&1 | tail -12` — 3.53s pass
- `cd '/media/nathanielsong/Sata Programming/VSCode/Character-Generation-API/rtdd-bench/led` — 0.09s pass
- `cd '/media/nathanielsong/Sata Programming/VSCode/Character-Generation-API/rtdd-bench/led` — 2.68s pass
- `tail -20 src/test/java/ledger/MainTest.java; rtdd run 2>&1 | tail -8` — 2.87s FAIL
- `rtdd run 2>&1 | tail -8` — 3.11s pass
- `cd '/media/nathanielsong/Sata Programming/VSCode/Character-Generation-API/rtdd-bench/led` — 2.33s pass

