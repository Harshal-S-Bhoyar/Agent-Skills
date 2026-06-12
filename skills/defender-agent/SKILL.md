---
name: defender-agent
description: >-
  Orchestrates the end-to-end security pipeline (Threat Model -> Scan -> Triage -> Validate -> Patch -> Report).
  Use this to run the full automated Defender security audit on a target codebase.
---

# Defender Agent

The Defender Agent is a security orchestrator that automates the full 6-step Defender security pipeline. It coordinates the end-to-end audit workflow so you don't have to run each phase manually.

## What It Does

The agent runs these steps in sequence:

1. **Threat Model** — Map trust boundaries and entry points → `THREAT_MODEL.md`
2. **Scan** — Analyze focus areas for vulnerabilities → `VULN-FINDINGS.json`
3. **Triage** — Deduplicate, rank, and verify findings → `TRIAGE.json`
4. **Validate** — Establish exploitability and preconditions
5. **Patch** — Generate minimal, root-cause diffs with variant hunts → `PATCHES/`
6. **Report** — Synthesize executive summary and technical details → `SECURITY_REPORT.md`

## How to Use

Trigger a full audit:
```
@defender-agent audit <target-dir>
```

Or run individual phases via the `@defender` skill:
```
@defender threat-model <target-dir>
@defender scan <target-dir>
@defender triage <findings.json> --repo <target-dir>
@defender patch <triage.json> --repo <target-dir>
@defender report <triage.json> --repo <target-dir>
```

## Constraints

- **Static analysis only** — no execution, no fuzzing, no network probing
- **Read-only codebase** — patches are written as `.diff` files, never applied directly
- **Containment** — stays within the target directory boundaries

## Related Skill

This agent depends on the **defender** skill for rules, workflows, checklists, and methodology. See `C:\Users\harshal.bhoyar\.gemini\antigravity\skills\defender\SKILL.md`.
