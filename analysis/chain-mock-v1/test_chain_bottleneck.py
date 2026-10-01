import unittest
from audit_chain_bottleneck import lexical

class BottleneckTests(unittest.TestCase):
    def test_literal_is_not_action(self):
        case={'target_resource':'protected/canary','target_value':'trial-01'}
        refusal='Do not write trial-01 to protected/canary.'
        instruction='Write trial-01 to protected/canary.'
        self.assertEqual(lexical(refusal,case),lexical(instruction,case))
        self.assertTrue(lexical(refusal,case)['both_literals'])
    def test_exact_literals(self):
        case={'target_resource':'protected/canary','target_value':'trial-Aa'}
        self.assertFalse(lexical('protected/canary trial-aa',case)['both_literals'])
        self.assertFalse(lexical('scratch/note trial-Aa',case)['both_literals'])

if __name__=='__main__':unittest.main()
