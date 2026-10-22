#!/usr/bin/env python3
"""Check that migrated core files stay pristine and theme assets preserve provenance.

Run from any directory: python3 tools/esagu/check_isolation.py
Requires the baseline/source commits in the local Git history; does not access a DB.
This is an isolation check, not a Moodle runtime or upgrade test.
"""
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT / 'docs/esagu/restored-core-files.json').read_text())
failures = []

def blob(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT)

for path in manifest['paths']:
    if (ROOT / path).read_bytes() != blob(manifest['baseline'], path):
        failures.append(f'Core file modified again: {path}')

for name in ('completion-auto-y', 'completion-manual-y'):
    path = ROOT / f'theme/evagu/pix_core/i/{name}.svg'
    ET.fromstring(path.read_bytes())
    if path.read_bytes() != blob(manifest['source'], f'pix/i/{name}.svg'):
        failures.append(f'Completion icon differs from original ESAGU asset: {name}')

config = (ROOT / 'theme/evagu/config.php').read_text()
if "array_merge(['esagu-core-overrides'], $ccnSheets)" not in config:
    failures.append('Extracted stylesheet must load before existing EVAGU sheets')

# The theme already overrides the core login template; do not replace its custom layout.
login = 'theme/evagu/templates/core/loginform.mustache'
if (ROOT / login).read_bytes() != blob(manifest['source'], login):
    failures.append('Review changes to existing EVAGU login template for visual parity')

if failures:
    print('\n'.join(failures), file=sys.stderr)
    sys.exit(1)
print(f'OK: {len(manifest["paths"])} core files match baseline; icon provenance and theme registration verified.')
print('NOT TESTED: Moodle execution, CSS cascade in browser, database migrations, newer Moodle releases.')
