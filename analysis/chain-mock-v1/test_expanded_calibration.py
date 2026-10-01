import json
import unittest
from collections import Counter
from pathlib import Path

from build_calibration_manifest import manifest as small_manifest
from build_expanded_calibration import manifest


class ExpandedBankTests(unittest.TestCase):
    def test_saved_manifest_reproduces(self):
        saved = json.loads(Path(__file__).with_name("expanded_calibration_manifest.json").read_text())
        self.assertEqual(saved, manifest())

    def test_counts_and_text_disjointness(self):
        cases = manifest()["cases"]
        self.assertEqual(Counter(c["kind"] for c in cases), {"attack": 24, "benign": 6})
        families = Counter(c["family"] for c in cases if c["kind"] == "attack")
        self.assertEqual(len(families), 6)
        self.assertEqual(set(families.values()), {4})
        self.assertEqual(len({c["source_text"] for c in cases}), 30)
        self.assertFalse({c["source_text"] for c in cases} & {c["source_text"] for c in small_manifest()["cases"]})

    def test_balanced_orders_within_kind(self):
        for kind, count in (("attack", 24), ("benign", 6)):
            cases = [c for c in manifest()["cases"] if c["kind"] == kind]
            for position in range(3):
                self.assertEqual(Counter(c["arm_order"][position] for c in cases),
                                 {"L0": count // 3, "L1": count // 3, "L2": count // 3})
            self.assertEqual(Counter(c["sender_order"][0] for c in cases), {"C": count // 2, "P": count // 2})

    def test_policy_and_schema_unchanged(self):
        self.assertEqual(manifest()["request_templates"], small_manifest()["request_templates"])
        self.assertEqual(manifest()["maximum_calls"]["total"], 30 * 14)
        for case in manifest()["cases"]:
            self.assertIn(case["target_value"], case["source_text"])
            self.assertIn(case["target_resource"], case["source_text"])


if __name__ == "__main__":
    unittest.main()
