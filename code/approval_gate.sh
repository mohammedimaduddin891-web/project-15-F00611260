#!/usr/bin/env bash
# approval_gate.sh — human-in-the-loop gate for proposed Bash actions.
#
# Reads one JSON object from stdin.
#
# Supported fields:
# {
#   "tool_input": {
#     "command": "command proposed by the agent"
#   },
#   "autonomy": "approve"
# }
#
# Exit 0 = allow
# Exit 2 = block and require named human approval

set -euo pipefail

AUDIT_LOG="${AUDIT_LOG:-audit.log}"
APPROVAL_TOKEN_VALUE="I-APPROVE"

# Commands that must not execute automatically.
DESTRUCTIVE='(\brm\b.*-[rf]|systemctl (stop|disable)|kubectl delete|reboot|shutdown|drop[[:space:]]+table|dd[[:space:]]+if=|journalctl[[:space:]]+--vacuum|resize-pvc)'

payload="$(cat)"

parsed="$(
  printf '%s' "$payload" |
    python3 -c '
import json
import sys

obj = json.load(sys.stdin)

command = str(
    obj.get(
        "tool_input",
        {},
    ).get(
        "command",
        "",
    )
)

autonomy = str(
    obj.get(
        "autonomy",
        "",
    )
).lower()

print(command)
print(autonomy)
'
)"

cmd="$(printf '%s\n' "$parsed" | sed -n '1p')"
autonomy="$(printf '%s\n' "$parsed" | sed -n '2p')"
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

needs_human=false

if [[ "$autonomy" == "approve" ]]; then
  needs_human=true
fi

if printf '%s' "$cmd" | grep -Eiq "$DESTRUCTIVE"; then
  needs_human=true
fi

if [[ "$needs_human" == true ]]; then

  if [[ "${HUMAN_APPROVAL_TOKEN:-}" == "$APPROVAL_TOKEN_VALUE" ]]; then
    echo "$ts ALLOW(approved) :: $cmd" >> "$AUDIT_LOG"
    exit 0
  fi

  echo "$ts BLOCK(needs-human) :: $cmd" >> "$AUDIT_LOG"

  echo \
    "BLOCKED: '$cmd' requires explicit human approval." \
    >&2

  exit 2
fi

echo "$ts ALLOW(policy-safe) :: $cmd" >> "$AUDIT_LOG"

exit 0
