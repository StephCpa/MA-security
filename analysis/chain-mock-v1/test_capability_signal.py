import unittest
from capability_signal import build,parse,CUE
from test_selector_transportability import response


class SignalTests(unittest.TestCase):
    def test_factor_contract(self):
        p=build();self.assertEqual(len(p['cases']),252)
        by={}
        for c in p['cases']:by.setdefault((c['stimulus_id'],c['a']),{})[c['signal']]=c
        self.assertEqual(len(by),126)
        for arms in by.values():
            left,right=arms[0],arms[1]
            self.assertEqual(left['payload'],right['payload'])
            self.assertEqual(left['request']['tools'],right['request']['tools'])
            self.assertEqual(left['request']['messages'][1],right['request']['messages'][1])
            self.assertEqual(right['request']['messages'][0]['content'].replace('\n'+CUE,''),left['request']['messages'][0]['content'])
            self.assertEqual(left['b'],1)
            self.assertEqual(right['b'],1)

    def test_parse_and_unknown(self):
        r=response('write_shared',{'resource':'protected/canary','value':'test'})
        self.assertEqual(parse(r)[0].kind,'write_shared')
        self.assertIsNone(parse(response('write_shared',{'resource':'x','value':9}))[0])
        self.assertEqual(parse(response(finish='length'))[1],'incomplete')


if __name__=='__main__':unittest.main()
