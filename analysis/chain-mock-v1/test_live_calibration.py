import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from live_calibration import run
from test_provider_adapter import call, record


class LiveOrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name) / "run"

    def run_quiet(self, transport):
        with contextlib.redirect_stdout(io.StringIO()):
            return run(self.directory, transport)

    def test_full_mock_campaign_and_freeze(self):
        def transport(request):
            self.assertTrue((self.directory / "manifest.json").exists())
            self.assertTrue((self.directory / "source/live_calibration.py").exists())
            if not request.get("tools"):
                response = record(content="Synthetic task")
            elif request["tools"][0]["function"]["name"] == "delegate":
                response = record([call("delegate", {"target": "R2", "payload": "Synthetic follow-up"})])
            else:
                response = record([call()])
            return 200, json.dumps(response["Response"])
        result = self.run_quiet(transport)
        self.assertEqual(result["run_status"], "completed")
        self.assertEqual(result["calls_attempted"], 48)
        self.assertTrue(result["source_unchanged_during_run"])
        rows = [json.loads(line) for line in (self.directory / "outcomes.jsonl").read_text().splitlines()]
        self.assertEqual(len(rows), 18)
        for case in {r["directive_id"] for r in rows}:
            pair = [r["sender_record_id"] for r in rows if r["directive_id"] == case and r["arm"] in ("L1", "L2")]
            self.assertEqual(pair[0], pair[1])

    def test_auth_failure_stops_after_one(self):
        result = self.run_quiet(lambda _: (401, '{"error":{"code":"invalid_key"}}'))
        self.assertEqual(result["calls_attempted"], 1)
        self.assertEqual(result["run_status"], "http_401")
        self.assertTrue(all(g["outcomes"]["protected_request"]["unknown"] == 3 for g in result["groups"]))

    def test_identity_mismatch_stops(self):
        result = self.run_quiet(lambda _: (200, json.dumps(record(content="summary", model="other")["Response"])))
        self.assertEqual(result["run_status"], "model_identity_mismatch")
        self.assertEqual(result["calls_attempted"], 1)

    def test_no_overwrite_existing_run(self):
        self.directory.mkdir()
        with self.assertRaises(FileExistsError):
            self.run_quiet(lambda _: self.fail("no call allowed"))

    def test_transport_error_limit(self):
        def fail(_):
            raise TimeoutError()
        result = self.run_quiet(fail)
        self.assertEqual(result["run_status"], "three_consecutive_errors")
        self.assertEqual(result["calls_attempted"], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
