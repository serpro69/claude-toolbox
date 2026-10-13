import collections
import json
from pathlib import Path
import re

V=Path('/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/functional-review/verification/task12/r7-conclusions')
counts=collections.Counter(); suspicious=[]; foreign=[]; mcp=collections.Counter(); broad=[]
pattern=re.compile(r'docs/feat/wip/functional-review|/oracle/|eval\.json|expected-verdicts\.json|gold-claims\.json|/source-inputs/|/tmp/fr-r7-(?:baseline|candidate)-20261013')
for p in sorted((V/'grading').glob('*/events/*.json')):
    d=json.loads(p.read_text()); i=d.get('item',{}); b=d.get('block',{})
    kind=''; data={}
    if b.get('type')=='tool_use':kind=b['name'];data=b.get('input',{})
    elif i.get('type')=='commandExecution':kind='commandExecution';data={'command':i['command']}
    elif i.get('type')=='mcpToolCall':
        kind='mcpToolCall'; data=i.get('arguments',{});mcp[i['server']+'/'+i['tool']]+=1
    elif i.get('type')=='subAgentActivity':kind='subAgentActivity';data={k:v for k,v in i.items() if k!='result'}
    elif i.get('type')=='collabAgentToolCall':kind='collabAgentToolCall';data=i
    elif i.get('type')=='fileChange':kind='fileChange';data={'paths':[c['path'] for c in i.get('changes',[])]}
    else:continue
    counts[kind]+=1
    s=json.dumps(data)
    where=str(p.relative_to(V))
    if pattern.search(s):suspicious.append(where)
    for target in re.findall(r'/tmp/fr-r7-conclusions-20261013/((?:claude|codex)-(?:baseline|candidate)-R[357]-(?:standard|isolated)-[12])',s):
        if target!=p.parents[1].name:foreign.append({'event':where,'target':target})
    if ('AGENTS.md' in s and '/tmp' in s and ('rg --files' in s or 'find ' in s)) or 'ls /tmp/fr-r7-conclusions-20261013' in s:
        broad.append(where)
print(json.dumps({'runs':len(list((V/'grading').glob('*/manifest.json'))),'request_counts':dict(counts),
    'tool_or_lifecycle_records':sum(counts.values()),'shell_requests':counts['Bash']+counts['commandExecution'],
    'mcp_calls':dict(mcp),'explicit_evaluator_path_requests':suspicious,'explicit_foreign_run_requests':foreign,
    'instruction_filename_or_parent_discovery_requests':broad,
    'inspection':'Controller inspected every complete tool request during package preparation; this targeted scan supplements that inspection.',
    'conclusion':'No evaluator content read observed; metadata discovery can extend outside the current run.',
    'limits':['Trace-based access audit, not OS-wide confinement','Exact Codex child prompt bodies are unavailable']},indent=2))
