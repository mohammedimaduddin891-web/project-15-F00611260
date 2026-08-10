#!/usr/bin/env python3
"""Sandboxed Project 15 self-healing loop simulator.

No operating-system state is changed.

Commands are printed and passed through approval_gate.sh, but remediation
effects are fictional measurements based on the supplied course incident.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess

from datetime import (
    UTC,
    datetime,
)

from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

RUNBOOK_PATH = (
    PROJECT_ROOT
    / "code"
    / "runbook_disk_pressure.yaml"
)

GATE_PATH = (
    PROJECT_ROOT
    / "code"
    / "approval_gate.sh"
)


def timestamp() -> str:
    return datetime.now(
        UTC
    ).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def load_runbook() -> dict[str, Any]:

    return yaml.safe_load(
        RUNBOOK_PATH.read_text(
            encoding="utf-8"
        )
    )


def append_event(
    path: Path,
    message: str,
) -> None:

    line = (
        f"{timestamp()} "
        f"{message}"
    )

    print(
        line
    )

    with path.open(
        "a",
        encoding="utf-8",
    ) as handle:

        handle.write(
            line + "\n"
        )


def invoke_gate(
    command: str,
    autonomy: str,
    audit_log: Path,
    approval_token: str | None,
) -> int:

    payload = json.dumps(
        {
            "tool_input": {
                "command": command,
            },
            "autonomy": autonomy,
        }
    )

    env = os.environ.copy()

    env["AUDIT_LOG"] = str(
        audit_log
    )

    if approval_token:
        env[
            "HUMAN_APPROVAL_TOKEN"
        ] = approval_token

    else:
        env.pop(
            "HUMAN_APPROVAL_TOKEN",
            None,
        )

    result = subprocess.run(
        [
            str(
                GATE_PATH
            )
        ],
        input=payload,
        text=True,
        env=env,
        check=False,
        capture_output=True,
    )

    if result.stderr.strip():
        print(
            result.stderr.strip()
        )

    return result.returncode


def run_gated(
    args: argparse.Namespace,
    runbook: dict[str, Any],
) -> int:

    run_log = Path(
        args.run_log
    )

    audit_log = Path(
        args.audit_log
    )

    append_event(
        run_log,
        (
            "EVENT DiskPressure "
            "mount=/var "
            "avail_pct=9 "
            "sustained=5m"
        ),
    )

    diagnostic = (
        runbook[
            "diagnose"
        ][0]
    )

    append_event(
        run_log,
        (
            "DIAGNOSE "
            f"autonomy="
            f"{diagnostic['autonomy']} "
            f"cmd="
            f"{diagnostic['cmd']}"
        ),
    )

    append_event(
        run_log,
        (
            "FINDING "
            "/var/log/journal=41G "
            "/var/lib/docker=18G "
            "/var/cache/apt=6G"
        ),
    )

    append_event(
        run_log,
        (
            "HYPOTHESIS "
            "journald rotation disabled; "
            "log volume dominates /var"
        ),
    )

    remediation = (
        runbook[
            "remediate"
        ][0]
    )

    append_event(
        run_log,
        (
            "PROPOSE "
            f"id={remediation['id']} "
            f"autonomy="
            f"{remediation['autonomy']} "
            f"reversible="
            f"{str(
                remediation['reversible']
            ).lower()} "
            f"cmd="
            f"{remediation['cmd']}"
        ),
    )

    append_event(
        run_log,
        (
            "GATE requesting "
            "human approval"
        ),
    )

    gate_exit = invoke_gate(
        remediation[
            "cmd"
        ],
        remediation[
            "autonomy"
        ],
        audit_log,
        args.approval_token,
    )

    if gate_exit != 0:

        append_event(
            run_log,
            (
                "GATE BLOCKED "
                f"exit={gate_exit}"
            ),
        )

        return gate_exit

    append_event(
        run_log,
        (
            "APPROVE token accepted "
            "for one simulated action"
        ),
    )

    append_event(
        run_log,
        (
            "ACT SIMULATED "
            "journalctl "
            "--vacuum-size=500M "
            "result=freed-40.6G"
        ),
    )

    observed_pct = 38

    expected_pct = int(
        runbook[
            "verify"
        ][
            "expect_pct_above"
        ]
    )

    verdict = (
        "PASS"
        if observed_pct
        > expected_pct
        else "FAIL"
    )

    append_event(
        run_log,
        (
            "VERIFY "
            "signal="
            "node_filesystem_avail_bytes "
            f"avail_pct={observed_pct} "
            f"expect_above={expected_pct} "
            f"verdict={verdict}"
        ),
    )

    if verdict != "PASS":

        append_event(
            run_log,
            (
                "PAGE-HUMAN "
                "verification target "
                "not met"
            ),
        )

        return 1

    append_event(
        run_log,
        (
            "RESOLVE incident closed "
            "human_in_loop=true"
        ),
    )

    return 0


def run_ungated(
    args: argparse.Namespace,
) -> int:

    run_log = Path(
        args.run_log
    )

    append_event(
        run_log,
        (
            "EVENT DiskPressure "
            "mount=/var "
            "avail_pct=9 "
            "sustained=5m"
        ),
    )

    append_event(
        run_log,
        (
            "DIAGNOSE "
            "finding=low-disk-space "
            "diagnosis=correct"
        ),
    )

    append_event(
        run_log,
        (
            "PROPOSE "
            "id=scale-volume "
            "autonomy=ACT(misconfigured) "
            "cmd=resize-pvc "
            "data-var --to 2000Gi"
        ),
    )

    append_event(
        run_log,
        (
            "ACT SIMULATED "
            "resize-pvc "
            "data-var --to 2000Gi "
            "command_exit=0"
        ),
    )

    append_event(
        run_log,
        (
            "VERIFY "
            "signal="
            "node_filesystem_avail_bytes "
            "avail_pct=65 "
            "expect_above=25 "
            "verdict=PASS"
        ),
    )

    append_event(
        run_log,
        (
            "FINOPS "
            "budget_violation=true "
            "unplanned_storage_"
            "spend_usd_per_month=1840"
        ),
    )

    append_event(
        run_log,
        (
            "RESOLVE "
            "technical_signal_"
            "cleared=true "
            "governance_outcome=FAIL"
        ),
    )

    return 0


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=[
            "gated",
            "ungated",
        ],
        required=True,
    )

    parser.add_argument(
        "--approval-token",
    )

    parser.add_argument(
        "--audit-log",
        default="audit.log",
    )

    parser.add_argument(
        "--run-log",
        required=True,
    )

    return parser.parse_args()


def main() -> int:

    args = parse_args()

    runbook = load_runbook()

    if args.mode == "gated":

        return run_gated(
            args,
            runbook,
        )

    return run_ungated(
        args
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
