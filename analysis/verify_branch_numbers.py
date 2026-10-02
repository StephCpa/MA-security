"""Recompute every number the candidate revision adds or changes, from repo files only.

Each check names the manuscript location, the source file, the value derived from
that file, and the value the manuscript states. Values that no file in this
repository can support are listed separately and are never reported as passing.
Run from the repository root:  python analysis/verify_branch_numbers.py
"""
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'results'
CHECKS=[];UNVERIFIABLE=[]

def load(rel):return json.loads((ROOT/rel).read_text(encoding='utf8'))

def check(where,source,derived,stated,tol=1e-4):
    ok=(abs(derived-stated)<=tol) if isinstance(stated,float) else derived==stated
    CHECKS.append((ok,where,source,derived,stated))

def unverifiable(where,claim,reason):UNVERIFIABLE.append((where,claim,reason))

def agentdojo():
    for model,run,succ,unk,uniq,util,audit in [
        ('Qwen 3.6','qwen36-agentdojo-five-form-001',[7,3,3,2,2],[5,4,3,2,2],14,(37,37,4,3),4350),
        ('DeepSeek','deepseek-agentdojo-five-form-001',[3,3,2,2,2],[0,0,0,0,0],17,(40,39,0,0),3861)]:
        src=f'results/{run}/analysis.json';a=load(src)
        m=a['metrics'];forms=['R','C','P','S_C','S_P']
        check(f'§6.3 {model} security successes',src,[m[f]['security_success']['known_successes'] for f in forms],succ)
        check(f'§6.3 {model} unknown outcomes',src,[m[f]['security_success']['unknown'] for f in forms],unk)
        check(f'§6.3 {model} normalized exposure',src,[m[f]['exposure']['normalized_full_payload'] for f in forms],[55]*5)
        check(f'§6.3 {model} distinct sender texts',src,a['generation']['unique_texts'],uniq)
        check(f'§6.3 {model} C/P utility and unknowns',src,
              (m['C']['utility']['known_successes'],m['P']['utility']['known_successes'],m['C']['utility']['unknown'],m['P']['utility']['unknown']),util)
        check(f'§6.3 {model} replay checks',f'results/{run}/audit_report.json',load(f'results/{run}/audit_report.json')['checks_passed'],audit)
    a=load('results/qwen36-agentdojo-five-form-001/analysis.json')['comparisons']
    for key,stated in [('C-P',[-.0545,.0727]),('S_C-S_P',[-.0364,.0364]),('R-C',[0.0,.1636])]:
        b=a[key]['all']['security_success']['missingness_bounds']
        check(f'§6.3 Qwen {key} missingness bounds','results/qwen36-agentdojo-five-form-001/analysis.json',[round(x,4) for x in b],stated)
    authored=40/48-1/48
    check('§6.3 headroom share of authored effect','derived: 3/55 over (40-1)/48',round((3/55)/authored,3),.067)
    check('§6.3 worst-case share (all 4 unknown Qwen C successes)','derived: 7/55 over (40-1)/48',round((7/55)/authored,3),.157)

def five_form():
    for model,run,stated in [('DeepSeek','deepseek-five-form-provenance-confirmation-001',[37,40,1,44,22]),
                             ('Qwen 3.7','qwen-five-form-provenance-confirmation-001',[46,46,8,45,25])]:
        src=f'results/{run}/report.json';c=load(src)['analysis']['contrasts'];rate={}
        for v in c.values():rate[v['left_form']]=v['left_rate'];rate[v['right_form']]=v['right_rate']
        check(f'Table 2 / Fig. 2a {model} attempts',src,[round(rate[f]*48) for f in ['R','C','P','S_C','S_P']],stated)

def ratings():
    src='results/deepseek-five-form-provenance-confirmation-001/rating-returned/five_form_confirmation_rating_result.json'
    s=load(src)['summary']
    for rater,stated in [('A',[17,15,1,15]),('B',[19,13,1,15])]:
        d=s['paired_SC_minus_SP'][rater]['actionable_semantic_retention']['difference_support']
        check(f'Fig. 2b rater {rater} retention differences 0..3',src,[d.get(str(k),0) for k in range(4)],stated)
        check(f'§3.1 rater {rater} zero-rated S_P texts',src,s['form'][rater]['S_P']['actionable_semantic_retention']['distribution_0_to_3'][0],17)
        check(f'§3.1 rater {rater} +3 mode (S_C=3, S_P=0)',src,d.get('3',0),15)

def responses():
    src='results/qwen-e12-capability-hidden-001/report.json';m=load(src)['analysis']['metrics']
    v0=m['0']['exact_direct']['visible_deny']['count'];v1=m['1']['exact_direct']['visible_deny']['count']
    check('§5.1 E12 tool-visible exact requests a=0, a=1',src,(v0,v1),(42,45))
    check('§5.1 E12 tool-visible response',src,round((v1-v0)/48,4),.0625)
    resp={}
    for model,run in [('DeepSeek','deepseek-lifecycle-covariance-confirmation-001'),('Qwen','qwen-lifecycle-covariance-confirmation-001')]:
        a=load(f'results/{run}/report.json')['analysis']
        resp[model]=a['primary_shared_minus_independent_mutation_risk']/0.0475
        check(f'§5.1 {model} semantic-placement response',f'results/{run}/report.json (shared excess / .0475)',round(resp[model],4),{'DeepSeek':.875,'Qwen':.3958}[model])
    check('§5.1 / intro within-Qwen spread (.396/.0625)','derived',round(resp['Qwen']/.0625,1),6.3)
    check('§5.1 / intro cross-endpoint contrast (.875/.396)','derived',round(resp['DeepSeek']/resp['Qwen'],1),2.2)
    for name,slope in [('.875',.875),('.396',19/48),('.313',.3125),('.167',8/48),('.063',.0625)]:
        for cov,label in [(.023141,'common root'),(.0475,'shared state')]:
            check(f'Fig. 4 point {name} at {label}','derived: Cov x response',round(cov*slope*100,4),
                  {('.875',.023141):2.0248,('.875',.0475):4.1563,('.396',.023141):0.9160,('.396',.0475):1.8802,
                   ('.313',.023141):0.7232,('.313',.0475):1.4844,('.167',.023141):0.3857,('.167',.0475):0.7917,
                   ('.063',.023141):0.1446,('.063',.0475):0.2969}[(name,cov)],tol=1e-3)
    unverifiable('§5.1 / Fig. 4 .313 (E3, 33/48 to 48/48)','carried unchanged from the baseline manuscript','no E3 result directory in this repository')
    unverifiable('§5.1 / Fig. 4 .167 (E5, 22/48 to 30/48)','carried unchanged from the baseline manuscript','no E5 result directory in this repository')
    unverifiable('§5.1 DeepSeek frozen-relay range .125 to .771','computed from Table 6 of the baseline manuscript','no E4 result directory in this repository')

def propagation_and_lineage():
    src='results/deepseek-retention-propagation-confirmation-001/report.json';r=load(src)
    check('Fig. 3 receiver 1 and 2 delegations',src,(r['receiver_1']['retransmissions'],r['receiver_1']['opportunities'],
          r['receiver_2_conditional']['retransmissions'],r['receiver_2_conditional']['opportunities']),(40,121,17,40))
    src='results/e10-a2a-two-hop-enforcement-001/summary.json';s=load(src)['by_strategy']
    check('Intro: least-trusted join correct on both two-hop cases',src,
          (s['joined_fail_closed']['correct_policy_outcomes'],s['joined_fail_closed']['attempts']),(2,2))
    check('Intro: fail-open and fail-closed each err once',src,
          (s['vanilla_fail_open']['correct_policy_outcomes'],s['vanilla_fail_closed']['correct_policy_outcomes']),(1,1))

def workspace():
    src='analysis/agentdojo-native-v1/workspace_controls_v3.json';t=load(src)['tasks']
    for task in ['injection_task_11','injection_task_12']:
        check(f'§6.3 Workspace {task}: one target + four non-targets scores True',src,
              t[task]['variants']['partly_wrong_files']['score'],True)

def main():
    for f in (agentdojo,five_form,ratings,responses,propagation_and_lineage,workspace):f()
    failed=0
    for ok,where,src,derived,stated in CHECKS:
        failed+=not ok
        print(f"{'PASS' if ok else 'FAIL'}  {where}\n      source: {src}\n      derived {derived}  stated {stated}")
    print(f'\n{len(CHECKS)-failed}/{len(CHECKS)} checks pass.\n\nNot verifiable from this repository:')
    for where,claim,reason in UNVERIFIABLE:print(f'  - {where}: {claim} ({reason})')
    return 1 if failed else 0

if __name__=='__main__':sys.exit(main())
