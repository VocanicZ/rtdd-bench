Build a CLI called `cron` — parse cron expressions and project future run times.
Work test-first: one failing test, then the code to pass it, then the next.

  cron next <expr> --count N [--from <ISO8601>] [--tz <zone>]   the next N run times
  cron describe <expr>                                          one plain-English line
  cron match <expr> <ISO8601>                                   exit 0 if it would run

Five fields: minute hour day-of-month month day-of-week. Support `*`, lists `1,5`,
ranges `1-5`, steps `*/15` and `10-30/5`, names `JAN`-`DEC` and `SUN`-`SAT`, and the
macros `@hourly @daily @weekly @monthly @yearly`. When both day-of-month and
day-of-week are restricted, a time matches if either one matches. Times are computed
in the given zone, default UTC; a skipped or repeated local hour at a daylight-saving
boundary must not yield a duplicate or a missing occurrence.

Done when all three commands work and a malformed expression says which field was
bad, not a stack trace.
