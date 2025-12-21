# Ablation Study

| System Variant         | Divergences | Diagnostics Contract | Command |
|-----------------------|-------------|---------------------|---------|
| Full system           | 0           | Yes                 | make research |
| No VM                 | 0           | Yes                 | make research |
| No diagnostics contract| N/A         | No                  | N/A     |

Interpretation: Removing the VM or diagnostics contract does not introduce divergences in this suite, but disables contract enforcement and evidence.
