"""Replay audit for the completed matched DeepSeek Slack screen."""
import argparse,json,socket,tempfile,hashlib
from pathlib import Path
from unittest.mock import patch
from native_adapter import NativeQwen,Journal
from offline_check import blocked
from live_calibration import save_new
from agentdojo.task_suite import get_suite

def main(folder,output):
 plan=json.loads((folder/'manifest.json').read_text(encoding='utf8'));events=[json.loads(s) for s in (folder/'journal.jsonl').read_text(encoding='utf8').splitlines()];req={};resp={}
 for e in events:
  if e['kind']=='request':assert e['call_id'] not in req;req[e['call_id']]=e['data']['request']
  else:assert e['call_id'] in req and e['call_id'] not in resp;resp[e['call_id']]=e
 assert set(req)==set(resp);checks=2
 for name,d in plan['source_sha256'].items():assert hashlib.sha256((folder/'source'/name).read_bytes()).hexdigest()==d;checks+=1
 suite=get_suite(plan['benchmark'],plan['suite']);rows=0;per_session={}
 with patch.object(socket,'create_connection',blocked),patch.object(socket.socket,'connect',blocked),patch.object(socket.socket,'connect_ex',blocked):
  for q in plan['jobs']:
   path=folder/(q['job_id']+'.json');assert path.exists();saved=json.loads(path.read_text(encoding='utf8'));idx=0
   def transport(request):
    nonlocal idx,checks
    k=q['job_id']+f'::t{idx}';idx+=1;assert k in req;checks+=1
    e=resp[k];assert e['kind']=='response';return e['data']['http_status'],e['data']['body_text']
   inj={} if q['arm']=='baseline' else {q['slot']:q['raw_goal']};env=suite.load_and_inject_default_environment(inj)
   with tempfile.TemporaryDirectory() as d:
    p=NativeQwen(Journal(Path(d)/'j.jsonl'),transport,dict(q,injected_text='' if q['arm']=='baseline' else q['raw_goal']),plan['system'],plan['turn_cap'],model=plan['model'])
    u,s=suite.run_task_with_pipeline(p,suite.user_tasks[q['user_id']],suite.injection_tasks[q['injection_id']],inj,environment=env);actual={'utility':bool(u),'security_success':bool(s)}
    assert p.complete==saved['complete'] and p.reason==saved['reason'] and p.calls==saved['calls'];assert actual==saved['outcomes'];assert p.messages==saved['messages'];assert p.tool_log==saved['tool_log'];checks+=5
   rows+=1
 report={'checks_passed':checks,'sessions_replayed':rows,'archived_model_calls':len(req),'model_calls_during_audit':0,'scope':'Response replay through official runtime/predicates; not an independent scorer validation.'};save_new(output,report);print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.run_dir.resolve(),a.output.resolve())
