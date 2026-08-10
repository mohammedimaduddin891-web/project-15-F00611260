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
  audit.log \
  output/rep3-gate-blocked.txt \
  output/rep3-gate-readonly.txt \
  output/rep3-gate-approved.txt

set +e

{
  echo \
    '{"tool_input":{"command":"kubectl delete pvc data-var"}}' |
    AUDIT_LOG=audit.log \
      ./code/approval_gate.sh

  echo "exit=$?"

} 2>&1 |
  tee output/rep3-gate-blocked.txt

{
  echo \
    '{"tool_input":{"command":"du -x -d1 /var"}}' |
    AUDIT_LOG=audit.log \
      ./code/approval_gate.sh

  echo "exit=$?"

} 2>&1 |
  tee output/rep3-gate-readonly.txt

{
  echo \
    '{"tool_input":{"command":"kubectl delete pvc data-var"}}' |
    AUDIT_LOG=audit.log \
    HUMAN_APPROVAL_TOKEN=I-APPROVE \
      ./code/approval_gate.sh

  echo "exit=$?"

} 2>&1 |
  tee output/rep3-gate-approved.txt

set -e

cat audit.log
