import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('/home/sergio/Projects/personal/claude-toolbox')
V = ROOT / 'docs/feat/wip/functional-review/verification/task12/r7-conclusions'
spec = importlib.util.spec_from_file_location('audit_runner', V / 'runner.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
freeze = runner.configure()
frozen = runner.matrix.controller.verify_frozen(freeze)
seed = runner.matrix.seed
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
counts = collections.Counter()
runs = []
knowledge = set()
credentials = [v.encode() for v in runner.matrix.codex.secrets()]
for side, snapshot in runner.matrix.controller.SNAPSHOTS.items():
    for p in (V/'source-inputs'/side).iterdir():
        if p.is_file(): assert p.read_bytes() == (snapshot/p.name).read_bytes(), p
for job in runner.jobs_for(freeze):
    e, w = job.evidence, job.workspace
    launch, prepared, done = (read(e / f) for f in ('launch.json', 'prepared.json', 'completion.json'))
    assert done['exit_code'] == 0 and not done.get('interrupted_by') and not done.get('finalization_failed'), e
    for name, digest in read(e / 'manifest.json').items():
        assert sha(e / name) == digest, (e, name)
        assert not any(value in (e/name).read_bytes() for value in credentials), (e,name)
        counts['capture_files'] += 1
    assert sha(e / 'launch.json') == prepared['launch_sha256']
    assert sha(e / 'prompt.txt') == prepared['prompt_sha256']
    assert sha(e / 'initial.patch') == prepared['patch_sha256']
    assert (e / 'initial.patch').read_bytes() == (e / 'final.patch').read_bytes(), e
    assert seed.git(w, 'rev-parse', 'HEAD').decode().strip() == launch['review_base']
    assert seed.sha(seed.git(w, 'diff', '--cached', '--binary')) == prepared['patch_sha256']
    if 'release_revision' in launch:
        assert seed.git(w, 'rev-parse', 'eval-release').decode().strip() == launch['release_revision']
    for name, digest in launch['initial_files'].items():
        assert done['final_files'][name] == digest == sha(w / name), (e, name)
    additions = sorted(set(done['final_files']) - set(launch['initial_files']))
    assert sha(w / '.capy.toml') == prepared['capy_config_sha256']
    assert launch['knowledge_path'] not in knowledge
    knowledge.add(launch['knowledge_path'])
    for name, digest in prepared['runtime_files'].items():
        assert sha(w / name) == digest, (w, name)
        counts['runtime_files'] += 1
    subprocess.run([sys.executable, '-B', str(V.parents[1] / 'prepare-bundles.py'), 'verify',
        str(w / 'plugins/kk'), str(job.snapshot / 'retained-manifest.json'), job.provider.replace('claude','klaude').replace('codex','kodex') + '-plugin'], check=True, capture_output=True)
    assert launch['actor'] == read(job.snapshot / 'identity.json')
    assert launch['fixture_manifest_sha256'] == sha(freeze)
    assert read(e / 'launch-validation.json')['status'] == 'PASS'
    if job.provider == 'codex':
        main = read(e / 'thread.json')
        assert main['model'] == 'gpt-6-astra' and main['reasoningEffort'] == 'xhigh'
        threads = [read(p)['thread'] for p in e.glob('thread-*.json')]
        for thread in threads:
            if thread['parentThreadId']:
                assert thread['agentRole'] == 'code-reviewer' and thread['model'] == 'gpt-6.1-sol' and thread['reasoningEffort'] == 'xhigh', thread['id']
                assert thread['parentThreadId'] == main['thread']['id']
                counts['codex_children'] += 1
        assert read(e / 'binding.json')['operative_manifest_verified']
        assert read(e / 'binding.json')['generated_role_bytes_verified']
    else:
        for line in (e / 'events.jsonl').read_text().splitlines():
            event = json.loads(line)
            event = event.get('event', event)
            message = event.get('message',{})
            model = event.get('model') or (message.get('model') if isinstance(message,dict) else None)
            if model:
                assert model == 'claude-opus-5-5', (e, model)
                counts['claude_model_receipts'] += 1
    g = V / 'grading' / e.name
    manifest = read(g / 'manifest.json')
    assert manifest['original_manifest_sha256'] == sha(e / 'manifest.json')
    for record in manifest['files']:
        assert sha(g / record['path']) == record['sha256'], (g, record['path'])
        counts['grading_files'] += 1
    payload = read(V / 'dispatches' / (e.name + '.json'))
    assert sha(g / 'manifest.json') in payload['message'] and str(g) in payload['message']
    grade = V / 'grades' / (e.name + '.md')
    correction = V / 'grade-corrections' / (e.name + '.md')
    rows = re.findall(r'^\|\s*(\d+\.\d+)\s*\|\s*(PASS|FAIL|PARTIAL)\s*\|', grade.read_text(), re.M)
    assert sorted(x[0] for x in rows) == sorted(x['id'] for x in read(g / 'assertions.json'))
    if correction.exists():
        corrected = re.findall(r'^\|\s*(\d+\.\d+)\s*\|\s*(PASS|FAIL|PARTIAL)\s*\|', correction.read_text(), re.M)
        assert len(corrected) == len(dict(corrected)) and set(dict(corrected)) <= set(dict(rows))
        rows = list((dict(rows) | dict(corrected)).items())
        grade = correction
    counts['assertions'] += len(rows)
    runs.append({'run':e.name,'capture_manifest':sha(e/'manifest.json'),'grading_manifest':sha(g/'manifest.json'),
        'grade_path':str(grade.relative_to(V)),'grade_sha256':sha(grade),
        'original_grade_sha256':sha(V/'grades'/(e.name+'.md')),
        'dispatch_sha256':sha(V/'dispatches'/(e.name+'.json')),'added_subject_paths':additions})
for manifest in sorted((V / 'admin').glob('*/*/manifest.json')):
    for name, digest in read(manifest).items():
        assert sha(manifest.parent / name) == digest, (manifest, name)
        counts['administrative_files'] += 1
for record in sorted((V / 'admin').glob('*/untrust/untrust.json')):
    assert read(record)['prior_absence_restored'] is True
    counts['restored_trust_entries'] += 1
for manifest in V.glob('binding-*/manifest.json'):
    for name,digest in read(manifest).items():
        assert sha(manifest.parent/name)==digest
        counts['binding_files']+=1
assert len(runs) == 48 and counts['assertions'] == 336
print(json.dumps({'status':'PASS','counts':dict(counts),'runs':runs,
    'frozen_inputs':'unchanged','bundles_verified':len(runs),'unique_knowledge_paths':len(knowledge),
    'archived_source_inputs':'byte-identical to frozen snapshots','configured_credential_scan':'no matches in sealed measured captures',
    'subject_integrity':'initial files, live Git refs/index and final selected patch unchanged; additions listed per run',
    'limits':['Not behavioral acceptance','No OS-wide read confinement','Exact Codex child prompt content remains unverified']},indent=2))
