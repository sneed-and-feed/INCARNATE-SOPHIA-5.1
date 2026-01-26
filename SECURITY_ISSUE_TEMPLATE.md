---
name: Security report
about: Report a security issue or exploit (PGP encrypted payload recommended)
title: "[CRITICAL] - <short description>"
labels: security, critical
assignees: ''
---

## Summary
Provide a one-sentence summary of the issue.

## Affected artifact
- **Version / Commit:** `commit=<commit-hash>`
- **Binary manifest:** `manifest.json` signature: `<signature-hash>`

## Impact
Describe the impact (e.g., grid collapse, data exfiltration).

## Reproduction steps
1. Environment (OS, Python version, hardware)
2. Exact commands and inputs
3. Expected vs actual behavior

## Proof of Concept
- **Encrypted PoC:** Attach PGP-encrypted file or paste PGP block here.
- **If PGP not available:** provide a ROT13 hint only (do not include full exploit).

## Disclosure preferences
- Coordinated disclosure window requested (e.g., 90 days)
- Contact method (PGP-encrypted email or GitHub private issue)

## Additional notes
Any logs, stack traces, or artifacts (PGP-encrypted).
