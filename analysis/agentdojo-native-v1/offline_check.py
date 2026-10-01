"""Run official suite self-checks with network connections prohibited."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import socket
from datetime import datetime,timezone
from pathlib import Path

SUITES=('workspace','slack')
BENCHMARK='v1.2.2'

def blocked(*args,**kwargs):
    raise RuntimeError('Network connection prohibited during offline suite validation')

def main(output):
    socket.create_connection=blocked
    socket.socket.connect=blocked
    socket.socket.connect_ex=blocked
    from agentdojo.task_suite import get_suite
    report={'checked_utc':datetime.now(timezone.utc).isoformat(),'package_version':importlib.metadata.version('agentdojo'),
            'benchmark_version':BENCHMARK,'suites_selected_before_live_calls':list(SUITES),
            'python':platform.python_version(),'network_connections':'prohibited by socket hooks',
            'evidence':'OFFLINE_OFFICIAL_GROUND_TRUTH_NOT_MODEL_PERFORMANCE','model_calls':0,'suites':{},
            'dependencies':dict(sorted((d.metadata['Name'],d.version) for d in importlib.metadata.distributions()))}
    wheel=Path(__file__).parent/'vendor/agentdojo-0.1.35-py3-none-any.whl'
    report['wheel_sha256']=hashlib.sha256(wheel.read_bytes()).hexdigest()
    for name in SUITES:
        print('Checking '+name,flush=True)
        result={}
        try:
            suite=get_suite(BENCHMARK,name)
            result={'user_tasks':len(suite.user_tasks),'injection_tasks':len(suite.injection_tasks),
                    'injection_vectors':len(suite.get_injection_vector_defaults()),
                    'tools':[t.name for t in suite.tools]}
            ok,(user,injection)=suite.check(check_injectable=True)
            result.update(all_passed=bool(ok),user_checks=user,injection_checks=injection)
        except Exception as exc:
            result.update(all_passed=False,error_type=type(exc).__name__,error=str(exc))
        report['suites'][name]=result
    report['all_passed']=all(r['all_passed'] for r in report['suites'].values())
    with Path(output).open('x',encoding='utf8') as stream:json.dump(report,stream,ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='dependencies'},indent=2))
    if not report['all_passed']:raise SystemExit(1)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();main(a.output)
