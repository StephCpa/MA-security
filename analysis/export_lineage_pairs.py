"""Per-pair evidence table for the displayed-lineage confirmation (no model calls).

Answers the reviewer's request for, per paired item and arm: the sender request
hash, the R1 and R2 request hashes, the R2 response hash, the exact protected
request judgement, and the authorization and state outcome. The run's events
must show that L0 and L2 were separate live receiver calls on one shared
sender output. The runner (authorized_propagation_calibration.py) executes no
write and applies no gate, so authorization and state change are reported as
not executed, never inferred.

Usage, on the local run directory:
  python analysis/export_lineage_pairs.py \
      --run-dir <runs>/qwen36-authorized-propagation-confirmation-001 \
      --output lineage_pairs.json
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha(obj):
    text = obj if isinstance(obj, str) else json.dumps(obj, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    run = Path(a.run_dir)
    events = [json.loads(s) for s in (run / "events.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    outcomes = [json.loads(s) for s in (run / "outcomes.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    req = {e["call_id"]: e["data"] for e in events if e["kind"] == "request"}
    resp = {e["call_id"]: e["data"] for e in events if e["kind"] == "response"}
    calls = Counter(e["data"]["stage"] for e in events if e["kind"] == "request")
    rows = []
    for o in outcomes:
        cid, arm = o["directive_id"], o["arm"]
        sender_id, r1_id, r2_id = f"{cid}::sender::P", f"{cid}::{arm}::R1", f"{cid}::{arm}::R2"
        rows.append({
            "directive_id": cid, "arm": arm, "family": o.get("family"),
            "sender_request_sha256": sha(req[sender_id]["request"]) if sender_id in req else None,
            "sender_output_sha256": sha(resp[sender_id]["body_text"]) if sender_id in resp else None,
            "r1_request_sha256": sha(req[r1_id]["request"]) if r1_id in req else None,
            "r2_request_sha256": sha(req[r2_id]["request"]) if r2_id in req else None,
            "r2_output_sha256": sha(resp[r2_id]["body_text"]) if r2_id in resp else None,
            "r1_delegated": o.get("r1_delegated"),
            "exact_protected_request": o.get("exact_protected_request"),
            "authorization_decision": "not executed (receiver authorized; runner applies no gate)",
            "state_change": "not executed",
        })
    by_pair = {}
    for r in rows:
        by_pair.setdefault(r["directive_id"], {})[r["arm"]] = r
    checks = {
        "pairs_complete": all(set(v) == {"L0", "L2"} for v in by_pair.values()),
        "one_shared_sender_output_per_pair": all(
            v["L0"]["sender_output_sha256"] == v["L2"]["sender_output_sha256"] for v in by_pair.values()),
        "receiver_calls_separate_per_arm": all(
            v["L0"]["r1_request_sha256"] != v["L2"]["r1_request_sha256"] for v in by_pair.values()
            if v["L0"]["r1_request_sha256"] and v["L2"]["r1_request_sha256"]),
        "model_calls_by_stage": dict(calls),
        "total_model_calls": sum(calls.values()),
    }
    counts = {arm: sum(r["exact_protected_request"] is True for r in rows if r["arm"] == arm) for arm in ("L0", "L2")}
    result = {"run_dir_name": run.name, "checks": checks, "exact_protected_request": counts, "rows": rows}
    with Path(a.output).open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(json.dumps({"checks": checks, "exact_protected_request": counts}, indent=2))


if __name__ == "__main__":
    main()
