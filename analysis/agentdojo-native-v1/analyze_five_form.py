"""Finite-bank descriptive analysis; crossed tasks are not IID samples."""
import argparse
import json
from pathlib import Path
from five_form import FORMS
from exposure_diagnostic import normalize
from native_adapter import contains
from live_calibration import save_new

def endpoint(row,key):
    return row['outcomes'][key] if row and row.get('complete') and row.get('outcomes') is not None else None

def contrast(a,b):
    assert len(a)==len(b) and a
    table={'both_success':0,'a_only':0,'b_only':0,'both_failure':0,'unknown_pair':0}
    low=high=0
    for x,y in zip(a,b):
        low+=(int(x) if x is not None else 0)-(int(y) if y is not None else 1)
        high+=(int(x) if x is not None else 1)-(int(y) if y is not None else 0)
        if x is None or y is None:table['unknown_pair']+=1
        else:table[{(True,True):'both_success',(True,False):'a_only',(False,True):'b_only',(False,False):'both_failure'}[(x,y)]]+=1
    return {'direction':'a minus b','planned_pairs':len(a),'paired_table':table,
            'risk_difference':low/len(a) if not table['unknown_pair'] else None,
            'missingness_bounds':[low/len(a),high/len(a)],'bounds_are_confidence_interval':False}

def analyze(folder,output):
    plan=json.loads((folder/'manifest.json').read_text(encoding='utf8'))
    end=json.loads((folder/'receiver_end.json').read_text(encoding='utf8'))
    bank=json.loads((folder/'generation_bank.json').read_text(encoding='utf8'))
    derived={(r['pair_id'],r['form']):r['content'] for r in bank['rows']}
    rows={}
    for p in plan['pairs']:
        for arm in FORMS+('baseline',):
            path=folder/(p['pair_id']+'-'+arm+'-receiver.json')
            if path.exists():rows[(p['pair_id'],arm)]=json.loads(path.read_text(encoding='utf8'))
    metrics={}
    for form in FORMS:
        vals={key:[endpoint(rows.get((p['pair_id'],form)),key) for p in plan['pairs']] for key in ('security_success','utility')}
        metrics[form]={key:{'known_successes':sum(v is True for v in vv),'unknown':sum(v is None for v in vv),'planned':len(vv),
                          'missingness_bounds':[sum(v is True for v in vv)/len(vv),sum(v is not False for v in vv)/len(vv)]} for key,vv in vals.items()}
        exposure=[]
        for p in plan['pairs']:
            row=rows.get((p['pair_id'],form));payload=p['forms'].get(form,derived.get((p['pair_id'],form)))
            if row is None or payload is None:exposure.append(None);continue
            exposure.append(any(not t['error'] and contains(normalize(t['result']),normalize(payload)) for t in row.get('tool_log',[])))
        metrics[form]['exposure']={'normalized_full_payload':sum(v is True for v in exposure),'unknown':sum(v is None for v in exposure)}
    comparisons={}
    for a,b in [('C','P'),('S_C','S_P'),('R','C')]:
        groups={'all':plan['pairs']}
        groups.update({'user:'+u:[p for p in plan['pairs'] if p['user_id']==u] for u in plan['users']})
        groups.update({'goal:'+g:[p for p in plan['pairs'] if p['injection_id']==g] for g in sorted({p['injection_id'] for p in plan['pairs']})})
        comparisons[a+'-'+b]={group:{key:contrast([endpoint(rows.get((p['pair_id'],a)),key) for p in pairs],
                                                 [endpoint(rows.get((p['pair_id'],b)),key) for p in pairs]) for key in ('security_success','utility')} for group,pairs in groups.items()}
    usage={}
    for stage in ('generation','receiver'):
        events=[json.loads(line) for line in (folder/(stage+'_journal.jsonl')).read_text(encoding='utf8').splitlines()]
        tokens=0
        for e in events:
            if e['kind']=='response':
                try:tokens+=json.loads(e['data']['body_text']).get('usage',{}).get('total_tokens',0)
                except (ValueError,AttributeError):pass
        usage[stage]={'calls':sum(e['kind']=='request' for e in events),'reported_tokens':tokens}
    controls=[r for (p,a),r in rows.items() if a=='baseline']
    report={'status':end['status'],'scope':plan['scope'],'analysis':plan['analysis'],'metrics':metrics,'comparisons':comparisons,'usage':usage,
            'baseline':{'planned':len(plan['users']),'observed':len(controls),'utility_success':sum(endpoint(r,'utility') is True for r in controls),
                        'unknown_utility':len(plan['users'])-sum(endpoint(r,'utility') is not None for r in controls)},
            'generation':{'planned':110,'valid':sum(r['content'] is not None for r in bank['rows']),
                          'unique_texts':len({r['content'] for r in bank['rows'] if r['content'] is not None})}}
    save_new(output,report)
    print(json.dumps({k:report[k] for k in ('status','metrics','usage','baseline','generation')},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();analyze(a.run_dir,a.output)
