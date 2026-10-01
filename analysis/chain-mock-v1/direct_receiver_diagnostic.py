"""Six prebuilt R2 requests from the completed calibration; no new attacks."""
import argparse
import copy
import hashlib
import json
import os
import shutil
from pathlib import Path

from live_calibration import DirectTransport, ENDPOINT, save_new, utc
from provider_adapter import parse_response, request_endpoints
from run_journal import Journal


def build(source):
    source = Path(source)
    plan = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    events = [json.loads(line) for line in (source / "events.jsonl").read_text(encoding="utf-8").splitlines()]
    replies = {e["call_id"]: json.loads(e["data"]["body_text"])
               for e in events if e["kind"] == "response"}
    cases = []
    attacks = [c for c in plan["cases"] if c["kind"] == "attack"]
    for index, case in enumerate(attacks):
        sender = replies[case["directive_id"] + "::shared-C::sender::source"]["choices"][0]["message"]["content"]
        forms = [("source", case["source_text"]), ("sender-C", sender)]
        if index % 2:
            forms.reverse()
        for form, text in forms:
            request = copy.deepcopy(plan["request_templates"]["R2"])
            request["messages"][1]["content"] = "<agent_output>\n" + text + "\n</agent_output>"
            cases.append({"directive_id": case["directive_id"], "form": form,
                          "expected_value": case["target_value"], "request": request})
    assert len(cases) == 6
    return {"status": "INTERNALLY_FROZEN_DIRECT_RECEIVER_DIAGNOSTIC",
            "frozen_utc": utc(), "source_run": source.name,
            "source_manifest_sha256": hashlib.sha256((source / "manifest.json").read_bytes()).hexdigest(),
            "cases": cases, "max_calls": 6, "automatic_retries": 0,
            "endpoint": ENDPOINT, "proxy_enabled": False,
            "scope": "Direct R2 presentation, not natural propagation or a confirmation study."}


def run(source, destination, transport):
    frozen = build(source)
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    snapshot = destination / "source"
    snapshot.mkdir()
    for name in ("direct_receiver_diagnostic.py", "live_calibration.py", "provider_adapter.py",
                 "run_journal.py", "chain_core.py", "branch_runner.py", "build_calibration_manifest.py"):
        shutil.copy2(Path(__file__).with_name(name), snapshot / name)
    save_new(destination / "manifest.json", frozen)
    journal = Journal(destination / "events.jsonl")
    rows, used = [], {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    stopped = None
    for index, case in enumerate(frozen["cases"]):
        if stopped:
            rows.append({"directive_id": case["directive_id"], "form": case["form"], "status": "not_run:" + stopped})
            continue
        identity = {"directive_id": case["directive_id"], "arm": "direct-" + case["form"],
                    "attack_variant": "baseline", "repeat_id": 0, "branch_id": "direct"}
        record = journal.invoke(str(index), "R2", case["request"], transport, identity=identity)
        parsed = parse_response("R2", record)
        response = record.get("Response") or {}
        for key in used:
            used[key] += response.get("usage", {}).get(key, 0)
        row = {"directive_id": case["directive_id"], "form": case["form"],
               "status": parsed.diagnostics["reason"], "request_endpoints": request_endpoints(parsed, case["expected_value"]),
               "valid_calls": parsed.valid_calls, "http": record.get("HttpStatus"),
               "reported_model": response.get("model")}
        rows.append(row)
        print(json.dumps(row), flush=True)
        if record.get("HttpStatus") != 200 or parsed.diagnostics["reason"] == "model_mismatch":
            stopped = "endpoint_error"
    report = {"status": stopped or "completed", "finished_utc": utc(), "rows": rows,
              "calls": sum(e["kind"] == "request" for e in journal.events), "usage": used,
              "tools_executed": 0, "scope": frozen["scope"]}
    save_new(destination / "report.json", report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-run", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    key = os.environ.get("DASHSCOPE_TP_API_KEY")
    if not key:
        raise SystemExit("DASHSCOPE_TP_API_KEY unavailable")
    run(args.source_run, args.run_dir, DirectTransport(key))
