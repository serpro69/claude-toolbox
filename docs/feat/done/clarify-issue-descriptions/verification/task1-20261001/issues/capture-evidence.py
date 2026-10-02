"""Preserve visible native session records; never export hidden reasoning."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("agent_path")
parser.add_argument("output")
parser.add_argument("--stage")
args = parser.parse_args()
output = Path(args.output)
output.mkdir(parents=True, exist_ok=True)
matches = []
for path in Path('/Users/sergio/.codex/sessions/2026/10/01').glob('*.jsonl'):
    with path.open() as stream:
        first = json.loads(next(stream))
    if first.get('payload', {}).get('agent_path') == args.agent_path:
        matches.append(path)
assert len(matches) == 1, matches
source = matches[0]
lines = source.read_text().splitlines()
rows = [json.loads(line) for line in lines]
meta = rows[0]['payload']
contexts = [r['payload'] for r in rows if r['type'] == 'turn_context']
visible = []
calls, results, answers = [], [], []
for line, row in zip(lines, rows):
    p = row.get('payload', {})
    kind = p.get('type')
    keep = False
    if row['type'] == 'response_item':
        if kind in ('custom_tool_call', 'function_call', 'custom_tool_call_output', 'function_call_output'):
            keep = True
            (results if kind.endswith('_output') else calls).append(p.get('call_id'))
        elif kind == 'message' and p.get('role') == 'assistant' and p.get('channel') != 'analysis':
            keep = True
            if p.get('channel') == 'final' or p.get('phase') == 'final_answer':
                answers.append('\n'.join(c.get('text', '') for c in p.get('content', [])))
    elif row['type'] == 'event_msg' and kind in ('task_started', 'task_complete'):
        keep = True
    if keep:
        visible.append(line)
(output/'trace.jsonl').write_text('\n'.join(visible) + '\n')
(output/'final.md').write_text('\n\n'.join(answers) + '\n')
metadata = {
    'agent_path': args.agent_path,
    'session_id': meta.get('id'),
    'parent_thread_id': meta.get('parent_thread_id'),
    'source_rollout': str(source),
    'source_sha256_at_capture': hashlib.sha256(source.read_bytes()).hexdigest(),
    'agent_role': meta.get('agent_role'),
    'model_provider': meta.get('model_provider'),
    'cli_version': meta.get('cli_version'),
    'turn_settings': [{k: p.get(k) for k in ('model', 'effort', 'cwd', 'approval_policy', 'sandbox_policy')} for p in contexts],
    'trace_policy': 'Raw complete tool calls/results and visible assistant messages; hidden reasoning and system boilerplate excluded. Exact plaintext transport request saved before dispatch in editor/reader/grader-prompt.txt.',
    'call_count': len(calls),
    'result_count': len(results),
    'unmatched_calls': [c for c in calls if c not in results],
    'final_message_present': bool(answers),
    'live_connector_certification': 'excluded',
}
(output/'actual-metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
if args.stage:
    stage = Path(args.stage)
    shutil.copytree(stage, output/'after')
    hashes = {str(p.relative_to(stage)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(stage.rglob('*')) if p.is_file()}
    (output/'after-sha256.json').write_text(json.dumps(hashes, indent=2) + '\n')
print(json.dumps(metadata))
