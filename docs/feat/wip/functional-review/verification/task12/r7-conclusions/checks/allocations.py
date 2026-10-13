import json
from pathlib import Path
import re

V=Path('/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/functional-review/verification/task12/r7-conclusions')
owned={}
references=set()
for run in sorted((V/'grading').iterdir()):
    requests={}
    for p in sorted((run/'events').glob('*.json')):
        d=json.loads(p.read_text()); item=d.get('item',{}); block=d.get('block',{})
        command=''; output=''; successful=False
        if item.get('type')=='commandExecution':
            command=item.get('command',''); output=item.get('aggregatedOutput') or ''
            successful=item.get('exitCode')==0
        elif block.get('type')=='tool_use':
            requests[block['id']]=block
            references.update(re.findall(r'/tmp/kk-[A-Za-z0-9_.-]+',json.dumps(block.get('input',{}))))
        elif block.get('type')=='tool_result':
            req=requests.get(block.get('tool_use_id'),{})
            command=req.get('input',{}).get('command','')
            output=block.get('content','') or ''
            if not isinstance(output,str): output=json.dumps(output)
            successful=not block.get('is_error',False)
            if req.get('name')=='Write' and successful and 'File created successfully at:' in output:
                file=req['input'].get('file_path','')
                if file.startswith('/tmp/kk-'):
                    owned[file]={'path':file,'kind':'new file','proof':str(p.relative_to(V))}
        references.update(re.findall(r'/tmp/kk-[A-Za-z0-9_.-]+',command))
        if successful and 'prepare_instructions.py' in command:
            for path in set(re.findall(r'/tmp/kk-review-instructions-[A-Za-z0-9_-]+(?=/part-)',output)):
                owned[path]={'path':path,'kind':'instruction packet','proof':str(p.relative_to(V))}
        if successful and 'mktemp ' in command:
            for path in re.findall(r'(?m)^(/tmp/kk-[A-Za-z0-9_.-]+)\s*$',output):
                if 'XXXX' not in path:
                    owned[path]={'path':path,'kind':'mktemp allocation','proof':str(p.relative_to(V))}
        if successful and 'tempfile.mkdtemp(' in command:
            paths=re.findall(r'"bundle": "(/tmp/kk-[A-Za-z0-9_.-]+)"',output)+re.findall(r'(?m)^(/tmp/kk-[A-Za-z0-9_.-]+)\s*$',output)
            for path in paths:
                owned[path]={'path':path,'kind':'mkdtemp allocation','proof':str(p.relative_to(V))}
for capture in sorted(V.glob('binding-claude-*/events.jsonl')):
    requests={}
    for line in capture.read_text().splitlines():
        d=json.loads(line);event=d.get('event',d)
        for block in event.get('message',{}).get('content',[]):
            if block.get('type')=='tool_use':requests[block['id']]=block
            if block.get('type')=='tool_result':
                request=requests.get(block.get('tool_use_id'),{})
                command=request.get('input',{}).get('command','')
                output=block.get('content','')
                if not isinstance(output,str):output=json.dumps(output)
                if 'prepare_instructions.py' in command and not block.get('is_error',False):
                    for path in set(re.findall(r'/tmp/kk-review-instructions-[A-Za-z0-9_-]+(?=/part-)',output)):
                        owned[path]={'path':path,'kind':'binding instruction packet','proof':str(capture.relative_to(V)),'source_sequence':d.get('sequence')}
for path in list(owned):
    if any(Path(path).is_relative_to(Path(other)) and path!=other for other in owned):del owned[path]
print(json.dumps({'owned':list(owned.values()),'unproven_existing_references':[
    p for p in sorted(references) if Path(p).exists() and not any(Path(p).is_relative_to(Path(o)) for o in owned)]},indent=2))
