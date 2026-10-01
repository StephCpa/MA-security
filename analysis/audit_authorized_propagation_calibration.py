"""Independent offline recount for the authorized-propagation calibration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run = Path(args.run_dir)
    rows = [json.loads(line) for line in (run / "outcomes.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    result = {"status": "completed", "provider_calls": 0,
              "scope": "offline recount; no provider calls", "counts": {}}
    events = [json.loads(line) for line in (run / "events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    result["provider_calls"] = sum(event["kind"] == "request" for event in events)
    for arm in ("L0", "L2"):
        subset = [row for row in rows if row["arm"] == arm]
        result["counts"][arm] = {
            "n": len(subset),
            "r1_delegated": sum(row.get("r1_delegated") is True for row in subset),
            "r2_called": sum(row.get("r2_called") is True for row in subset),
            "protected_request": sum(row.get("protected_request") is True for row in subset),
            "exact_protected_request": sum(row.get("exact_protected_request") is True for row in subset),
        }
    report = json.loads((run / "report.json").read_text(encoding="utf-8"))
    result["matches_report"] = result["counts"] == report["counts"] and result["provider_calls"] == report["actual_model_calls"]
    if not result["matches_report"]:
        raise SystemExit(json.dumps(result, indent=2))
    output = Path(args.output)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
