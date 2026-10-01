"""Outcome-blind selection from the F6 request manifest; three further draws."""
import argparse
import copy
import hashlib
import json
import os
import random
from pathlib import Path
from capability_signal import run
from live_calibration import DirectTransport, utc

SEED=2026092816

def build_panel(original):
    original=Path(original)
    source=original/'manifest.json'
    base=json.loads(source.read_text(encoding='utf8'))
    # Deliberately do not open original outcomes, responses, or scored reports.
    families={}
    for c in base['cases']:
        if c['kind']=='attack':families.setdefault(c['family'],set()).add(c['stimulus_id'])
    assert len(families)==6 and all(len(v)==8 for v in families.values())
    rng=random.Random(SEED);order=sorted(families);rng.shuffle(order)
    selected=[];allocation={}
    for i,family in enumerate(order):
        count=3 if i<4 else 2
        allocation[family]=count
        selected.extend(rng.sample(sorted(families[family]),count))
    selected=sorted(selected)
    originals=[c for c in base['cases'] if c['stimulus_id'] in selected]
    assert len(originals)==64
    cases=[]
    for repeat in (1,2,3):
        block=[dict(copy.deepcopy(c),repeat_id=repeat) for c in originals]
        rng.shuffle(block);cases.extend(block)
    plan=copy.deepcopy(base)
    plan.update(frozen_utc=utc(),cases=cases,maximum_calls=192,seed=SEED,
        original_run=str(original.resolve()),original_manifest_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        selected_ids=selected,family_allocation=allocation,
        selection='Random family order, 3 IDs in first four families and 2 in last two; sorted IDs sampled using seed 2026092816. Selection reads manifest only. Original aggregate results were already known. Not a blinded analyst or fresh confirmation bank.',
        primary='Descriptive repeatability panel: per-round exact-request counts and paired cue RDs; per-source-cell four-draw endpoint strings and fraction with both 0 and 1. No new null-hypothesis tests.',
        supporting='Report each of four draws (original repeat 0 plus new 1/2/3), not 64 independent sources. Summarize source-cell response flips and per-draw RD range; these are not confidence intervals. Also report any protected-resource request separately.',
        missing='Unknown remains unknown in the four-draw strings. Complete-cell instability uses complete cells only, with both complete and unknown cell counts. No replacement or retry.',
        scope='Sixteen fixed sources, four conditions and three additional short-window draws. Reuses original request bytes and parameters. No fresh payloads, controls, sender or external tool execution. Does not estimate multi-day drift.',
        stop='401/403/429, model mismatch, three consecutive non-200 responses, 192 calls. No retries or external writes.')
    plan.pop('source_sha256',None)
    return plan

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--original',required=True);p.add_argument('--run-dir',required=True);p.add_argument('--freeze-only',action='store_true');a=p.parse_args()
    plan=build_panel(a.original)
    if a.freeze_only:
        print(json.dumps({k:plan[k] for k in ('selected_ids','family_allocation','maximum_calls','primary')},indent=2))
    else:
        key=os.environ.get('DASHSCOPE_TP_API_KEY')
        if not key:raise SystemExit('DASHSCOPE_TP_API_KEY unavailable')
        run(a.run_dir,DirectTransport(key),plan=plan,extra_sources=(Path(__file__),))
