# Benchmark prompt

Paste verbatim into both sessions. The only difference between the two runs is the
skill invoked first: `/tdd` in the `ledger-tdd` workspace, `/rtdd` in `ledger-rtdd`.

Start each session with its working directory set to that submodule, and nothing else
open. Do not mention the benchmark, the other variant, or any metric to the agent —
everything is measured afterwards from the transcript.

---

```
Build a Java CLI called `ledger` — double-entry bookkeeping. Work test-first: one
failing test, then the code to pass it, then the next.

  ledger validate <file>   report every imbalance with line numbers
  ledger balance  <file>   account balances, tree-indented, --depth N
  ledger register <file>   transaction list, --account, --since, --until

Format: a date line `2026-01-04 payee`, then indented postings
`  account:sub  -42.50 USD`. One posting per transaction may omit its amount and is
inferred. Postings must sum to zero. Multiple currencies, never converted.
Comments with `;`. `include other.journal`.

Java 21, Maven, JUnit 5, no dependencies beyond the test scope. Done when all three
commands work and malformed input gives a clear error, not a stack trace.
```
