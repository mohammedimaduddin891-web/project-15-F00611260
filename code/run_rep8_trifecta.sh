#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(
  cd "$(
    dirname "${BASH_SOURCE[0]}"
  )/.."
  pwd
)"

cd "$PROJECT_ROOT"

rm -f \
  output/rep8-exfiltration-captured.txt \
  output/rep8-vulnerable-agent.txt \
  output/rep8-rule-of-two-listener.txt \
  output/rep8-rule-of-two-blocked.txt

(
  timeout 6s \
    nc -l 9999 \
    > output/rep8-exfiltration-captured.txt
) &

listener_pid=$!

sleep 1

python3 code/trifecta_agent.py \
  --mode vulnerable |
  tee output/rep8-vulnerable-agent.txt

wait "$listener_pid" || true

echo \
  "== Captured by localhost listener =="

cat \
  output/rep8-exfiltration-captured.txt

(
  timeout 3s \
    nc -l 9999 \
    > output/rep8-rule-of-two-listener.txt
) &

listener_pid=$!

sleep 1

python3 code/trifecta_agent.py \
  --mode rule-of-two |
  tee output/rep8-rule-of-two-blocked.txt

wait "$listener_pid" || true

bytes="$(
  wc -c \
    < output/rep8-rule-of-two-listener.txt
)"

echo \
  "rule_of_two_listener_bytes=$bytes" |
  tee -a \
    output/rep8-rule-of-two-blocked.txt
