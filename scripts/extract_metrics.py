import json
import sys
from pathlib import Path

def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

root = Path(__file__).parent.parent
baseline = root / 'results' / 'baseline_raw.json'
diff = root / 'results' / 'diff_report.json'
bench = root / 'results' / 'bench_raw.json'

if not baseline.exists() or not diff.exists() or not bench.exists():
    fail('Missing input results file(s)')

with open(baseline) as f:
    b = json.load(f)
with open(diff) as f:
    d = json.load(f)
with open(bench) as f:
    be = json.load(f)

print('''
| Program | Python (s) | SuayInterp (s) | SuayVM (s) |
|---------|------------|---------------|-----------|')
''')
for row in b['benchmarks']:
    print(f"| {row['name']} | {row['python']['median_runtime']:.3f} | {row['suay_interpreter']['median_runtime']:.3f} | {row['suay_vm']['median_runtime']:.3f} |")

total = d.get('total_programs', 'N/A')
div = d.get('divergences', 'N/A')
print(f"\n**Diff test:** {total} programs, {div} divergences")

bfast = be['benchmarks'][0]['median_runtime'] if be.get('benchmarks') else 'N/A'
print(f"\n**Benchmark (first):** {bfast}")

sys.exit(0)
