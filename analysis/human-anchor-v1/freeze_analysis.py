"""Record the tested pre-return version; never overwrites an existing freeze."""
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
import numpy
import openpyxl

HERE=Path(__file__).resolve().parent
FILES=['analyze_returns.py','test_returns.py','ANALYSIS_PLAN.md','coordinator_only/key.json',
       '../../../.artifact-work/five-form-confirmation-ratings-20260828/confirmation_scored_inspection.json']
record={'created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'internal_pre_return_freeze_not_external_registration',
        'human_returns_received':0,
        'prior_knowledge':'historical model scores and receiver outcomes known to analyst',
        'software':{'python':platform.python_version(),'numpy':numpy.__version__,'openpyxl':openpyxl.__version__},
        'file_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in FILES}}
with (HERE/'coordinator_only/analysis_freeze.json').open('x',encoding='utf8') as stream:
    json.dump(record,stream,indent=2)
    stream.write('\n')
print(json.dumps({'status':record['status'],'files_frozen':len(FILES),'human_returns_received':0}))
