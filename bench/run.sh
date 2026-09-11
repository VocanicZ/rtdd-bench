#!/usr/bin/env bash
# Render the comparison from whatever has been collected.
#
# Containerised runs (the isolated setup): collect inside each container with
# bench/collect.py, copy the two JSON files into results/, then run this with
# no arguments.
#
# Same-machine runs: pass session ids to collect from the submodules directly.
#   bench/run.sh [tdd-session-id] [rtdd-session-id]
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results

if [ ! -f results/tdd.json ] || [ ! -f results/rtdd.json ]; then
  if [ -d ledger-tdd ] && [ -d ledger-rtdd ]; then
    a=${1:-}; b=${2:-}
    python3 bench/collect.py --workspace ledger-tdd  --label tdd  ${a:+--session "$a"} > results/tdd.json
    python3 bench/collect.py --workspace ledger-rtdd --label rtdd ${b:+--session "$b"} > results/rtdd.json
  else
    cat >&2 <<'MSG'
No collected results and no submodule workspaces here.

Each session ran in its own container, so collect there and bring the JSON back:

  # inside the ledger-tdd container, in the cloned workspace
  python3 collect.py --workspace . --label tdd > tdd.json

  # inside the ledger-rtdd container
  python3 collect.py --workspace . --label rtdd > rtdd.json

Then copy both into results/ here and run bench/run.sh again.
MSG
    exit 1
  fi
fi

python3 bench/report.py results/tdd.json results/rtdd.json | tee RESULTS.md
echo
echo "Wrote RESULTS.md, results/tdd.json, results/rtdd.json"
