import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from provenance_rerender import build
from capability_signal import run
from audit_provenance_rerender import audit
from test_selector_transportability import response

class AuditCueTests(unittest.TestCase):
    def test_mock_and_detect_changed_outcome(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination=Path(tmp)/'run'
            def mock(req):return 200,json.dumps(response('summarize',{'summary':'offline fixture'})['Response'])
            with contextlib.redirect_stdout(io.StringIO()):run(destination,mock,plan=build())
            report=audit(destination)
            self.assertTrue(report['all_checks_pass'])
            self.assertEqual(report['contrasts']['S_C']['n'],48)
            self.assertEqual(report['contrasts']['S_C']['two_sided_exact_McNemar_p'],1)
            self.assertNotIn('two_sided_exact_McNemar_p',report['contrasts']['S_P'])
            rows=[json.loads(s) for s in (destination/'outcomes.jsonl').read_text().splitlines()]
            rows[0]['exact_request']=True
            (destination/'outcomes.jsonl').write_text('\n'.join(json.dumps(r) for r in rows)+'\n')
            self.assertFalse(audit(destination)['all_checks_pass'])

if __name__=='__main__':unittest.main()
