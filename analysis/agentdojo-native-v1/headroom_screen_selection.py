"""Outcome-blind selection for the important_instructions headroom screen.

Reads the offline gate output, verifies every recorded attack hash, and draws
the screen sample and the disjoint stage-2 banks with a declared seed. No
model calls and no AgentDojo import: the gate output is the only input.
"""
import argparse
import hashlib
import json
import random
from pathlib import Path

SEED=2026100101
SUITES=('slack','banking','travel')
SCREEN_USERS=10

def select(gate):
    rng=random.Random(SEED);out={'seed':SEED,'gate_sha256':None,'suites':{}}
    for name in SUITES:
        suite=gate['suites'][name]
        for p in suite['pairs']:
            assert hashlib.sha256(p['attack_text'].encode('utf8')).hexdigest()==p['attack_sha256']
        goals=sorted(i for i,r in suite['injections'].items()
                     if not r['output_only'] and r['official_reference_security_success'])
        users=sorted(u for u,r in suite['users'].items()
                     if r['official_reference_utility_pass'] and r['injection_candidates'])
        order=users[:];rng.shuffle(order);screen_users=sorted(order[:SCREEN_USERS])
        goal_cycle=goals[:];rng.shuffle(goal_cycle)
        screen=[{'user_id':u,'injection_id':goal_cycle[k%len(goal_cycle)]} for k,u in enumerate(screen_users)]
        rest=sorted(set(users)-set(screen_users))
        out['suites'][name]={'eligible_goals':goals,
            'excluded_goals':sorted(set(suite['injections'])-set(goals)),
            'screen_pairs':screen,'stage2_users':rest,
            'stage2_pairs':len(rest)*len(goals)}
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--gate',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    raw=a.gate.read_bytes();result=select(json.loads(raw))
    result['gate_sha256']=hashlib.sha256(raw).hexdigest()
    with a.output.open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
