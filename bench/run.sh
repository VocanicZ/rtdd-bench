#!/usr/bin/env bash
# Render the comparison from whatever has been collected.
#
#   bench/run.sh                          every project that has results, plus the roll-up
#   bench/run.sh ledger/java-maven        one project
#   bench/run.sh ledger/java-maven A B    ... pinning the tdd and rtdd session ids
#
# Containerised runs (the isolated setup): collect inside each container with
# bench/collect.py, drop the two JSON files in results/<example>/<project>/, then run
# this with no arguments. Same-machine runs collect from the submodules directly.
set -euo pipefail
cd "$(dirname "$0")/.."

render_one() {
  local p=$1 a=${2:-} b=${3:-}
  local res="results/$p" ws="examples/$p"
  mkdir -p "$res"
  if [ ! -f "$res/tdd.json" ] || [ ! -f "$res/rtdd.json" ]; then
    if [ -d "$ws/tdd" ] && [ -d "$ws/rtdd" ]; then
      python3 bench/collect.py --workspace "$ws/tdd"  --label tdd  ${a:+--session "$a"} > "$res/tdd.json"
      python3 bench/collect.py --workspace "$ws/rtdd" --label rtdd ${b:+--session "$b"} > "$res/rtdd.json"
    else
      cat >&2 <<MSG
No collected results for $p, and its workspaces are not checked out here.

Each session ran in its own container, so collect there and bring the JSON back:

  # inside the tdd container, in the cloned workspace
  python3 collect.py --workspace . --label tdd > tdd.json

  # inside the rtdd container
  python3 collect.py --workspace . --label rtdd > rtdd.json

Then copy both into results/$p/ here and run bench/run.sh again.
MSG
      exit 1
    fi
  fi
  python3 bench/report.py "$res/tdd.json" "$res/rtdd.json" > "$ws/RESULTS.md"
  echo "Wrote $ws/RESULTS.md, $res/{tdd,rtdd}.json"
}

if [ $# -gt 0 ]; then
  render_one "$@"
else
  found=0
  for d in results/*/*/; do
    [ -f "$d/tdd.json" ] && [ -f "$d/rtdd.json" ] || continue
    p=${d#results/}; render_one "${p%/}"; found=1
  done
  if [ "$found" = 0 ]; then
    echo "No collected results under results/. Run bench/run.sh <example>/<project>." >&2
    exit 1
  fi
fi

python3 bench/summary.py > RESULTS.md
echo "Wrote RESULTS.md"
