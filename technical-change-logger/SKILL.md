---
name: technical-change-logger
description: Use when documenting architectural or code changes to maintain a detailed, reversible changelog.
metadata:
  category: meta
  triggers: changelog, logging, documentation, revert, technical_changelog
---

# Technical Change Logger

Use this skill to maintain the `TECHNICAL_CHANGELOG.md` file in the root of the repository. Every significant code change must be recorded here to ensure architectural traceability and allow for easy reverts.

## MANDATORY: Auto-Documentation Requirement
**This skill MUST be triggered automatically by the agent after every successful code modification.** Do not wait for the user to ask. If you have edited a file, you must document it in `TECHNICAL_CHANGELOG.md` before concluding your turn.

## Guidelines

1. **Location & Append Mode**: Always update `TECHNICAL_CHANGELOG.md` in the repository root. **CRITICAL: NEVER OVERWRITE existing contents.** You must APPEND new changes to the file, preserving all previous entries exactly as they were.
2. **Immediate Logging**: Register each change in `TECHNICAL_CHANGELOG.md` AS SOON AS the change is made. Do not wait to batch multiple unrelated changes.
3. **Comprehensive Listing**: 
   - You MUST list **EVERY** file that was modified. 
   - For every file, you MUST provide a specific "Before" and "After" code block showing exactly what changed. **Do not use "Examples" or generic summaries for a group of files.**
4. **Format**: Use the following structure for each entry:
   - **Date & Time**: [ISO 8601 Date] [Accurate Current Local Time in IST, e.g., 07:15:33 PM IST] (Must be the exact time the registration is being written in Indian Standard Time).
   - **Change Title**: Short descriptive title.
   - **Context/Rationale**: Why was this change needed?
   - **Detailed File Changes**: 
     - **File Path**: [Full Path]
     - **Before**: [Code Block]
     - **After**: [Code Block]
   - **Revert Instructions**: Specific steps or code blocks to undo the change.

5. **Atomic Documentation**: Document changes immediately after they are successfully applied to the codebase.

## Example Entry

```markdown
## [2026-04-30 10:30 AM] Hardening Repository Retrieval Methods

### Context
Methods like `Get`, `GetAsync`, and `GetAllAsync` had empty `catch { }` blocks that masked database errors.

### Detailed File Changes

#### File: `EmcureNPD.Data.DataAccess\Core\Repositories\Repository.cs`
**Before:**
```csharp
catch (Exception ex) { }
```

**After:**
```csharp
catch (Exception ex)
{
    _logger?.LogError(ex, "Error in GetAllAsync for entity {EntityName}", _EntityName);
    throw;
}
```

### Revert Procedure
Replace the try-catch block back to the empty catch version.
```

## Anti-Rationalization
- **NO SUMMARIES**: Avoid saying "updated all appsettings." Instead, list each `appsettings.json` separately with its specific change.
- **NO DELAY**: Documentation is part of the "Definition of Done" for any code task.
