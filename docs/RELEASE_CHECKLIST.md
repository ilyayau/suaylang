# Release Checklist

1. Run `make reproduce-all` and `make research-pdf tech-report-pdf`.
2. Run `make release-artifacts`.
3. Tag release: `git tag v0.1.x && git push --tags`.
4. Attach `dist/results_<gitsha>.tar.gz` to GitHub Release.
5. Record sha256 checksums for PDF and results bundle.
6. Confirm CI artifacts are uploaded and downloadable.
