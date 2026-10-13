import hashlib
import json
from pathlib import Path
import shutil
import tarfile

V=Path('/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/functional-review/verification/task12/r7-conclusions')
ROOT=Path('/tmp/fr-r7-conclusions-20261013')
runtime=json.loads((V/'runtime-inputs.json').read_text())
archive=V/runtime['archive']
assert hashlib.sha256(archive.read_bytes()).hexdigest()==runtime['sha256']
with tarfile.open(archive) as t:
    for name,digest in runtime['files'].items():
        assert hashlib.sha256(t.extractfile(name).read()).hexdigest()==digest
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
evidence=sorted([*(V/'runs').glob('*/completion.json'),*V.glob('binding-*/completion.json')])
assert len(evidence)==52 and {p.name for p in ROOT.iterdir()}=={p.parent.name for p in evidence}
records=[]
for completion in evidence:
    directory=completion.parent;launch=json.loads((directory/'launch.json').read_text());state=json.loads(completion.read_text())
    w=Path(launch['workspace'])
    assert w==ROOT/directory.name and w.resolve()==w and not w.is_symlink()
    assert state['exit_code']==0
    for relative,digest in state['final_files'].items():
        assert hashlib.sha256((directory/'final'/relative).read_bytes()).hexdigest()==digest
        assert hashlib.sha256((w/relative).read_bytes()).hexdigest()==digest
    records.append({'workspace':str(w),'evidence':str(directory.relative_to(V)),'final_subject_files_verified':len(state['final_files'])})
for record in records:
    p=Path(record['workspace']);shutil.rmtree(p);assert not p.exists()
ROOT.rmdir()
print(json.dumps({'status':'PASS','removed_workspaces':records,'runtime_archive_verified':runtime['archive'],
    'source_snapshots':'retained locally; source archives and manifests are retained in the verification record',
    'other_paths':'unproven scratch parent and persistent runtime session history untouched'},indent=2))
