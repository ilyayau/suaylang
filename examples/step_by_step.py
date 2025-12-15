import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from suaylang.interpreter import run_source

src = """\
inc ← ⌁(x) x + 1

fact ← ⌁(n)
  ⟲ (n 1) ▷ ⟪
    ▷ (0 acc) ⇒ ↯ acc
    ▷ (k acc) ⇒ ↩ ((k - 1) (acc × k))
  ⟫

x ← 3
x ⇐ inc · x
say · ("fact=" ⊞ (text · (fact · x)))
"""

# trace=True prints evaluation enter/exit with indentation.
run_source(src, trace=True)
