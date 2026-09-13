# Benchmark results

One row per project: the same task, the same stack, `/tdd` against `/rtdd`. Percentages are rtdd relative to tdd, so negative is less. Each project links to its full table.

| Project                                                    | Test executions | Time in tests | Billable tokens | Red->green | Fidelity |
|------------------------------------------------------------|-----------------|---------------|-----------------|------------|----------|
| [ledger/java-maven](examples/ledger/java-maven/RESULTS.md) | -50%            | -50%          | +39%            | 11 -> 6    | static   |

> Rows below `execution` fidelity ran rtdd against an adapter that records no coverage and builds no map (maven is one), so their tests were chosen from declared correspondence rather than from a recorded run. Read those selection deltas as static selection.

_One trial is an anecdote; these sessions are not deterministic._
