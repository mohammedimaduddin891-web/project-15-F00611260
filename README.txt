Project 15 — AIOps and Autonomous Operations: How Much May We Entrust?

Student: Mohammed Imad Uddin
Student ID: F00611260
Course: CSC 6400 — System Administration and Maintenance (DCA)

PURPOSE
All eleven Project 15 reps are in this directory and the read-only MCP server is in this directory.
The ability to run sandboxed (and ungated) prompt-injection tests and have them approved -- a human approval gate.
Self-healing loop evidence, audit.log, governance.txt and AI activity log.

SAFETY
All destructive actions are emulated. The Rep 8 “exfil” demonstration
The use of a fake token and localhost only. No secret to production and no real secret,
The external destination is modified and/or contacted, or real cloud volume.d.

SETUP
python3 -m venv "$HOME/project15-venv"
source "$HOME/project15-venv/bin/activate"
pip install -r requirements.txt

MAIN RUNS
printf 'YES\n' | python code/mcp_consent_client.py --tool --path / | tee output/rep1-mcp-consent.txt
python code/mcp_consent_client.py --resource | tee output/rep2-resource-read.txt
bash code/run_rep3_gate_tests.sh
bash code/run_rep8_trifecta.sh
bash code/run_rep9_hostile_log.sh
bash code/run_rep10_11_loops.sh

VALIDATION
python3 -m py_compile code/*.py
for file in code/*.sh; do bash -n "$file"; done

VERIFIED RESULTS
- Rep 1: This meant that before get_disk_usage, MCP Tool consent appeared. VM disk usage was 60.8%.
- Rep 2: Incident-log Resource was readable and there was no write Tool on the MCP server.
- Rep 3: Destructive command exit is set to 2, read-only command exit is set to 0 and approved command exit is set to 0.
- Rep 8: tafter the Rule-of-Two bugfix, the second listener got 0 bytes, the fictional token reached the localhost.
- Rep 9: hostile telemetry was used as data, no command from log was executed.
- Rep 10:  Exit=2 was the first remediation attempt, it was successful in the approved simulation, with 38% available space and >25% needed.
- Rep 11: The ungated simulation was able to pass the signal, but resulted in a budget violation of $1,840/month and governance_outcome=FAIL.

SUBMISSION ARTIFACTS
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

AI HONESTY
AI assistance was used for scaffolding, debugging, and draft explanations.
I reviewed the commands and actual outputs myself. The autonomy placements,
Rule-of-Two judgment, governance policy, post-incident account, approval
decisions, and final submission remain my responsibility.
