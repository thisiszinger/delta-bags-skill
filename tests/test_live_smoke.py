from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE_SCRIPT = REPO_ROOT / "skills" / "delta-bags" / "scripts" / "live_smoke.py"
SPEC = importlib.util.spec_from_file_location("delta_bags_live_smoke", SMOKE_SCRIPT)
assert SPEC and SPEC.loader
smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke)


class FakeResponse:
    status = 200

    def __init__(self, body: str) -> None:
        self.body = body.encode()

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self, _limit: int) -> bytes:
        return self.body


class LiveSmokeTests(unittest.TestCase):
    def test_check_uses_get_and_requires_all_markers(self) -> None:
        check = {
            "name": "example",
            "url": "https://example.test/content.json",
            "markers": ("first", "second"),
        }

        def open_request(request: object, *, timeout: float) -> FakeResponse:
            self.assertEqual(request.get_method(), "GET")
            self.assertEqual(timeout, 3.0)
            return FakeResponse("first and second")

        with mock.patch.object(smoke.urllib.request, "urlopen", side_effect=open_request):
            result = smoke.check_url(check, timeout=3.0)
        self.assertTrue(result["ok"])
        self.assertEqual(result["missingMarkers"], [])

    def test_missing_marker_fails(self) -> None:
        check = {
            "name": "example",
            "url": "https://example.test/content.json",
            "markers": ("present", "missing"),
        }
        with mock.patch.object(
            smoke.urllib.request, "urlopen", return_value=FakeResponse("present")
        ):
            result = smoke.check_url(check, timeout=3.0)
        self.assertFalse(result["ok"])
        self.assertEqual(result["missingMarkers"], ["missing"])


if __name__ == "__main__":
    unittest.main()
