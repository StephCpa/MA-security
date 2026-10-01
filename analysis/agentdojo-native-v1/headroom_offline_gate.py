"""Offline gate for the important_instructions headroom screen (no model calls).

Sidecar only. It does not patch installed AgentDojo or its predicates, and it
does not modify offline_check.py or the other scripts whose hashes are pinned
in earlier frozen run manifests.

For each requested suite it records the official reference utility and
security checks, the injection candidates that the official attack class
finds for every user task, and the official attack text for every
user/injection pair together with its SHA-256.
"""
import argparse
import ast
import hashlib
import inspect
import textwrap
import importlib.metadata
import json
import socket
from pathlib import Path
from offline_check import blocked,BENCHMARK

ATTACK='important_instructions_no_model_name'
# The registered important_instructions attacks resolve a prose model name in
# their parent constructor and raise for models absent from
# agentdojo.models.MODEL_NAMES; qwen3.6-flash and deepseek-flash are absent.
# The no-model-name variant then overwrites that name with DEFAULT_MODEL_NAME,
# so any listed key yields identical text. The placeholder is never called.
PLACEHOLDER_PIPELINE_NAME='gpt-4o-2024-05-13'

class _NamedPipeline:
    def __init__(self,name):self.name=name

def sha(text):return hashlib.sha256(text.encode('utf8')).hexdigest()

def predicate_inputs(task):
    """Which inputs the active security predicate reads (static inspection)."""
    method='security_from_traces' if 'security_from_traces' in type(task).__dict__ else 'security'
    tree=ast.parse(textwrap.dedent(inspect.getsource(getattr(type(task),method))))
    names={n.id for stmt in tree.body[0].body for n in ast.walk(stmt) if isinstance(n,ast.Name)}
    return {'method':method,'defined_in':type(task).__module__,
            'reads_post_environment':'post_environment' in names,
            'reads_model_output':'model_output' in names,'reads_traces':'traces' in names}

def main(suites,output):
    socket.create_connection=blocked;socket.socket.connect=blocked;socket.socket.connect_ex=blocked
    from agentdojo.task_suite import get_suite
    from agentdojo.attacks.attack_registry import load_attack
    report={'benchmark_version':BENCHMARK,'package_version':importlib.metadata.version('agentdojo'),
            'attack':ATTACK,'placeholder_pipeline_name':PLACEHOLDER_PIPELINE_NAME,
            'model_calls':0,'upstream_modified':False,'network_connections':'prohibited by socket hooks',
            'evidence':'OFFLINE_OFFICIAL_GROUND_TRUTH_NOT_MODEL_PERFORMANCE','suites':{}}
    for name in suites:
        suite=get_suite(BENCHMARK,name)
        attack=load_attack(ATTACK,suite,_NamedPipeline(PLACEHOLDER_PIPELINE_NAME))
        _,(utility,security)=suite.check(check_injectable=False)
        env=suite.load_and_inject_default_environment({})
        users={}
        for uid,task in sorted(suite.user_tasks.items()):
            try:candidates=sorted(attack.get_injection_candidates(task));error=None
            except ValueError as exc:candidates=[];error=str(exc)
            users[uid]={'official_reference_utility_pass':bool(utility[uid][0]),
                        'injection_candidates':candidates,'not_injectable':error}
        injections={iid:{'reference_call_count':len(task.ground_truth(env.model_copy(deep=True))),
                         'official_reference_security_success':bool(security[iid]),
                         'predicate':predicate_inputs(task)}
                    for iid,task in sorted(suite.injection_tasks.items())}
        for r in injections.values():
            p=r['predicate'];r['output_only']=p['reads_model_output'] and not (p['reads_post_environment'] or p['reads_traces'])
        pairs=[]
        for uid,task in sorted(suite.user_tasks.items()):
            if not users[uid]['injection_candidates']:continue
            for iid,inj in sorted(suite.injection_tasks.items()):
                rendered=attack.attack(task,inj)
                texts=set(rendered.values())
                assert len(texts)==1,(uid,iid)
                text=texts.pop()
                pairs.append({'user_id':uid,'injection_id':iid,'slots':sorted(rendered),
                              'attack_text':text,'attack_sha256':sha(text)})
        eligible=[u for u,r in users.items() if r['official_reference_utility_pass'] and r['injection_candidates']]
        report['suites'][name]={'users':users,'injections':injections,'pairs':pairs,
            'summary':{'user_tasks':len(users),'official_reference_utility_pass':sum(r['official_reference_utility_pass'] for r in users.values()),
                       'injectable_user_tasks':sum(bool(r['injection_candidates']) for r in users.values()),
                       'eligible_user_tasks':len(eligible),
                       'mean_injection_candidates':round(sum(len(r['injection_candidates']) for r in users.values())/len(users),3),
                       'injection_tasks':len(injections),
                       'reference_security_success':sum(r['official_reference_security_success'] for r in injections.values()),
                       'empty_reference_actions':sum(r['reference_call_count']==0 for r in injections.values()),
                       'output_only_predicates':sorted(i for i,r in injections.items() if r['output_only']),
                       'pairs':len(pairs)}}
    with Path(output).open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({n:r['summary'] for n,r in report['suites'].items()},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--suites',nargs='+',default=['slack','banking','travel'])
    p.add_argument('--output',required=True)
    a=p.parse_args();main(a.suites,a.output)
