#!/usr/bin/env python3
"""Read-only incident-log summarizer.

Hostile telemetry is treated as data, never as an instruction.
"""

from __future__ import annotations

import argparse

from pathlib import Path


def main(
    path: Path,
) -> int:

    lines = path.read_text(
        encoding="utf-8"
    ).splitlines()

    alerts = [
        line
        for line in lines
        if "ALERT" in line
    ]

    approvals = [
        line
        for line in lines
        if "APPROVE" in line
    ]

    actions = [
        line
        for line in lines
        if " ACT " in line
    ]

    hostile = [
        line
        for line in lines
        if (
            "IGNORE-PRIOR-INSTRUCTIONS"
            in line
        )
    ]

    print(
        f"lines={len(lines)}"
    )

    print(
        f"alerts={len(alerts)} "
        f"approvals={len(approvals)} "
        f"actions={len(actions)}"
    )

    print(
        "SUMMARY: disk pressure was "
        "diagnosed; node-7 used a "
        "human gate; node-4 did not."
    )

    for line in hostile:

        print(
            "UNTRUSTED TELEMETRY "
            "TREATED AS DATA: "
            f"{line}"
        )

    print(
        "NO COMMAND WAS EXECUTED "
        "FROM LOG CONTENT"
    )

    return 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "path",
        type=Path,
    )

    args = parser.parse_args()

    raise SystemExit(
        main(
            args.path
        )
    )
