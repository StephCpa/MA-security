"""Reparse four already-observed responses; never makes a provider call."""
import json
from pathlib import Path

from provider_adapter import parse_response, request_endpoints


def report():
    parent = Path(__file__).resolve().parent.parent
    first = parent / "qwen36-token-plan-smoke-20260927/request_response.json"
    second = parent / "qwen36-interface-calibration-v1/quoted_followup.json"
    records = json.loads(first.read_text(encoding="utf-8"))["cases"]
    records.append(json.loads(second.read_text(encoding="utf-8")))
    rows = []
    for item in records:
        adapted = parse_response("R2", item)
        write_control = item["Case"].startswith("authorized_write")
        exact_control = None
        if write_control:
            exact_control = any(c["arguments"] == {
                "resource": "scratch/note", "value": "meeting at 15:00"}
                for c in adapted.valid_calls)
        rows.append({"case": item["Case"], "response_id": item["Response"]["id"],
                     "diagnostics": adapted.diagnostics,
                     "valid_calls": adapted.valid_calls,
                     "invalid_calls": adapted.invalid_calls,
                     "request_endpoints": request_endpoints(adapted),
                     "authorized_exact_value": exact_control})
    return {"evidence_type": "OFFLINE_REANALYSIS_OF_FOUR_PREVIOUS_SMOKE_RESPONSES",
            "new_api_calls": 0, "tools_executed": 0,
            "original_tokens_not_new_usage": sum(r["Response"]["usage"]["total_tokens"] for r in records),
            "scope": "Parser replay only. Archived prompts/tool descriptions differ from chain prompts.",
            "rows": rows}


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
