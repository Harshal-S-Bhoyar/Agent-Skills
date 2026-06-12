---
name: change-traker
description: >-
  Use when recording, documenting, or tracking code changes, refactors, bug fixes, features, or test updates in a Markdown changelog file.
metadata:
  category: discipline
  triggers: change-traker, change tracking, document changes, changelog, record changes, code modification, refactor log, git changes
---

# Change Tracker (`change-traker`)

The `change-traker` skill enforces consistent, high-fidelity documentation of code modifications across any codebase (especially Rust and TypeScript projects). It guarantees that all changes—whether features, refactors, bug fixes, or test updates—are systematically recorded in a designated Markdown log file.

## Iron Law

**NEVER modify the codebase without recording the exact changes in the Markdown log file using the `change-traker` entry format. If no log file is specified by the user, you MUST ask for it before proceeding.**

Violating the letter of this documentation standard IS violating the spirit of repository safety.

---

## When to Use

- **Refactoring:** Cleaning up, optimizing, or restructuring code.
- **Bug Fixes:** Resolving crashes, errors, logic issues, or edge cases.
- **Feature Additions:** Implementing new functionality, APIs, components, or modules.
- **Test Updates:** Adding, modifying, or repairing unit or integration tests.
- **Task Milestones:** Completing key phases of an implementation plan.

**NOT for:**
- Explaining code concepts in normal chat (use direct replies instead).
- General brainstorming without code changes.

---

## The Rule (Step-by-Step)

### 1. Identify or Request the Target Log File
- Look for a Markdown file path provided by the user (e.g., `changelog.md`, `CHANGELOG.md`, `revisions.md`, `change-log.md`).
- **If none is provided:** Immediately ask the user: *"Please specify the target Markdown file where I should record the changes."* Do not assume or guess a filename.

### 2. Verify and Load Current Log Content
- Read the target Markdown file (using `view_file`) if it already exists, to avoid overwriting unrelated or previous entries.
- **If the file does not exist:** Create it from scratch using the template format.

### 3. Record Details for Every Change
For each change, you must capture:
- **Timestamp:** ISO 8601 local format (e.g., `YYYY-MM-DD HH:MM:SS [TimeZone]`).
- **File Paths:** Relative to the workspace root.
- **Type of Change:** Refactor, Bug Fix, Feature, Test, or Hybrid.
- **Why / Problem:** Clear explanation of why the change is necessary and what problem it resolves.
- **Implementation Summary:** What precisely was modified in a clean, structured bullet-point list.
- **Before vs After Diff:** Direct code blocks representing what was replaced and what was introduced. Use standard markdown `diff` syntax with `-` and `+`.
- **Status:** Complete, Partial, or Uncertain. Mark partial/uncertain changes clearly with a warning banner or status marker.

### 4. Group Multiple Changes
- If multiple files are modified under the same task/issue, group them under a single logical entry, but clearly label the individual files and differences.

### 5. Append with Integrity
- Append the new entry at either the top or bottom of the log file, keeping existing contents exactly intact (do not overwrite historical records).
- Keep entries highly concise yet technically complete.

---

## 🔗 Supporting Reference Files

To keep context lightweight, the specific templates and multi-language examples are moved to supporting files:
- **[template.md](file:///C:/Users/harshal.bhoyar/.gemini/antigravity/skills/change-traker/references/template.md)**: The standard Markdown entry template to copy-paste.
- **[examples.md](file:///C:/Users/harshal.bhoyar/.gemini/antigravity/skills/change-traker/references/examples.md)**: Real-world example logs for TypeScript and Rust changes.

---

## Common Rationalizations to Avoid

| Excuse / Rationalization | Reality |
| :--- | :--- |
| *"The change is too small to log."* | No change is too small. Even one-line fixes can cause regression. Document it. |
| *"I will write the log at the very end."* | Documenting as you go prevents forgotten details and ensures the diff is exact. |
| *"I'll just overwrite the old entries."* | Historic logs are crucial for debugging regressions. Always append or prepend. |

## Red Flags - STOP

- Appending a summary without file paths or timestamps.
- Guessing the log file name (e.g., creating `changelog.md` without asking when the user wanted `revisions.md`).
- Omitting the exact Before vs After code diff blocks.

**If you catch these red flags:** Stop, reread the rules, and correct the format immediately.
