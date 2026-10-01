import tempfile
import json
import unittest
from pathlib import Path
from collections import Counter
from capability_signal import build,run
from capability_signal_repeats import build_panel
from test_selector_transportability import response

class RepeatTests(unittest.TestCase):
    def test_selection_and_requests(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'original';source.mkdir()
            base=build();(source/'manifest.json').write_text(json.dumps(base),encoding='utf8')
            panel=build_panel(source);other=build_panel(source)
            self.assertEqual(panel['selected_ids'],other['selected_ids'])
            self.assertEqual(len(panel['selected_ids']),16)
            self.assertEqual(sorted(panel['family_allocation'].values()),[2,2,3,3,3,3])
            self.assertEqual(Counter(c['repeat_id'] for c in panel['cases']),{1:64,2:64,3:64})
            originals={(c['stimulus_id'],c['a'],c['signal']):c for c in base['cases']}
            for c in panel['cases']:
                self.assertEqual(c['request'],originals[c['stimulus_id'],c['a'],c['signal']]['request'])
            # Runner IDs remain unique across identical requests; offline only.
            panel['cases']=panel['cases'][:2];panel['maximum_calls']=2
            def mock(req):return 200,json.dumps(response('summarize',{'summary':'mock'})['Response'])
            target=Path(tmp)/'run';run(target,mock,plan=panel)
            status=json.loads((target/'run_status.json').read_text())
            self.assertEqual(status['status'],'completed')
            self.assertTrue(all('::r1' in r['call_id'] for r in status['rows']))

if __name__=='__main__':unittest.main()
