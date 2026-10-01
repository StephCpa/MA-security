"""Sidecar diagnosis only: do not patch installed AgentDojo or its predicates."""
import argparse
import json
import socket
from pathlib import Path
from offline_check import blocked,SUITES,BENCHMARK

def main(output):
    socket.create_connection=blocked;socket.socket.connect=blocked;socket.socket.connect_ex=blocked
    from agentdojo.task_suite import get_suite
    from agentdojo.agent_pipeline.ground_truth_pipeline import GroundTruthPipeline
    from agentdojo.functions_runtime import FunctionsRuntime
    from agentdojo.types import get_text_content_as_str
    from agentdojo.task_suite.task_suite import is_task_injectable
    report={'benchmark_version':BENCHMARK,'model_calls':0,'upstream_modified':False,'suites':{}}
    for name in SUITES:
        suite=get_suite(BENCHMARK,name)
        defaults=suite.get_injection_vector_defaults()
        markers={k:f'---CANARY_{k}---' for k in defaults}
        env=suite.load_and_inject_default_environment(markers)
        _,(utility,security)=suite.check(check_injectable=False)
        users={}
        for taskid,task in suite.user_tasks.items():
            _,_,_,messages,_=GroundTruthPipeline(task).query(task.PROMPT,FunctionsRuntime(suite.tools),env.model_copy(deep=True))
            texts=[get_text_content_as_str(m['content']) for m in messages if m['role']=='tool']
            visible=[k for k,v in markers.items() if any(v in t for t in texts)]
            users[taskid]={'native_injectability':is_task_injectable(messages,list(markers.values())),
                'normalized_text_canary_visible':bool(visible),'visible_slots':visible,'tool_content_types':sorted({type(m['content']).__name__ for m in messages if m['role']=='tool'}),
                'official_reference_utility_pass':utility[taskid][0]}
        injections={taskid:{'reference_call_count':len(task.ground_truth(env.model_copy(deep=True))),
                            'official_reference_security_success':security[taskid]} for taskid,task in suite.injection_tasks.items()}
        report['suites'][name]={'users':users,'injections':injections,
            'summary':{'user_tasks':len(users),'official_reference_utility_pass':sum(r['official_reference_utility_pass'] for r in users.values()),
                       'native_canary_visible':sum(r['native_injectability'] for r in users.values()),
                       'normalized_canary_visible':sum(r['normalized_text_canary_visible'] for r in users.values()),
                       'injection_tasks':len(injections),'reference_security_success':sum(r['official_reference_security_success'] for r in injections.values()),
                       'empty_reference_actions':sum(r['reference_call_count']==0 for r in injections.values())}}
    with Path(output).open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({n:r['summary'] for n,r in report['suites'].items()},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();main(a.output)
