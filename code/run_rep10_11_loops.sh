#!/usr/bin/env bash

set -u

PROJECT_ROOT="$(
  cd "$(
    dirname "${BASH_SOURCE[0]}"
  )/.."
  pwd
)"

cd "$PROJECT_ROOT"

rm -f \
  output/rep10-gated-blocked.txt \
  output/rep10-gated-approved.txt \
  output/rep11-ungated-run.txt

set +e

python3 code/self_healing_loop.py \
  --mode gated \
  --audit-log audit.log \
  --run-log \
  output/rep10-gated-blocked.txt

blocked_exit=$?

echo \
  "blocked_exit=$blocked_exit" |
  tee -a \
    output/rep10-gated-blocked.txt

set -e

python3 code/self_healing_loop.py \
  --mode gated \
  --approval-token I-APPROVE \
  --audit-log audit.log \
  --run-log \
  output/rep10-gated-approved.txt

python3 code/self_healing_loop.py \
  --mode ungated \
  --run-log \
  output/rep11-ungated-run.txt

printf \
  '\n== audit.log ==\n'

cat audit.log
