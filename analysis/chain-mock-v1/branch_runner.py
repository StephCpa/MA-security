"""Offline bounded-fanout runner, extending rather than replacing chain_core v1."""
from dataclasses import asdict

from chain_core import IntegrityError, R1_RULE, R2_RULE, gateway, render_receiver
from provider_adapter import build_request, parse_response, request_endpoints

ENDPOINTS = ("any_write_request", "nonallowlisted_request", "protected_request",
             "exact_protected_request")


def aggregate(branches, unresolved=False):
    """True if witnessed; False only when every relevant branch is known false."""
    result = {}
    for key in ENDPOINTS:
        values = [branch[key] for branch in branches]
        result[key] = (True if any(v is True for v in values) else
                       None if unresolved or any(v is None for v in values) else False)
    return result


def run_branches(lineage, sender_record, arm, invoke, *, max_branches=3,
                 expected_value="changed", capability=True, enforce=True):
    """invoke(stage, request, branch_id) returns a recorded API-format object.

    R1 valid delegations are dispatched in returned order, up to max_branches.
    Excess, malformed, and missing branches remain explicitly unresolved.
    No original source is reinserted; all valid R2 writes are evaluated in order.
    """
    if type(max_branches) is not int or max_branches < 1:
        raise ValueError("positive integer branch budget required")
    result = {"evidence_type": "OFFLINE_BRANCH_RUNNER", "arm": arm,
              "branch_cap": max_branches, "branches": [], "events": [],
              "unresolved": False, "omitted_call_ids": [],
              "store_after": {"protected/canary": "initial"}}

    def fail(reason):
        result.update(unresolved=True, stop_reason=reason,
                      request_endpoints=aggregate([], True))
        return result

    try:
        r1_text = render_receiver(lineage, sender_record, arm)
    except IntegrityError:
        return fail("invalid_sender_lineage")
    r1_request = build_request("R1", R1_RULE, r1_text)
    r1_record = invoke("R1", r1_request, "root")
    r1 = parse_response("R1", r1_record)
    result["events"].append({"stage": "R1", "record": r1_record, "parsed": asdict(r1)})
    if not r1.diagnostics["complete"]:
        return fail("R1_incomplete")
    if r1.diagnostics["reason"] in ("text_only", "explicit_refusal"):
        result.update(stop_reason="observed_nondelegation", request_endpoints=aggregate([]))
        return result
    result["unresolved"] = bool(r1.invalid_calls) or not r1.valid_calls
    selected = r1.valid_calls[:max_branches]
    result["omitted_call_ids"] = [c["id"] for c in r1.valid_calls[max_branches:]]
    result["unresolved"] |= bool(result["omitted_call_ids"])
    for index, delegation in enumerate(selected):
        branch_id = str(index)
        child = lineage.derive(sender_record.identifier + ":" + arm + ":branch:" + branch_id,
                               delegation["arguments"]["payload"], (sender_record,))
        request = build_request("R2", R2_RULE, render_receiver(lineage, child, arm))
        record = invoke("R2", request, branch_id)
        parsed = parse_response("R2", record)
        endpoints = request_endpoints(parsed, expected_value)
        decisions = []
        # Incomplete responses retain witnessed request observations but are not executed.
        executable = parsed.diagnostics["complete"] and not parsed.invalid_calls
        if executable:
            for call in parsed.valid_calls:
                decisions.append({"call_id": call["id"], "arguments": call["arguments"],
                                  "decision": gateway(call["arguments"], capability=capability,
                                                      enforce=enforce, store=result["store_after"])})
        result["branches"].append({"branch_id": branch_id,
                                   "r1_call_id": delegation["id"],
                                   "request_endpoints": endpoints,
                                   "gateway_decisions": decisions})
        result["events"].append({"stage": "R2", "branch_id": branch_id,
                                  "record": record, "parsed": asdict(parsed)})
        result["unresolved"] |= (not executable or any(v is None for v in endpoints.values()))
    result["request_endpoints"] = aggregate(
        [b["request_endpoints"] for b in result["branches"]], result["unresolved"])
    result["stop_reason"] = "partial" if result["unresolved"] else "complete"
    return result
