import unittest
from collections import Counter
from utility_wording_diagnostic import manifest
from build_expanded_calibration import manifest as expanded


class UtilityManifestTests(unittest.TestCase):
    def test_pairing_and_balance(self):
        plan = manifest()
        self.assertEqual(len(plan['cases']), 12)
        self.assertEqual(plan['maximum_calls']['total'], 168)
        for wording in ('original', 'explicit-write'):
            subset = [c for c in plan['cases'] if c['wording'] == wording]
            self.assertEqual(len(subset), 6)
            self.assertEqual(len({tuple(c['arm_order']) for c in subset}), 6)
            self.assertEqual(Counter(c['sender_order'][0] for c in subset), {'C': 3, 'P': 3})
        for pair in {c['pair_id'] for c in plan['cases']}:
            a, b = [c for c in plan['cases'] if c['pair_id'] == pair]
            self.assertEqual(a['target_value'], b['target_value'])
            self.assertEqual(a['arm_order'], b['arm_order'])

    def test_preserved_original_and_policy(self):
        plan = manifest()
        originals = {c['source_text'] for c in plan['cases'] if c['wording'] == 'original'}
        prior = {c['source_text'] for c in expanded()['cases'] if c['kind'] == 'benign'}
        self.assertEqual(originals, prior)
        self.assertEqual(plan['request_templates'], expanded()['request_templates'])
        self.assertTrue(all('Write a note' in c['source_text'] for c in plan['cases'] if c['wording'] == 'explicit-write'))


if __name__ == '__main__':
    unittest.main()
