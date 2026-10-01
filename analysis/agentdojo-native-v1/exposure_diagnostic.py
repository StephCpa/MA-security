"""Post-run whitespace diagnostic; preserves original exact exposure flags."""
import argparse
import json
from pathlib import Path
from native_adapter import contains
from live_calibration import save_new

def normalize(value):
    if isinstance(value,str):return ' '.join(value.split())
    if isinstance(value,list):return [normalize(v) for v in value]
    if isinstance(value,dict):return {k:normalize(v) for k,v in value.items()}
    return value

def main(folder,output):
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf8'));rows=[]
    for job in manifest['jobs']:
        if job['arm']=='baseline':continue
        row=json.loads((folder/(job['job_id']+'.json')).read_text(encoding='utf8'))
        logs=[x for x in row['tool_log'] if not x['error']]
        rows.append({'job_id':job['job_id'],'arm':job['arm'],'slot':job['slot'],
                     'original_exact':row['exposed'],
                     'whitespace_normalized_full_payload':any(contains(normalize(x['result']),normalize(job['injected_text'])) for x in logs),
                     'literal_marker':any(contains(x['result'],'UNTRUSTED EMBEDDED CONTENT:') for x in logs),
                     'raw_goal':any(contains(normalize(x['result']),normalize(job['raw_goal'])) for x in logs)})
    report={'post_hoc':True,'purpose':'Diagnose whitespace folding, not redefine security outcomes or rerun original gates.',
            'groups':{arm:{key:sum(r[key] for r in rows if r['arm']==arm) for key in ('original_exact','whitespace_normalized_full_payload','literal_marker','raw_goal')} for arm in ('raw','marked')},'rows':rows}
    save_new(output,report);print(json.dumps(report['groups'],indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.run_dir,a.output)
