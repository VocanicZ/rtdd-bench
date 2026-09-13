# Benchmark results

One row per project: the same task, the same stack, `/tdd` against `/rtdd`. Percentages are rtdd relative to tdd, so negative is less. Each project links to its full table.

| Project                                                      | Test executions | Time in tests | Billable tokens | Red->green | Fidelity          |
|--------------------------------------------------------------|-----------------|---------------|-----------------|------------|-------------------|
| [cron-parser/go](examples/cron-parser/go/RESULTS.md)         | -40%            | -70%          | +29%            | 12 -> 5    | static            |
| [cron-parser/python](examples/cron-parser/python/RESULTS.md) | -58%            | -59%          | -27%            | 24 -> 7    | execution-derived |
| [ledger/go](examples/ledger/go/RESULTS.md)                   | -50%            | -64%          | -8%             | 13 -> 6    | static            |
| [ledger/python](examples/ledger/python/RESULTS.md)           | -48%            | +24%          | +12%            | 20 -> 6    | execution-derived |

> Rows below `execution` fidelity ran rtdd against an adapter that records no coverage and builds no map (go is one), so their tests were chosen from declared correspondence rather than from a recorded run. Read those selection deltas as static selection.

_One trial is an anecdote; these sessions are not deterministic._
