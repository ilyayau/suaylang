# Backward compatibility policy

Spec versioning is independent from code versioning.

## Policy

- Patch versions: clarify text or tighten tests without changing semantics.
- Minor versions: may add features behind explicit version gates; must not break existing programs unless declared.
- Major versions: may remove or redefine features.

## Compatibility artifacts

- Any incompatible change must be accompanied by:
  - an updated spec/VERSION
  - conformance tests demonstrating the change
  - a note in CHANGELOG.md
