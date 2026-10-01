"""Three-call DeepSeek connectivity/model-identity gate; no AgentDojo task."""
import argparse,json,os,urllib.request,urllib.error,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/'chain-mock-v1'))
from datetime import datetime,timezone
from live_calibration import save_new

ENDPOINT='https://api.deepseek.com/chat/completions';MODEL='deepseek-flash'
def key():
 v=os.environ.get('DEEPSEEK_API_KEY')
 if not v:
  import winreg
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as k:v=winreg.QueryValueEx(k,'DEEPSEEK_API_KEY')[0]
 if not v:raise RuntimeError('DEEPSEEK_API_KEY unavailable')
 return v
def main(out):
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}));rows=[]
 for i in range(3):
  req=urllib.request.Request(ENDPOINT,data=json.dumps({'model':MODEL,'messages':[{'role':'user','content':'Reply with exactly READY.'}],'temperature':0,'max_tokens':8,'stream':False,'thinking':{'type':'disabled'}}).encode(),method='POST',headers={'Authorization':'Bearer '+key(),'Content-Type':'application/json'})
  try:
   with opener.open(req,timeout=45) as r:
    body=r.read().decode();parsed=json.loads(body);rows.append({'probe':i,'status':r.status,'reported_model':parsed.get('model'),'finish_reason':(parsed.get('choices') or [{}])[0].get('finish_reason'),'text':((parsed.get('choices') or [{}])[0].get('message') or {}).get('content')})
  except urllib.error.HTTPError as e:rows.append({'probe':i,'status':e.code,'error':'HTTPError','body_prefix':e.read().decode(errors='replace')[:180]})
  except Exception as e:rows.append({'probe':i,'status':None,'error':type(e).__name__})
 report={'utc':datetime.now(timezone.utc).isoformat(),'endpoint':ENDPOINT,'requested_model':MODEL,'probes':rows,
         'pass':len(rows)==3 and all(x.get('status')==200 and x.get('reported_model')==MODEL for x in rows),
         'scope':'Connectivity and model-identity gate only; no benchmark task or AgentDojo result.'}
 save_new(out,report);print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.output)
