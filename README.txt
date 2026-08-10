Project 15 — AIOps and Autonomous Operations: How Much May We Entrust?

Student:
Mohammed Imad Uddin

Student ID:
F00611260

Course:
CSC 6400 — System Administration and Maintenance (DCA)

Tier:
Normal

PURPOSE

This repository contains all eleven Project 15 reps and the required
governance policy. It demonstrates a read-only MCP server, explicit Tool
consent, a human approval gate, action-specific autonomy tiers, a sandboxed
prompt-injection demonstration, gated and ungated self-healing loops, an audit
log, and human accountability.

SAFETY

All cleanup, deletion, resize, service-stop, and exfiltration examples are
simulations or use fictional data sent only to localhost. No production
service, real secret, real volume, or external host is used.

INSTALLATION

sudo apt update

sudo apt install -y \
  python3-venv \
  python3-pip \
  netcat-openbsd \
  jq \
  git

python3 -m venv "$HOME/project15-venv"

source "$HOME/project15-venv/bin/activate"

python -m pip install --upgrade pip

pip install -r requirements.txt

MAIN RUNS

Rep 1 — MCP Tool consent:

printf 'YES\n' | \
  python code/mcp_consent_client.py \
    --tool \
    --path / | \
  tee output/rep1-mcp-consent.txt

Rep 2 — MCP Resource:

python code/mcp_consent_client.py \
  --resource | \
  tee output/rep2-resource-read.txt

Rep 3 — Approval gate:

bash code/run_rep3_gate_tests.sh

Rep 8 — Lethal-trifecta sandbox:

bash code/run_rep8_trifecta.sh

Rep 9 — Hostile telemetry:

bash code/run_rep9_hostile_log.sh

Reps 10 and 11 — Gated and ungated loops:

bash code/run_rep10_11_loops.sh

VALIDATION

python3 -m py_compile code/*.py

for file in code/*.sh
do
  bash -n "$file"
done

python3 - <<'PY'
import yaml
from pathlib import Path

yaml.safe_load(
    Path(
        "code/runbook_disk_pressure.yaml"
    ).read_text(
        encoding="utf-8"
    )
)

print("YAML PASS")
PY

REQUIRED SUBMISSION FILES

code/
reps/
sandbox/
output/
audit.log
governance.txt
agent-log.txt
README.txt
REPORT.docx
requirements.txt

HUMAN ACCOUNTABILITY

AI assistance was used for initial scaffolding and draft explanations. The
autonomy placements, Rule-of-Two judgment, post-incident account, governance
policy, approval decisions, and final submission remain the student's
responsibility.
