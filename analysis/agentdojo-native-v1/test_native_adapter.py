import json
import tempfile
import unittest
from pathlib import Path
from native_adapter import NativeQwen,Journal,strict_args,MODEL
from agentdojo.task_suite import get_suite
from agentdojo.functions_runtime import FunctionsRuntime

def response(calls=None):
    return 200,json.dumps({'model':MODEL,'choices':[{'finish_reason':'tool_calls' if calls else 'stop','message':{'role':'assistant','content':'Done','tool_calls':calls}}]})

class Tests(unittest.TestCase):
    def test_arguments(self):
        for bad in ('{"x":1,"x":2}','{"x":NaN}','[]'):
            with self.assertRaises(ValueError):strict_args(bad)
        self.assertEqual(strict_args('{"x":1}'),{'x':1})
    def check_pipeline(self,name,cap):
        suite=get_suite('v1.2.2','slack');env=suite.load_and_inject_default_environment({})
        call={'id':'c1','type':'function','function':{'name':name,'arguments':'{}'}}
        responses=iter([response([call]),response()])
        with tempfile.TemporaryDirectory() as d:
            j=Journal(Path(d)/'events.jsonl')
            p=NativeQwen(j,lambda req:next(responses),{'pair_id':'test','arm':'raw','job_id':'test','injected_text':'general'},'test',cap)
            result=p.query('List channels',FunctionsRuntime(suite.tools),env)
            self.assertEqual(len(p.tool_log),1)
            self.assertEqual(len(j.events),p.calls*2)
            self.assertEqual(p.complete,cap==2)
            if name=='get_channels':self.assertIsNone(p.tool_log[0]['error'])
            else:self.assertIn('unregistered',p.tool_log[0]['error'])
            if cap==1:self.assertEqual(result[3][-1]['content'],[])
    def test_native_tool(self):self.check_pipeline('get_channels',2)
    def test_unknown_tool(self):self.check_pipeline('unregistered_shell',2)
    def test_cap(self):self.check_pipeline('get_channels',1)

if __name__=='__main__':unittest.main()
