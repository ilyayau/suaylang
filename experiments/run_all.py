# Run all experiments and regenerate results deterministically

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    root = Path(__file__).parent.parent
    subprocess.check_call([
        sys.executable, "-m", "tools.research_run",
        "--out-dir", str(root / "results"),
        "--diff-profile", "ci",
        "--bench-profile", "smoke"
    ])
    # TODO: Add regression minimization and results/regressions/ handling.
    print("All results regenerated. See results/README.md.")
