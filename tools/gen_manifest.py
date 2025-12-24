import hashlib
import json
import os
import sys

ARTIFACTS = [
    'baseline_raw.json',
    'baseline.md',
    'diff_report.md',
    'coverage.md',
    'benchmarks.md',
    'golden_diagnostics.md',
    'ablation.md',
    'mutation_catches.md',
    'coverage_by_construct.md',
    'img/performance.png',
    'img/coverage.png',
]

RESULTS_DIR = 'results'

manifest = {
    'commit': os.popen('git rev-parse HEAD').read().strip(),
    'artifacts': {},
    'python_version': sys.version.replace("\n", " ").strip(),
    'os': os.popen('uname -a').read().strip(),
}

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return 'sha256-' + h.hexdigest()

for rel in ARTIFACTS:
    path = os.path.join(RESULTS_DIR, rel)
    if os.path.exists(path):
        manifest['artifacts'][rel] = sha256sum(path)

with open(os.path.join(RESULTS_DIR, 'manifest.json'), 'w') as f:
    json.dump(manifest, f, indent=2)
