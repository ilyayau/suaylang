# Releasing SuayLang: Artifact Protocol

## Release Checklist

1. **Ensure all results are up to date:**
   - Run `make reproduce-all` and `make research-pdf tech-report-pdf`.
   - Confirm results/ and PDFs are current.

2. **Create release artifact:**
   - Run `make release-artifacts`
   - This produces `dist/results_<gitsha>.tar.gz` containing:
     - results/ (all outputs)
     - docs/COMMITTEE_ONEPAGER.md
   - docs/TECH_REPORT.md (PDF: run `make tech-report-pdf`)
     - results/baseline.md, results/diff_report.md, results/benchmarks.md
     - dist/MANIFEST.txt (git sha, date, Python version, OS info)

3. **Tag the release:**
   - `git tag v0.1.x`
   - `git push --tags`

4. **Attach artifact to GitHub Release:**
   - Go to GitHub Releases, create a new release for the tag.
   - Upload `dist/results_<gitsha>.tar.gz` as an asset.
   - Note: Reviewers can download results without rerunning.

5. **CI Evidence:**
   - Every CI run uploads results/ and PDFs as workflow artifacts (see Actions tab).
   - Artifact name includes commit sha, retention 30 days.

## Reviewer Instructions
- Download the release artifact or CI artifact for full evidence.
- See [results/README.md](../results/README.md) for artifact index.
- See [docs/COMMITTEE_ONEPAGER.md](COMMITTEE_ONEPAGER.md) for summary.
