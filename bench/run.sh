#!/usr/bin/env bash
# Collect both variants and render the comparison.
#   bench/run.sh [tdd-session-id] [rtdd-session-id]
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results

a=${1:-}; b=${2:-}
python3 bench/collect.py --workspace ledger-tdd  --label tdd  ${a:+--session "$a"} > results/tdd.json
python3 bench/collect.py --workspace ledger-rtdd --label rtdd ${b:+--session "$b"} > results/rtdd.json
python3 bench/report.py results/tdd.json results/rtdd.json | tee RESULTS.md

echo
echo "Wrote RESULTS.md, results/tdd.json, results/rtdd.json"
echo "List sessions for a workspace with:"
echo "  python3 bench/collect.py --workspace ledger-tdd --label x --list"
