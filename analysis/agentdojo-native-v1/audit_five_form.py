"""Offline response replay and accounting for the native five-form extension."""
import argparse
import hashlib
import json
import socket
import tempfile
from pathlib import Path
from unittest.mock import patch
from five_form import decode,SENDER,MODEL
from native_adapter import NativeQwen,Journal
from offline_check import blocked
from live_calibration import save_new
from agentdojo.task_suite import get_suite

def load(path):return json.loads(path.read_text(encoding='utf8'))

def events(path):
    ev=[json.loads(s) for s in path.read_text(encoding='utf8').splitlines()]
    assert [e['seq'] for e in ev]==list(range(len(ev)))
    req={};resp={}
    for e in ev:
        if e['kind']=='request':
            assert e['call_id'] not in req;req[e['call_id']]=e['data']['request']
        else:
            assert e['call_id'] in req and e['call_id'] not in resp;resp[e['call_id']]=e
    assert set(req)==set(resp)
    return req,resp

def audit(folder,output):
    plan=load(folder/'manifest.json');bank=load(folder/'generation_bank.json');start=load(folder/'receiver_start.json')
    assert hashlib.sha256((folder/'generation_bank.json').read_bytes()).hexdigest()==start['bank_sha256']
    checks=1
    for name,digest in plan['source_sha256'].items():
        assert hashlib.sha256((folder/'source'/name).read_bytes()).hexdigest()==digest;checks+=1
    pilot=load(Path(plan['pilot'])/'manifest.json')
    assert not set(plan['users']) & {p['user_id'] for p in pilot['pairs']};checks+=1
    pairs={p['pair_id']:p for p in plan['pairs']}
    assert len(pairs)==55 and len(plan['receiver_order'])==286;checks+=1
    greq,gresp=events(folder/'generation_journal.jsonl');rreq,rresp=events(folder/'receiver_journal.jsonl')
    derived={}
    for row in bank['rows']:
        key=row['pair_id']+'-'+row['form'];p=pairs[row['pair_id']];request=greq[key]
        assert request['messages']==[{'role':'system','content':plan['sender_system']},{'role':'user','content':p['forms'][row['form'][2:]]}];checks+=1
        response=gresp[key]
        record={'HttpStatus':None,'Response':None}
        if response['kind']=='response':
            record['HttpStatus']=response['data']['http_status']
            try:record['Response']=json.loads(response['data']['body_text'])
            except ValueError:pass
        content,reason=decode(record)
        assert content==row['content'] and reason==row['reason'];checks+=1
        derived[(row['pair_id'],row['form'])]=content
    suite=get_suite(plan['benchmark'],plan['suite']);replayed=0;skipped=0
    with patch.object(socket,'create_connection',blocked),patch.object(socket.socket,'connect',blocked),patch.object(socket.socket,'connect_ex',blocked):
        for spec in plan['receiver_order']:
            p=pairs[spec['pair_id']];arm=spec['arm'];jobid=p['pair_id']+'-'+arm
            path=folder/(jobid+'-receiver.json')
            if not path.exists():continue
            row=load(path)
            payload='' if arm=='baseline' else p['forms'].get(arm,derived.get((p['pair_id'],arm)))
            if payload is None:
                assert row['reason']=='missing_generation' and row['outcomes'] is None;checks+=1;skipped+=1;continue
            index=0
            def transport(request):
                nonlocal index,checks
                key=jobid+f'::t{index}';index+=1
                assert request==rreq[key];checks+=1
                response=rresp[key]
                if response['kind']=='error':raise RuntimeError('archived transport error')
                return response['data']['http_status'],response['data']['body_text']
            job=dict(p,arm=arm,job_id=jobid,injected_text=payload)
            with tempfile.TemporaryDirectory() as d:
                pipeline=NativeQwen(Journal(Path(d)/'journal.jsonl'),transport,job,plan['system'],plan['turn_cap'],model=plan.get('model', MODEL))
                injection={} if arm=='baseline' else {p['slot']:payload}
                try:
                    u,s=suite.run_task_with_pipeline(pipeline,suite.user_tasks[p['user_id']],suite.injection_tasks[p['injection_id']],injection)
                    observed={'utility':bool(u),'security_success':bool(s)}
                except Exception as exc:
                    pipeline.complete=False;pipeline.reason='exception_'+type(exc).__name__;observed=None
                for actual,expected in [(pipeline.complete,row['complete']),(pipeline.reason,row['reason']),(pipeline.calls,row['calls']),
                                        (pipeline.messages,row['messages']),(pipeline.tool_log,row['tool_log']),(observed,row['observed_predicates']),
                                        (pipeline.exposed if arm!='baseline' else None,row['exposed_exact'])]:
                    assert actual==expected,jobid;checks+=1
                if hasattr(pipeline,'final_environment'):
                    assert pipeline.final_environment==row['post_environment'];checks+=1
            replayed+=1
    end=load(folder/'receiver_end.json')
    assert replayed==end['sessions_executed'];checks+=1
    report={'checks_passed':checks,'receiver_sessions_replayed':replayed,'generation_responses_checked':len(bank['rows']),
            'missing_generation_sessions':skipped,'model_calls_during_audit':0,'archived_generation_calls':len(greq),'archived_receiver_calls':len(rreq),
            'scope':'Replay through official runtime/predicates; scorer itself is not independently validated by this audit.'}
    save_new(output,report);print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();audit(a.run_dir,a.output)
