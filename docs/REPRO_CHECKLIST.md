# External Reproducibility Checklist

Instructions for external reproduction:

1. Clone the repo: `git clone <repo-url>`
2. Create and activate a virtual environment.
3. Install dependencies: `python -m pip install -e .`
4. Run: `make research`
5. Check all results in the `results/` directory.

## Template for external reviewer
- [ ] I was able to install and run `make research` without errors.
- [ ] All results files were generated as described in results/README.md.
- [ ] The numbers in README.md match the generated artifacts.
- [ ] I confirm the commit hash and environment metadata in results/manifest.json.
- [ ] (Optional) I ran a subset of tests or benchmarks and got similar results.

Please submit this checklist as a comment or issue for reproducibility credit.
