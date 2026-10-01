"""Matched native Slack pilot for the existing ten-pair bank on DeepSeek."""
import argparse,hashlib,json,os,shutil,sys,urllib.request,urllib.error
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/'chain-mock-v1'))
from native_adapter import NativeQwen,Journal,wire
from live_calibration import save_new,utc
from agentdojo.task_suite import get_suite
from agentdojo.agent_pipeline.agent_pipeline import load_system_message
HERE=Path(__file__).resolve().parent;MODEL='deepseek-flash';ENDPOINT='https://api.deepseek.com/chat/completions'
class Transport:
 def __init__(self,key):self.key=key;self.opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 def __call__(self,request):
  payload=dict(request);payload.pop('enable_thinking',None);payload['thinking']={'type':'disabled'}
  req=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),method='POST',headers={'Authorization':'Bearer '+self.key,'Content-Type':'application/json'})
  try:
   with self.opener.open(req,timeout=90) as r:return r.status,r.read().decode()
  except urllib.error.HTTPError as e:return e.code,e.read().decode(errors='replace')
def key():
 v=os.environ.get('DEEPSEEK_API_KEY')
 if not v:
  import winreg
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as k:v=winreg.QueryValueEx(k,'DEEPSEEK_API_KEY')[0]
 if not v:raise RuntimeError('DEEPSEEK_API_KEY unavailable')
 return v
def freeze(out,pilot):
 pm=json.loads((pilot/'manifest.json').read_text());out.mkdir(parents=True,exist_ok=False);(out/'source').mkdir();plan={'frozen_utc':utc(),'model':MODEL,'endpoint':ENDPOINT,'benchmark':'v1.2.2','package':'0.1.35','suite':'slack','source_pilot':str(pilot.resolve()),'pairs':pm['pairs'],'jobs':[dict(p,arm=a,job_id=p['pair_id']+'-'+a) for p in pm['pairs'] for a in ('baseline','raw')],'system':load_system_message(None),'turn_cap':12,'scope':'Matched ten-pair native Slack model comparison; descriptive feasibility only. Pairs were fixed before this model run and not selected by outcomes.','payload':'Literal official injection goal, baseline versus raw; no marked or generated forms.','stop':'No retries; stop on HTTP 400/401/403/404/429, model mismatch or three consecutive incomplete sessions.','source_sha256':{}}
 for src in [HERE/'deepseek_slack_pilot.py',HERE/'native_adapter.py',HERE.parent/'chain-mock-v1'/'run_journal.py']:
  shutil.copy2(src,out/'source'/src.name);plan['source_sha256'][src.name]=hashlib.sha256(src.read_bytes()).hexdigest()
 save_new(out/'manifest.json',plan);print(json.dumps({'jobs':len(plan['jobs']),'frozen':str(out)}),flush=True)
def run(out):
 plan=json.loads((out/'manifest.json').read_text());jpath=out/'journal.jsonl'
 if jpath.exists():raise RuntimeError('no implicit resume')
 transport=Transport(key());j=Journal(jpath);suite=get_suite(plan['benchmark'],plan['suite']);rows=[];streak=0;status='completed'
 for q in plan['jobs']:
  p=NativeQwen(j,transport,dict(q,injected_text='' if q['arm']=='baseline' else q['raw_goal']),plan['system'],plan['turn_cap'],model=MODEL);inj={} if q['arm']=='baseline' else {q['slot']:q['raw_goal']};env=suite.load_and_inject_default_environment(inj)
  try:u,s=suite.run_task_with_pipeline(p,suite.user_tasks[q['user_id']],suite.injection_tasks[q['injection_id']],inj,environment=env);o={'utility':bool(u),'security_success':bool(s)}
  except Exception as e:p.complete=False;p.reason='exception_'+type(e).__name__;o=None
  row=dict(q,complete=p.complete,reason=p.reason,calls=p.calls,outcomes=o if p.complete else None,observed_predicates=o,exposed=p.exposed if q['arm']=='raw' else None,post_environment=getattr(p,'final_environment',wire(env)),messages=p.messages,tool_log=p.tool_log);save_new(out/(q['job_id']+'.json'),row);rows.append(row);print(json.dumps({k:row[k] for k in ('job_id','complete','calls','outcomes')}),flush=True)
  streak=0 if p.complete else streak+1
  if p.last_http in (400,401,403,404,429) or p.reason=='model_mismatch' or streak>=3:status='stopped';break
 tokens=sum(json.loads(e['data']['body_text']).get('usage',{}).get('total_tokens',0) for e in j.events if e['kind']=='response')
 save_new(out/'summary.json',{'status':status,'model':MODEL,'sessions':len(rows),'calls':sum(r['calls'] for r in rows),'reported_tokens':tokens,'groups':{a:{'complete':sum(r['complete'] for r in rows if r['arm']==a),'utility':sum(bool(r['outcomes'] and r['outcomes']['utility']) for r in rows if r['arm']==a),'security_success':sum(bool(r['outcomes'] and r['outcomes']['security_success']) for r in rows if r['arm']==a)} for a in ('baseline','raw')},'ended_utc':utc()})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['freeze','run']);p.add_argument('--run-dir',type=Path,required=True);p.add_argument('--pilot',type=Path);a=p.parse_args();(freeze if a.mode=='freeze' else run)(a.run_dir.resolve(),a.pilot.resolve() if a.pilot else None) if a.mode=='freeze' else run(a.run_dir.resolve())
