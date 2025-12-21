# Reviewer Attack Questions (SuayLang)

1. What does “observational equivalence” mean here, exactly?
2. Where is the observation policy defined? Is it formal or ad hoc?
3. Could the formatting-insensitive comparator hide real divergences?
4. Are error codes and exit codes compared, or just values?
5. Is 5001 programs enough? What is the generator’s bias?
6. Are the seeds fixed and documented?
7. Is the claim falsifiable by construction, or could the harness miss real bugs?
8. What breaks on non-Linux or non-Python 3.12?
9. Are all dependencies pinned and reproducible?
10. Is the VSCode extension evaluated or not?
11. Are all results files actually produced by the pipeline?
12. What happens if a baseline program fails to parse?
13. Are comments in .suay files handled consistently?
14. Is the diff-test run on the same programs as the baseline?
15. Are all coverage numbers reproducible and explained?
16. What is the comparator’s policy for stdout/stderr?
17. Are all artifacts uploaded to CI/releases?
18. Is the PDF always available, or only sometimes?
19. Are all links in README/docs valid and up to date?
20. What is the minimal path to reproduce the main claim?
21. What happens if a reviewer uses fish shell?
22. What if the reviewer’s Python is 3.13 or 3.11?
23. Are all test dependencies (e.g., hypothesis) documented and installed?
24. Is the “smoke test” path actually minimal and meaningful?
25. Are all limitations and threats to validity explicit and non-handwavy?
26. How are random seeds handled? Is there any non-determinism left?
27. What is the expected output for each artifact file?
28. How are failures reported? Are error messages actionable?
29. Is the artifact bundle downloadable and self-contained?
30. Are all claims in README directly linked to evidence?
