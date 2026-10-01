import unittest
from collections import Counter
from provenance_rerender import build,CUE

class CueTests(unittest.TestCase):
    def test_full_bank_and_only_cue_diff(self):
        plan=build();self.assertEqual(Counter(c['form'] for c in plan['cases']),{'S_C':96,'S_P':96,'AUTH':12})
        lookup={(c['stimulus_id'],c['signal']):c for c in plan['cases']}
        for ident in {c['stimulus_id'] for c in plan['cases']}:
            left,right=lookup[ident,0],lookup[ident,1]
            self.assertEqual(left['payload'],right['payload'])
            self.assertTrue(left['request']['messages'][0]['content'].endswith(left['payload']))
            self.assertTrue(right['request']['messages'][0]['content'].endswith(right['payload']))
            altered=right['request'].copy();altered['messages']=[m.copy() for m in altered['messages']]
            altered['messages'][0]['content']=altered['messages'][0]['content'].replace(CUE+'\n','',1)
            self.assertEqual(altered,left['request'])
            self.assertEqual(left['b'],right['b'])
            if left['kind']=='authorized_control':
                self.assertEqual(left['resource'],f"session/{left['session_id']}/authorized/output")

if __name__=='__main__':unittest.main()
