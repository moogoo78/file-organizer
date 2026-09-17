# file-organizer

A [Claude Code](https://claude.com/claude-code) agent skill for organizing messy folders: sort files by project, type or date, find duplicates and version clutter, rename in bulk, and undo every move.

> The skill instructions (`SKILL.md`) are written in Traditional Chinese. Claude understands them regardless of the language you talk to it in.

## Principles

- **Understand → propose → act with approval → everything is undoable.**
- Never deletes files. "Delete" means moving to `_待刪除/` (to-delete) or `_重複檔/` (duplicates) for you to review.
- Organizes by meaning (projects, reference material, your own outputs) rather than just file extension.
- Keeps code projects (`.git`, `package.json`, `pyproject.toml`…) intact and never leaves the target folder.
- Marks each inferred classification HIGH / MEDIUM / LOW; low-confidence files are left for you to decide.
- If a move doesn't make a file easier to find, it stays where it is.

## Install

Requires Python 3 (standard library only).

```bash
git clone https://github.com/moogoo78/file-organizer.git ~/.claude/skills/file-organizer
```

Restart Claude Code, then ask something like:

- "organize my Downloads folder"
- 「幫我整理桌面」
- "find duplicate files in ~/Pictures"

or invoke it directly with `/file-organizer`.

To update: `git -C ~/.claude/skills/file-organizer pull`

## How it works

| Step | What happens |
|---|---|
| 1. Scan | `scripts/scan.py` inventories the folder: file types, sizes, dates, SHA-256 duplicates, temp files, version-like names (`final2`, `copy`, `(1)`, `v3`). |
| 2. Understand | Claude reads paths, names, metadata and (when useful) content to find project boundaries. |
| 3. Propose | A dry-run `plan.json` (by project, or `scripts/plan.py --mode type\|date\|type-date`) shown as a tree + change table with reasons and confidence. |
| 4. Apply | After you approve, `scripts/apply.py` moves files without overwriting (adds `(1)`, `(2)`), verifies results, and writes `.organize_log_<timestamp>.json`. |
| 5. Undo | `scripts/undo.py <log>` puts everything back. |

## Files

```
file-organizer/
├── SKILL.md                  # workflow and safety rules
├── references/principles.md  # detailed guidance: outputs, dates, versions, file types, confidence
└── scripts/
    ├── scan.py
    ├── plan.py
    ├── apply.py
    └── undo.py
```

## Scripts on their own

The scripts work without Claude too:

```bash
python scripts/scan.py ~/Downloads --out scan.json
python scripts/plan.py scan.json --mode type --out plan.json   # review plan.json
python scripts/apply.py plan.json
python scripts/undo.py ~/Downloads/.organize_log_YYYYMMDD_HHMMSS.json
```
