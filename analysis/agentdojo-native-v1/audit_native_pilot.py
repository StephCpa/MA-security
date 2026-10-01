"""Replay archived provider responses through the unmodified native evaluator.

No model calls. Checks request reconstruction, exposure and native state/score.
This is a deterministic replay check, not independent validation of the scorer.
"""
import argparse
import hashlib
import json
import socket
import tempfile
from pathlib import Path
from unittest.mock import patch
from native_adapter import NativeQwen,Journal
from offline_check import blocked
from live_calibration import save_new
from agentdojo.task_suite import get_suite

def audit(folder,output):
    plan=json.loads((folder/'manifest.json').read_text(encoding='utf8'))
    events=[json.loads(x) for x in (folder/'journal.jsonl').read_text(encoding='utf8').splitlines()]
    assert [e['seq'] for e in events]==list(range(len(events)))
    checks=1;requests={};responses={};tokens=0
    for e in events:
        if e['kind']=='request':
            assert e['call_id'] not in requests;checks+=1;requests[e['call_id']]=e['data']['request']
        else:
            assert e['call_id'] in requests and e['call_id'] not in responses;checks+=1;responses[e['call_id']]=e
            if e['kind']=='response':tokens+=json.loads(e['data']['body_text']).get('usage',{}).get('total_tokens',0)
    for name,digest in plan['source_sha256'].items():
        assert hashlib.sha256((folder/'source'/name).read_bytes()).hexdigest()==digest;checks+=1
    suite=get_suite(plan['benchmark'],plan['suite']);replayed=0
    with patch.object(socket,'create_connection',blocked),patch.object(socket.socket,'connect',blocked),patch.object(socket.socket,'connect_ex',blocked):
        for job in plan['jobs']:
            path=folder/(job['job_id']+'.json')
            if not path.exists():continue
            saved=json.loads(path.read_text(encoding='utf8'));index=0
            def transport(request):
                nonlocal index,checks
                key=job['job_id']+f'::t{index}';index+=1
                assert request==requests[key];checks+=1
                r=responses[key]
                if r['kind']=='error':raise RuntimeError('archived transport error')
                return r['data']['http_status'],r['data']['body_text']
            with tempfile.TemporaryDirectory() as d:
                pipeline=NativeQwen(Journal(Path(d)/'journal.jsonl'),transport,job,plan['system'],plan['turn_cap'])
                injections={} if job['arm']=='baseline' else {job['slot']:job['injected_text']}
                utility,security=suite.run_task_with_pipeline(pipeline,suite.user_tasks[job['user_id']],suite.injection_tasks[job['injection_id']],injections)
                actual={'utility':bool(utility),'security_success':bool(security)}
                for a,b in [(pipeline.complete,saved['complete']),(pipeline.reason,saved['reason']),
                            (pipeline.calls,saved['calls']),(pipeline.tool_log,saved['tool_log']),
                            (pipeline.final_environment,saved['post_environment']),(actual,saved['observed_predicates']),
                            (pipeline.messages,saved['messages']),
                            (pipeline.exposed if job['arm']!='baseline' else None,saved['exposed'])]:
                    assert a==b,job['job_id'];checks+=1
            replayed+=1
    summary=json.loads((folder/'summary.json').read_text(encoding='utf8'))
    assert summary['reported_tokens']==tokens and summary['calls']==len(requests);checks+=2
    result={'checks_passed':checks,'sessions_replayed':replayed,'model_calls_during_audit':0,'archived_calls':len(requests),
            'reported_tokens':tokens,'scope':'Provider-response replay through official native runtime and predicates; not an independent security oracle.'}
    save_new(output,result);print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();audit(a.run_dir,a.output)
