import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from collections import Counter
from provenance_neutral_control import build,NEUTRAL,CUE
from capability_signal import run
from audit_provenance_rerender import audit
from test_selector_transportability import response

class NeutralTests(unittest.TestCase):
    def test_three_arm_contract_and_audit(self):
        plan=build()
        self.assertEqual(len(NEUTRAL.split()),len(CUE.split()))
        self.assertEqual(Counter(c['signal'] for c in plan['cases']),{0:102,1:102,2:102})
        self.assertFalse(plan['report_primary_p'])
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'run'
            def mock(req):return 200,json.dumps(response('summarize',{'summary':'offline'})['Response'])
            with contextlib.redirect_stdout(io.StringIO()):run(target,mock,plan=plan)
            report=audit(target)
            self.assertTrue(report['all_checks_pass'])
            self.assertEqual(len(report['groups']),9)
            self.assertEqual(report['contrasts']['S_C']['n'],48)
            self.assertNotIn('two_sided_exact_McNemar_p',report['contrasts']['S_C'])
            self.assertIn('conservative_95_paired_projection',report['contrasts']['S_C'])

if __name__=='__main__':unittest.main()
