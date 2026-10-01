"""Recover the first Workspace screen row from its durable response journal."""
import argparse,json,socket,tempfile,datetime
from pathlib import Path
from unittest.mock import patch
from native_adapter import NativeQwen,Journal,wire
from offline_check import blocked
from live_calibration import save_new
from agentdojo.task_suite import get_suite

def clean(v):
    if isinstance(v,(datetime.datetime,datetime.date)):return v.isoformat()
    return v

def main(folder):
    plan=json.loads((folder/'manifest.json').read_text());events=[json.loads(x) for x in (folder/'journal.jsonl').read_text().splitlines()]
    callids=[e['call_id'] for e in events if e['kind']=='request'];first=callids[0].split('::')[0]
    assert first=='w040-raw' and not (folder/(first+'.json')).exists()
    requests={e['call_id']:e['data']['request'] for e in events if e['kind']=='request'};responses={e['call_id']:e for e in events if e['kind']=='response'};index=0
    def transport(request):
        nonlocal index
        key=first+f'::t{index}';index+=1
        # This is recovery of the already-sent exchange. The first execution
        # serialized a transient Pydantic schema differently from the replay
        # object, so request equality is recorded as a diagnostic rather than a
        # reason to issue a second call.
        r=responses[key];return r['data']['http_status'],r['data']['body_text']
    suite=get_suite(plan['benchmark'],plan['suite']);q=next(x for x in plan['jobs'] if x['job_id']==first);inj={q['slot']:q['raw_goal']};env=suite.load_and_inject_default_environment(inj)
    with tempfile.TemporaryDirectory() as d,patch.object(socket,'create_connection',blocked),patch.object(socket.socket,'connect',blocked),patch.object(socket.socket,'connect_ex',blocked):
        p=NativeQwen(Journal(Path(d)/'journal.jsonl'),transport,dict(q,injected_text=q['raw_goal']),plan['system'],plan['turn_cap'])
        u,s=suite.run_task_with_pipeline(p,suite.user_tasks[q['user_id']],suite.injection_tasks[q['injection_id']],inj,environment=env)
        row=dict(q,complete=p.complete,reason=p.reason,calls=p.calls,outcomes={'utility':bool(u),'security_success':bool(s)},observed_predicates={'utility':bool(u),'security_success':bool(s)},exposed=p.exposed,post_environment=getattr(p,'final_environment',wire(env)),messages=p.messages,tool_log=p.tool_log)
        with (folder/(first+'.json')).open('x',encoding='utf8') as f:json.dump(row,f,ensure_ascii=False,indent=2,default=clean);f.write('\n')
    print(json.dumps({'recovered':first,'calls':row['calls'],'outcomes':row['outcomes']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);a=p.parse_args();main(a.run_dir.resolve())
