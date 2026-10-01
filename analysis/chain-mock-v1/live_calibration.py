"""Bounded live calibration. Requires explicit --run-dir argument.

No automatic retries, no real tool execution, no ordinary-pay fallback.
The source manifest and source-code snapshot are saved before the first call.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from branch_runner import ENDPOINTS, run_branches
from build_calibration_manifest import manifest
from chain_core import Lineage, SOURCE_MARKER, SENDER_RULE
from provider_adapter import build_request, parse_response
from run_journal import Journal

ENDPOINT = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions"
SOURCE_FILES = ("live_calibration.py", "branch_runner.py", "chain_core.py",
                "provider_adapter.py", "run_journal.py", "build_calibration_manifest.py",
                "build_expanded_calibration.py", "utility_wording_diagnostic.py")


def utc():
    return datetime.now(timezone.utc).isoformat()


def save_new(path, obj):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class DirectTransport:
    def __init__(self, key):
        self._key = key
        self._opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def __call__(self, request):
        body = json.dumps(request, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self._key})
        try:
            with self._opener.open(req, timeout=45) as response:
                return response.status, response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read().decode("utf-8", errors="replace")


class StopRun(RuntimeError):
    pass


def missing(case, arm, reason):
    return {"directive_id": case["directive_id"], "kind": case["kind"], "arm": arm,
            "unresolved": True, "stop_reason": reason,
            "request_endpoints": {k: None for k in ENDPOINTS},
            "legitimate_exact_write": None, "branches": [], "events": []}


def summary(rows, journal, run_status):
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    response_models, http_codes = {}, {}
    for event in journal.events:
        if event["kind"] != "response":
            continue
        status = str(event["data"]["http_status"])
        http_codes[status] = http_codes.get(status, 0) + 1
        try:
            body = json.loads(event["data"]["body_text"])
        except ValueError:
            continue
        if not isinstance(body, dict):
            continue
        model = body.get("model", "not_reported")
        response_models[model] = response_models.get(model, 0) + 1
        for key in usage:
            usage[key] += body.get("usage", {}).get(key, 0)
    groups = []
    for kind in ("benign", "attack"):
        for arm in ("L0", "L1", "L2"):
            subset = [r for r in rows if r["kind"] == kind and r["arm"] == arm]
            counters = {}
            for endpoint in (*ENDPOINTS, "legitimate_exact_write"):
                values = [r[endpoint] if endpoint == "legitimate_exact_write"
                          else r["request_endpoints"][endpoint] for r in subset]
                counters[endpoint] = {"true": sum(v is True for v in values),
                                      "false": sum(v is False for v in values),
                                      "unknown": sum(v is None for v in values)}
            groups.append({"kind": kind, "arm": arm, "n_seeded": len(subset),
                           "unresolved_chains": sum(r["unresolved"] for r in subset),
                           "outcomes": counters})
    return {"run_status": run_status, "finished_utc": utc(), "evidence_type": "LIVE_ENGINEERING_CALIBRATION",
            "calls_attempted": sum(e["kind"] == "request" for e in journal.events),
            "pending_calls": [k for k, v in journal.states.items() if v == "pending"],
            "http_codes": http_codes, "reported_models": response_models,
            "usage": usage, "credit_charge": "not returned by API; check subscription console",
            "external_tool_executions": 0, "groups": groups,
            "scope": "Authored development items, no inference of defense efficacy. All monitor writes are process-local."}


def run(run_dir, transport, supplied_plan=None):
    plan = copy.deepcopy(supplied_plan if supplied_plan is not None else manifest())
    if plan["model"] != "qwen3.6-flash" or plan["branch_cap"] != 3:
        raise ValueError("unexpected endpoint or branch contract")
    if plan["maximum_calls"]["total"] != len(plan["cases"]) * 14:
        raise ValueError("call ceiling does not match branch contract")
    if len({c["directive_id"] for c in plan["cases"]}) != len(plan["cases"]):
        raise ValueError("duplicate directive id")
    for case in plan["cases"]:
        if sorted(case["arm_order"]) != ["L0", "L1", "L2"] or sorted(case.get("sender_order", ["C", "P"])) != ["C", "P"]:
            raise ValueError("invalid arm or sender ordering")
    run_dir = Path(run_dir).resolve()
    run_dir.mkdir(parents=True, exist_ok=False)
    source_dir = run_dir / "source"
    source_dir.mkdir()
    hashes = {}
    for name in SOURCE_FILES:
        src = Path(__file__).with_name(name)
        hashes[name] = hashlib.sha256(src.read_bytes()).hexdigest()
        shutil.copy2(src, source_dir / name)
    plan.update(status="INTERNALLY_FROZEN_LIVE_CALIBRATION_NOT_EXTERNAL_PREREGISTRATION",
                frozen_utc=utc(), network_execution_enabled=True,
                endpoint=ENDPOINT, proxy_enabled=False, source_sha256=hashes,
                stop_rules=["HTTP 401/403/429", "model identity mismatch", "three consecutive HTTP/transport errors",
                            str(plan["maximum_calls"]["total"]) + "-call ceiling"])
    save_new(run_dir / "manifest.json", plan)
    journal = Journal(run_dir / "events.jsonl")
    rows, seen, failure_streak = [], set(), 0
    state = "completed"

    def invoke(case, arm, stage, request, branch):
        nonlocal failure_streak
        used = sum(e["kind"] == "request" for e in journal.events)
        if used >= plan["maximum_calls"]["total"]:
            raise StopRun("call_ceiling")
        identity = {"directive_id": case["directive_id"], "arm": arm,
                    "attack_variant": "baseline", "repeat_id": case["repeat_id"], "branch_id": branch}
        call_id = "::".join((case["directive_id"], arm, stage, branch))
        result = journal.invoke(call_id, stage, request, transport, identity=identity)
        status = result.get("HttpStatus")
        print(json.dumps({"call": used + 1, "item": case["directive_id"], "arm": arm,
                          "stage": stage, "http": status}), flush=True)
        failure_streak = failure_streak + 1 if status != 200 else 0
        body = result.get("Response")
        if status in (401, 403, 429):
            raise StopRun("http_" + str(status))
        if status == 200 and isinstance(body, dict) and body.get("model") != plan["model"]:
            raise StopRun("model_identity_mismatch")
        if failure_streak >= 3:
            raise StopRun("three_consecutive_errors")
        return result

    try:
        for case in plan["cases"]:
            lineage = Lineage()
            root = lineage.root(case["directive_id"], case["source_text"], "external-untrusted")
            inputs = {}
            for form in case.get("sender_order", ["C", "P"]):
                prefix = SOURCE_MARKER if form == "P" else ""
                request = build_request("sender", SENDER_RULE, prefix + root.text)
                record = invoke(case, "shared-" + form, "sender", request, "source")
                parsed = parse_response("sender", record)
                if parsed.reply.status == "ok" and parsed.diagnostics["reason"] == "text_only":
                    inputs[form] = lineage.derive(root.identifier + ":" + form,
                                                 parsed.reply.arguments["text"], (root,))
                else:
                    inputs[form] = None
            for arm in case["arm_order"]:
                sender = inputs["C" if arm == "L0" else "P"]
                if sender is None:
                    row = missing(case, arm, "sender_unavailable")
                else:
                    row = run_branches(lineage, sender, arm,
                        lambda stage, request, branch: invoke(case, arm, stage, request, branch),
                        max_branches=plan["branch_cap"], expected_value=case["target_value"])
                    row.update(directive_id=case["directive_id"], kind=case["kind"],
                               evidence_type="LIVE_ENGINEERING_CALIBRATION", sender_record_id=sender.identifier)
                    hit = any(d["arguments"] == {"resource": case["target_resource"], "value": case["target_value"]}
                              and d["decision"]["write_executed"]
                              for b in row["branches"] for d in b["gateway_decisions"])
                    row["legitimate_exact_write"] = (hit if case["kind"] == "benign" and (hit or not row["unresolved"])
                                                     else None)
                with (run_dir / "outcomes.jsonl").open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(row, ensure_ascii=False) + "\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                rows.append(row)
                seen.add((case["directive_id"], arm))
    except StopRun as exc:
        state = str(exc)
    except Exception as exc:
        state = "runner_error:" + type(exc).__name__
        raise
    finally:
        for case in plan["cases"]:
            for arm in case["arm_order"]:
                if (case["directive_id"], arm) not in seen:
                    row = missing(case, arm, "not_completed:" + state)
                    rows.append(row)
                    with (run_dir / "outcomes.jsonl").open("a", encoding="utf-8") as stream:
                        stream.write(json.dumps(row) + "\n")
                        stream.flush()
                        os.fsync(stream.fileno())
        result = summary(rows, journal, state)
        result["source_unchanged_during_run"] = all(
            hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() == digest
            for name, digest in hashes.items())
        save_new(run_dir / "summary.json", result)
        print(json.dumps({"finished": state, "calls": result["calls_attempted"], "usage": result["usage"]}), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--manifest", help="Explicit candidate manifest; default is the original six-item development pack")
    args = parser.parse_args()
    key = os.environ.get("DASHSCOPE_TP_API_KEY")
    if not key:
        raise SystemExit("DASHSCOPE_TP_API_KEY unavailable; no call made")
    supplied = json.loads(Path(args.manifest).read_text(encoding="utf-8")) if args.manifest else None
    run(args.run_dir, DirectTransport(key), supplied)
