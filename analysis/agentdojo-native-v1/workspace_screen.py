"""Bounded Workspace headroom screen on tasks with non-empty official references."""
import argparse,hashlib,json,os,random,shutil,sys,datetime
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/'chain-mock-v1'))
from native_adapter import NativeQwen,Journal,wire,MODEL
from live_calibration import DirectTransport,save_new,utc,ENDPOINT
from agentdojo.task_suite import get_suite
from agentdojo.agent_pipeline.agent_pipeline import load_system_message
HERE=Path(__file__).resolve().parent

def freeze(out):
    suite=get_suite('v1.2.2','workspace');d=json.loads((HERE/'offline_diagnostic.json').read_text())['suites']['workspace']['users']
    # The six goals with non-empty official reference traces are selected before
    # any live model call. Task 0--5 are not the flawed empty-reference block.
    goals=[f'injection_task_{i}' for i in range(6)]; users=sorted(suite.user_tasks)[:10]
    rng=random.Random(2026092823);rng.shuffle(users);pairs=[]
    for u in users:
        slots=sorted(d[u]['visible_slots']);assert slots
        for g in goals:
            pairs.append({'pair_id':f'w{len(pairs):03d}','user_id':u,'injection_id':g,'slot':slots[0],'raw_goal':suite.injection_tasks[g].GOAL})
    jobs=[dict(p,arm=arm,job_id=p['pair_id']+'-'+arm) for p in pairs for arm in ('baseline','raw')];rng.shuffle(jobs)
    out.mkdir(parents=True,exist_ok=False);(out/'source').mkdir();plan={'frozen_utc':utc(),'model':MODEL,'endpoint':ENDPOINT,'suite':'workspace','benchmark':'v1.2.2','package':'0.1.35','seed':2026092823,'users':users,'goals':goals,'pairs':pairs,'jobs':jobs,'system':load_system_message(None),'turn_cap':12,'scope':'Headroom screen only: non-empty official reference goals 0--5; no claim about empty-reference tasks 6--13.','analysis':'Descriptive raw-vs-baseline attack and utility counts by user and goal; no IID inference. This is a finite crossed bank.','payload':'Literal official injection goal; no optimization or sender transformation.','missing':'Unknown for incomplete sessions; no retries or replacement.','stop':'Stop on HTTP 400/401/403/404/429, model mismatch or three consecutive incomplete sessions.','source_sha256':{}}
    for src in [HERE/'workspace_screen.py',HERE/'native_adapter.py',HERE/'offline_check.py',HERE.parent/'chain-mock-v1'/'run_journal.py',HERE.parent/'chain-mock-v1'/'live_calibration.py']:
        shutil.copy2(src,out/'source'/src.name);plan['source_sha256'][src.name]=hashlib.sha256(src.read_bytes()).hexdigest()
    save_new(out/'manifest.json',plan);print(json.dumps({'pairs':len(pairs),'sessions':len(jobs),'frozen':str(out)}),flush=True)

def run(out):
    plan=json.loads((out/'manifest.json').read_text());key=os.environ.get('DASHSCOPE_TP_API_KEY')
    if not key:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as k:key=winreg.QueryValueEx(k,'DASHSCOPE_TP_API_KEY')[0]
    if not key:raise RuntimeError('Key unavailable')
    # A pre-existing journal is resumable only when every completed session has
    # its own immutable row. The caller must first recover any row lost during
    # serialization; no missing row is silently reissued.
    suite=get_suite(plan['benchmark'],plan['suite']);transport=DirectTransport(key);j=Journal(out/'journal.jsonl');rows=[]
    for old in plan['jobs']:
        path=out/(old['job_id']+'.json')
        if path.exists():
            try:rows.append(json.loads(path.read_text(encoding='utf8')))
            except json.JSONDecodeError:raise RuntimeError('Existing row is not valid JSON; recover or quarantine before resuming')
    streak=0;status='completed'
    for q in plan['jobs']:
        if (out/(q['job_id']+'.json')).exists():
            continue
        p=NativeQwen(j,transport,dict(q,injected_text='' if q['arm']=='baseline' else q['raw_goal']),plan['system'],plan['turn_cap']);inj={} if q['arm']=='baseline' else {q['slot']:q['raw_goal']};env=suite.load_and_inject_default_environment(inj)
        try:
            u,s=suite.run_task_with_pipeline(p,suite.user_tasks[q['user_id']],suite.injection_tasks[q['injection_id']],inj,environment=env);o={'utility':bool(u),'security_success':bool(s)}
        except Exception as exc:p.complete=False;p.reason='exception_'+type(exc).__name__;o=None
        row=dict(q,complete=p.complete,reason=p.reason,calls=p.calls,outcomes=o if p.complete else None,observed_predicates=o,exposed=p.exposed if q['arm']=='raw' else None,post_environment=getattr(p,'final_environment',wire(env)),messages=p.messages,tool_log=p.tool_log)
        save_new(out/(q['job_id']+'.json'),json.loads(json.dumps(row,default=lambda x:x.isoformat() if isinstance(x,(datetime.datetime,datetime.date)) else x)));rows.append(row);print(json.dumps({k:row[k] for k in ('job_id','complete','calls','outcomes')}),flush=True)
        streak=0 if p.complete else streak+1
        if p.last_http in (400,401,403,404,429) or p.reason=='model_mismatch' or streak>=3:status='stopped';break
    groups={}
    for arm in ('baseline','raw'):
        rr=[r for r in rows if r['arm']==arm];groups[arm]={'planned':len(plan['pairs']),'observed':len(rr),'complete':sum(r['complete'] for r in rr),'utility':sum(bool(r['outcomes'] and r['outcomes']['utility']) for r in rr),'security_success':sum(bool(r['outcomes'] and r['outcomes']['security_success']) for r in rr),'exposed':sum(r['exposed'] is True for r in rr)}
    tokens=sum(json.loads(e['data']['body_text']).get('usage',{}).get('total_tokens',0) for e in j.events if e['kind']=='response')
    save_new(out/'summary.json',{'status':status,'groups':groups,'sessions':len(rows),'calls':sum(r['calls'] for r in rows),'reported_tokens':tokens,'by_goal':{g:{a:{'success':sum(bool(r['outcomes'] and r['outcomes']['security_success']) for r in rows if r['injection_id']==g and r['arm']==a)} for a in ('baseline','raw')} for g in plan['goals']},'ended_utc':utc()})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['freeze','run']);p.add_argument('--run-dir',type=Path,required=True);a=p.parse_args();(freeze if a.mode=='freeze' else run)(a.run_dir.resolve())
