import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np


def _ensure_dirs():
    os.makedirs('results/img', exist_ok=True)
    os.makedirs('docs/plots', exist_ok=True)

def plot_performance():
    with open('results/baseline_raw.json') as f:
        data = json.load(f)
    labels = ['Python', 'Interpreter', 'VM']
    py = [b['python']['median_runtime'] for b in data['benchmarks']]
    interp = [b['suay_interpreter']['median_runtime'] for b in data['benchmarks']]
    vm = [b['suay_vm']['median_runtime'] for b in data['benchmarks']]
    means = [np.mean(py), np.mean(interp), np.mean(vm)]
    plt.figure(figsize=(4,3))
    plt.bar(labels, means, color=['#4e79a7','#f28e2b','#76b7b2'])
    plt.ylabel('Mean Runtime (s)')
    plt.title('Performance Comparison')
    plt.tight_layout()
    _ensure_dirs()
    plt.savefig('results/img/performance.png', dpi=150)
    plt.savefig('docs/plots/performance.png', dpi=200)
    # Committee-facing alias name (requested by reviewer UX docs)
    plt.savefig('results/img/interp_vs_vm.png', dpi=150)
    plt.savefig('docs/plots/interp_vs_vm.png', dpi=200)
    plt.close()

def plot_coverage():
    # Coverage here refers to language-feature/opcode coverage over the shipped corpora,
    # as computed by the coverage pipeline (not test coverage).
    with open('results/coverage.json') as f:
        cov = json.load(f)

    termination = cov.get('termination_counts', {})
    labels = list(termination.keys())
    values = [termination[k] for k in labels]

    plt.figure(figsize=(5, 3))
    plt.bar(labels, values)
    plt.ylabel('Count')
    plt.title('Corpus termination outcomes')
    plt.tight_layout()
    _ensure_dirs()
    plt.savefig('results/img/coverage.png', dpi=150)
    plt.savefig('docs/plots/coverage.png', dpi=200)
    plt.close()

def main():
    ap = argparse.ArgumentParser(prog="plot-results")
    ap.add_argument(
        "--fast",
        action="store_true",
        help="Generate only the minimal plot set for CI reproduce-fast.",
    )
    args = ap.parse_args()

    plot_performance()
    if not args.fast:
        plot_coverage()

if __name__ == '__main__':
    main()
