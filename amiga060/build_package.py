#!/usr/bin/env python3
"""Assemble a local test package; do not download or commit historical binaries."""
import hashlib
import pathlib
import shutil
import subprocess
import sys

here = pathlib.Path(__file__).resolve().parent
source, output = map(pathlib.Path, sys.argv[1:])
commit = '61e059cccf8f719a7624266220604c1e5bcaca41'
if subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip() != commit:
    raise SystemExit('Support checkout must be at ' + commit)
for line in (here / 'UPSTREAM_SHA256SUMS').read_text().splitlines():
    digest, name = line.split('  ', 1)
    if hashlib.sha256((source / name).read_bytes()).hexdigest() != digest:
        raise SystemExit('Upstream hash mismatch: ' + name)
output.mkdir(parents=True, exist_ok=False)
payload = output / 'payload'
hybrid = payload / 'Minimig_Hybrid'
hybrid.mkdir(parents=True)
for name in ['qemu', 'kernel_patch']:
    shutil.copytree(source / 'Minimig_Hybrid' / name, hybrid / name)
shutil.copy2(here / 'scripts/start', hybrid / 'start')
(hybrid / 'cpu_model').write_text('m68020\n')
control = payload / 'Amiga060_Testing'
control.mkdir()
shutil.copy2(source / 'MiSTer', control / 'Hybrid_Main')
for name in ['activate.sh', 'restore.sh', 'set_cpu.sh']:
    shutil.copy2(here / 'scripts' / name, control / name)
(payload / '_Computer').mkdir()
shutil.copy2(source / '_Computer/MinimigHybrid.rbf', payload / '_Computer/Amiga_060_Testing.rbf')
shutil.copy2(here / 'scripts/install.sh', output / 'install.sh')
shutil.copy2(here / 'README.md', output / 'README.md')
shutil.copy2(here.parent / 'CREDITS.md', output / 'CREDITS.md')
shutil.copy2(here / 'UPSTREAM_SHA256SUMS', output / 'UPSTREAM_SHA256SUMS')
(output / 'SOURCE.txt').write_text('https://github.com/scrameta/MiSTer_Hybrid_Support\n' + commit + '\nNo binary modifications; RBF renamed only. See CREDITS.md for source and licence caveats.\n')
(output / 'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + str(p.relative_to(output)) + '\n' for p in sorted(output.rglob('*')) if p.is_file()))
print(output)
