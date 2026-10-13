import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tomllib

V=Path('/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/functional-review/verification/task12/r7-conclusions')
allocations=json.loads((V/'cleanup-allocations.json').read_text())
audit=json.loads((V/'integrity-audit.json').read_text())
assert audit['status']=='PASS' and len(audit['runs'])==48
assert len(list((V/'runs').glob('*/completion.json')))==48
cfg=tomllib.loads(Path('/home/sergio/.codex/config.toml').read_text())
assert not any('/tmp/fr-r7-conclusions-20261013' in name for name in cfg.get('projects',{}))
assert not any('fr-r7-' in name for name in cfg.get('plugins',{}))
assert not list(Path('/home/sergio/.codex/plugins/cache').glob('fr-r7-*-20261013'))
secrets=[str(v).encode() for k,v in cfg.get('mcp_servers',{}).get('pal',{}).get('env',{}).items() if any(x in k for x in ('KEY','TOKEN','SECRET')) and v]
archive=V/'temporary-evidence.tar.gz'
assert not archive.exists()
records={}; owned=[]
for record in allocations['owned']:
    p=Path(record['path'])
    assert str(p).startswith('/tmp/kk-') and not p.is_symlink()
    if not p.exists():owned.append({**record,'status':'already absent'});continue
    entries=sorted(p.rglob('*')) if p.is_dir() else [p]
    hashes={}
    for f in entries:
        assert not f.is_symlink(),f
        if f.is_file():
            data=f.read_bytes();assert not any(s in data for s in secrets)
            name=str(f.relative_to('/tmp'));digest=hashlib.sha256(data).hexdigest()
            hashes[name]=digest;records[name]=digest
    owned.append({**record,'status':'archive verified, then removed','files':hashes})
subprocess.run(['tar','--null','-czf',str(archive),'-C','/tmp','-T','-'],input=b'\0'.join(n.encode() for n in sorted(records))+b'\0',check=True)
with tarfile.open(archive) as t:
    assert sorted(t.getnames())==sorted(records)
    for name,digest in records.items():assert hashlib.sha256(t.extractfile(name).read()).hexdigest()==digest
for record in owned:
    p=Path(record['path'])
    if record['status']=='already absent':continue
    for name,digest in record['files'].items():assert hashlib.sha256((Path('/tmp')/name).read_bytes()).hexdigest()==digest
    if p.is_dir():
        for d in [p,*p.rglob('*')]:
            if d.is_dir():d.chmod(d.stat().st_mode | 0o700)
        shutil.rmtree(p)
    else:p.unlink()
    assert not p.exists()
print(json.dumps({'status':'PASS','archive':'temporary-evidence.tar.gz','archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
    'files_archived':len(records),'owned':owned,'untouched_unproven_directories':allocations['unproven_existing_references'],
    'temporary_project_trust':'absent','temporary_plugin_registration':'absent','temporary_plugin_cache':'absent',
    'workspaces':'retained for final independent integrity review; runtime inputs archived separately',
    'known_configured_credential_scan':'no matches'},indent=2))
