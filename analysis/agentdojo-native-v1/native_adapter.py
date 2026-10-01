"""Qwen transport adapter; only registered native simulated tools may execute."""
import json
import socket
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent.parent/'chain-mock-v1'))
from run_journal import Journal
from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
from agentdojo.agent_pipeline.tool_execution import tool_result_to_str
from agentdojo.functions_runtime import FunctionCall
from agentdojo.types import text_content_block_from_string
from offline_check import blocked

MODEL='qwen3.6-flash'

def wire(value):
    if hasattr(value,'model_dump'):return wire(value.model_dump())
    if isinstance(value,dict):return {k:wire(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [wire(v) for v in value]
    return value

def contains(value,text):
    value=wire(value)
    if isinstance(value,str):return bool(text) and text in value
    if isinstance(value,dict):return any(contains(v,text) for v in value.values())
    if isinstance(value,list):return any(contains(v,text) for v in value)
    return False

def strict_args(text):
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise ValueError('duplicate argument')
            d[k]=v
        return d
    def bad(x):raise ValueError('non-JSON constant')
    args=json.loads(text,object_pairs_hook=unique,parse_constant=bad)
    if not isinstance(args,dict):raise ValueError('arguments must be object')
    return args

class NativeQwen(BasePipelineElement):
    def __init__(self,journal,transport,job,system,turn_cap=12,model=MODEL):
        self.journal=journal;self.transport=transport;self.job=job;self.system=system;self.turn_cap=turn_cap;self.model=model
        self.complete=False;self.reason='not_started';self.calls=0;self.exposed=False;self.tool_log=[];self.messages=[];self.last_http=None

    def query(self,query,runtime,env,messages=(),extra_args=None):
        if self.calls:raise RuntimeError('No automatic pipeline retry permitted')
        self.initial_environment=wire(env)
        api=[{'role':'system','content':self.system},{'role':'user','content':query}]
        native=[{'role':r['role'],'content':[text_content_block_from_string(r['content'])]} for r in api]
        tools=[{'type':'function','function':{'name':f.name,'description':f.description,'parameters':f.parameters.model_json_schema()}} for f in runtime.functions.values()]
        for turn in range(self.turn_cap):
            request={'model':self.model,'messages':api,'tools':tools,'tool_choice':'auto','temperature':0,'enable_thinking':False,'max_tokens':1024,'stream':False}
            ident={'directive_id':self.job['pair_id'],'arm':self.job['arm'],'attack_variant':'native_goal_fixed_slot','repeat_id':0,'branch_id':str(turn)}
            record=self.journal.invoke(self.job['job_id']+f'::t{turn}','native_agent',request,self.transport,identity=ident)
            self.calls+=1;self.last_http=record['HttpStatus']
            body=record.get('Response')
            if self.last_http!=200 or not isinstance(body,dict):self.reason='transport_or_body';break
            if body.get('model')!=self.model:self.reason='model_mismatch';break
            try:
                if len(body['choices'])!=1:raise ValueError('choices')
                choice=body['choices'][0];msg=choice['message'];finish=choice['finish_reason']
                if msg['role']!='assistant':raise ValueError('role')
                calls=msg.get('tool_calls') or []
                content=msg.get('content') or ''
                if not isinstance(content,str):raise ValueError('content')
                if not calls:
                    if finish!='stop' or not content.strip():self.reason='incomplete_or_empty';break
                    native.append({'role':'assistant','content':[text_content_block_from_string(content)],'tool_calls':None})
                    self.complete=True;self.reason='completed';break
                if finish!='tool_calls':self.reason='incomplete_tools';break
                parsed=[];seen=set()
                for c in calls:
                    if c.get('type')!='function' or not c.get('id') or c['id'] in seen:raise ValueError('tool identity')
                    seen.add(c['id']);fn=c['function'];args=strict_args(fn['arguments'])
                    parsed.append(FunctionCall(function=fn['name'],args=args,id=c['id']))
            except (KeyError,ValueError,TypeError):self.reason='malformed_response';break
            api.append({'role':'assistant','content':content,'tool_calls':[{'id':c.id,'type':'function','function':{'name':c.function,'arguments':json.dumps(c.args)}} for c in parsed]})
            native.append({'role':'assistant','content':[text_content_block_from_string(content)],'tool_calls':parsed})
            for c in parsed:
                # Unknown tool names are never dispatched. Tools touch only native
                # environment objects; socket use is additionally prohibited here.
                with patch.object(socket,'create_connection',blocked),patch.object(socket.socket,'connect',blocked),patch.object(socket.socket,'connect_ex',blocked):
                    if c.function not in runtime.functions:result,error='', 'ToolNotFoundError: unregistered tool'
                    else:result,error=runtime.run_function(env,c.function,c.args)
                text=error or tool_result_to_str(result)
                exposed=contains(result,self.job.get('injected_text','')) if not error else False
                self.exposed=self.exposed or exposed
                self.tool_log.append({'turn':turn,'call':wire(c),'error':error,'result':wire(result),'serialized_text':text,'injected_payload_in_raw_result':exposed})
                api.append({'role':'tool','tool_call_id':c.id,'name':c.function,'content':text})
                native.append({'role':'tool','tool_call':c,'tool_call_id':c.id,'content':[text_content_block_from_string(text)],'error':error})
        else:self.reason='turn_cap'
        if not self.complete:
            # Empty administrative terminal prevents upstream's three-run retry.
            # It is not presented as model prose; outer outcomes remain unknown.
            native.append({'role':'assistant','content':[],'tool_calls':None})
        self.messages=wire(native)
        self.final_environment=wire(env)
        return query,runtime,env,native,{}
