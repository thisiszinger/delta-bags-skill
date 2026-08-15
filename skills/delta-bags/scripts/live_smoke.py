#!/usr/bin/env python3
"""Run read-only reachability and marker checks against Delta public content."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


CHECKS = (
    {
        "name": "form-content",
        "url": "https://www.delta.com/content/www/en_US/baggage/guarantee.baggagedata.json",
        "markers": ("first_name", "skymiles_number", "confirmation_number"),
    },
    {
        "name": "result-content",
        "url": "https://www.delta.com/content/www/en_US/baggage/guarantee-messages.baggagedata.json",
        "markers": ("Claim Successful",),
    },
)


def check_url(check: dict[str, Any], *, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        check["url"],
        headers={"User-Agent": "delta-bags-skill-live-smoke/0.1 (+read-only GET)"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read(2_000_000).decode("utf-8", errors="replace")
        missing = [marker for marker in check["markers"] if marker not in body]
        return {
            "name": check["name"],
            "url": check["url"],
            "httpStatus": response.status,
            "missingMarkers": missing,
            "ok": 200 <= response.status < 300 and not missing,
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read Delta public content with GET requests only; never submit a request."
    )
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    results: list[dict[str, Any]] = []
    for check in CHECKS:
        try:
            results.append(check_url(check, timeout=args.timeout))
        except (OSError, urllib.error.URLError) as error:
            results.append(
                {
                    "name": check["name"],
                    "url": check["url"],
                    "ok": False,
                    "error": str(error),
                }
            )

    print(json.dumps({"readOnly": True, "checks": results}, indent=2, sort_keys=True))
    return 0 if all(result["ok"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
