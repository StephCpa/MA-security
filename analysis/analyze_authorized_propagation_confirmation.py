"""Independent paired analysis for the weak authorized-propagation run."""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


def exact_mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(0, min(b, c) + 1)) / (2 ** n)
    return min(1.0, 2.0 * tail)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run = Path(args.run_dir)
    rows = [json.loads(line) for line in (run / "outcomes.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    pairs = defaultdict(dict)
    for row in rows:
        pairs[row["directive_id"]][row["arm"]] = row
    paired = []
    for directive_id, arms in sorted(pairs.items()):
        if set(arms) != {"L0", "L2"}:
            raise SystemExit(f"incomplete pair: {directive_id}")
        l0 = bool(arms["L0"].get("exact_protected_request"))
        l2 = bool(arms["L2"].get("exact_protected_request"))
        paired.append({"directive_id": directive_id, "family": arms["L0"]["family"], "L0": l0, "L2": l2})
    n = len(paired)
    l0 = sum(row["L0"] for row in paired)
    l2 = sum(row["L2"] for row in paired)
    b = sum(row["L0"] and not row["L2"] for row in paired)
    c = sum(row["L2"] and not row["L0"] for row in paired)
    result = {
        "status": "completed",
        "provider_calls": 0,
        "estimand": "paired exact protected request among receiver-authorized R2 chains",
        "n_pairs": n,
        "L0_exact": l0,
        "L2_exact": l2,
        "risk_difference_L2_minus_L0": l2 / n - l0 / n,
        "discordant_L0_only": b,
        "discordant_L2_only": c,
        "mcnemar_two_sided_exact_p": exact_mcnemar(b, c),
        "family_breakdown": {},
        "scope": "fixture comparison; not unauthorized mutation, defense efficacy, or natural propagation",
    }
    families = sorted({row["family"] for row in paired})
    for family in families:
        subset = [row for row in paired if row["family"] == family]
        result["family_breakdown"][family] = {
            "n": len(subset), "L0_exact": sum(row["L0"] for row in subset),
            "L2_exact": sum(row["L2"] for row in subset),
            "discordant_L0_only": sum(row["L0"] and not row["L2"] for row in subset),
            "discordant_L2_only": sum(row["L2"] and not row["L0"] for row in subset),
        }
    result["pairs"] = paired
    with Path(args.output).open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
