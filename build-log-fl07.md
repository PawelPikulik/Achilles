# FL-07 Build Log: The Build Steward Agent

## What I Built

A runnable Python script (`build_steward_agent.py`) that connects to the existing MCP filesystem server from FL-04 and executes the full 5-step weekly review workflow defined in the Build Steward spec. It reads the repo, cross-checks deliverables, scans for issues, pressure-tests content, checks git hygiene, and outputs a structured markdown report.

**Runtime:** ~1.0 seconds for the entire FlyRank repo (22 markdown files + `index.html`).

---

## Deviation from FL-06 Spec

The FL-06 spec chose **Claude Project + local MCP** as the platform. For FL-07, building a Claude Project involves manual UI configuration (pasting instructions into a web form) — there is no source file to commit, no build step, and no reproducible artifact. The assignment asks for a "working agent" with a build log and an unedited run capture.

**Deviation:** I built a **Python script** (`build_steward_agent.py`) that connects to the same MCP server and executes the same workflow. The script IS the reproducible artifact. It can be run from the terminal with `python build_steward_agent.py`, committed to the repo, and executed by anyone who clones it.

**Rationale:**
- A Python script is version-controllable, reviewable, and testable — a Claude Project prompt is not.
- The script connects to the same MCP filesystem server the spec already requires, so no new infrastructure.
- The deterministic regex approach avoids API keys, rate limits, and LLM cost.
- The build log can document real bugs and fixes — impossible with a web-based Claude Project.

---

## What Broke and What Changed

### Bug 1: File Detection Found 0 Markdown Files

**Symptom:** First run: "Checking 0 markdown files..." Only `index.html` was checked.

**Root cause:** The script tried to extract filenames from the status table text using backtick regex (`\`([^`]+\.md)\``). The status table items don't contain backtick-wrapped filenames — the filenames live in a separate deliverables table earlier in the README.

**Fix:** Replaced filename extraction with a glob: collect ALL `*.md` files in the repo root (minus excluded artifacts). This is more robust and thorough.

**Code change:**
```python
# Before: fragile regex extraction from status table item text
# After: glob all markdown files, exclude known artifacts
EXCLUDED = {"build-steward-run.txt", "mcp_test_output.txt", "mcp_test_evidence.txt"}
md_files_to_check = sorted(
    [f for f in REPO_ROOT.glob("*.md") if f.name not in EXCLUDED]
)
```

---

### Bug 2: False Positives — Course-Internal Language in README Index

**Symptom:** `README.md` was flagged with 26 "course-internal" hits for lines like `| **Week 01 — Proof Statement**`. These are legitimate table-of-contents entries, not problematic course references inside deliverable content.

**Root cause:** The `COURSE_RE` regex (`FL-\d+|Week\s+\d+|assignment|deliverable`) matches anywhere, including the deliverables index table.

**Fix:** Added a context check: skip lines that start with `| **Week` or `| Week` — these are index entries, not deliverable body text.

**Code change:**
```python
line = lines[line_num] if line_num < len(lines) else ""
if re.search(r"^\|\s*\*+Week\s+\d+", line.strip()):
    continue
```

**First regex attempt failed:** `\*?` matched zero or one asterisk, but `**Week` has two. The regex didn't match, so the false positives persisted. Fixed to `\*+` to match one or more asterisks.

---

### Bug 3: False Positives — Forbidden Buzzwords in Examples

**Symptom:** `case-study-achilles.md` and `automation-workflow-v2.md` were flagged for containing "leverage", "synergy", "cutting-edge" — but these words appeared in quotes as examples of what NOT to do (e.g., "I don't use buzzwords like 'leverage' or 'synergy.'").

**Root cause:** The `GENERIC_CLAIM_RE` regex matches any occurrence, including in quoted examples and forbidden-word lists.

**Fix:** Added a prefix check: skip matches preceded by a quote mark or the words "buzzwords" / "forbidden" in the preceding 30 characters.

**Code change:**
```python
prefix = line[max(0, start - 30):start]
if '"' in prefix or "'" in prefix or "buzzwords" in prefix.lower() or "forbidden" in prefix.lower():
    continue
```

---

### Bug 4: False Positives — Deliberately Bad Eval Text

**Symptom:** `build-steward-prompt-and-evals.md` was flagged for "skilled developer" in Eval 4's setup instructions. That text is explicitly designed to be bad — it's the test input for the eval case.

**Root cause:** The `BUZZWORD_RE` regex matched the eval setup text.

**Fix:** Added context check for eval-case setup lines (lines containing "setup", "append", or "bad text").

---

### Bug 5: False Positives — "Reach Out" in Proof Statement Meta-Line

**Symptom:** `README.md` line 5 (`**One action:** Reach out to me to build...`) was flagged as a vague CTA.

**Root cause:** The vague CTA regex caught "reach out" anywhere, including in meta-descriptions of the proof statement's action.

**Fix:** Added a context check: skip lines containing "proof statement", "one action", "desired action", or "audience is" — these are meta-descriptions, not page CTAs.

---

## What I Cut from the Spec

### Cut: LLM-Powered Pressure-Test

The FL-06 spec implies the pressure-test (claim/audience/action criteria) would be applied by an LLM (Claude Project). In the Python script, I replaced this with **deterministic regex keyword scanning**.

**Why:**
- No API keys required. The script runs entirely offline after MCP server startup.
- Deterministic output: same input → same output every time. An LLM might flag different lines on different runs.
- Speed: the entire repo scans in <1 second. An LLM call would take 5–15 seconds per file.
- Honest limitation: regex is a blunt instrument. It produces false positives (flagged in the build log above) and misses subtle issues. The spec's eval cases (Eval 4) test whether a human would catch nuanced problems — the script surfaces candidates for that human review.

### Cut: Scheduled Friday Trigger

The spec calls for a weekly Friday review. The script has no scheduler.

**Why:** Scheduling (cron, Task Scheduler) is OS-specific and adds 2–3 hours of setup. The script is designed for on-demand execution: `python build_steward_agent.py`. The user can add a scheduler later if the manual trigger becomes annoying.

### Cut: MCP Server Auto-Start

The script assumes `mcp_server.py` is in the same directory and starts it via stdio. It does not bundle or install the MCP server.

**Why:** The server is already built from FL-04. Rebuilding it would be duplication. The script simply connects to it.

---

## Architecture Decisions

| Decision | Chosen | Rejected | Why |
|----------|--------|----------|-----|
| Pressure-test engine | Deterministic regex | LLM API call | Offline, fast, reproducible, no keys |
| File discovery | Glob `*.md` | Parse README tables | Robust, handles new files automatically |
| Git access | Subprocess `git status` | MCP tool for git | Git is not a filesystem operation; subprocess is native |
| Output format | Markdown report | JSON or structured log | Human-readable, matches the spec's report format |
| Write access | None (read-only) | Auto-fix suggestions | Spec guardrail: agent is a mirror, not an editor |

---

## Verification: Does It Match the Spec?

| Spec Requirement | Implementation | Evidence |
|-------------------|----------------|----------|
| Read README status table | ✅ `extract_status_table()` | Report §1 shows all 21 items |
| Cross-check every ✅/⚠️ file | ✅ Glob all `*.md` + `index.html` | Report §2 lists 22 files checked |
| Scan for placeholders | ✅ `PLACEHOLDER_RE` | Found `[relevant background — add if you have it]` in `case-study-achilles.md` |
| Scan for course-internal language | ✅ `COURSE_RE` with context filter | Found `FL-03` in `through-line.md` after filtering index lines |
| Scan for missing assets | ✅ `IMAGE_RE` + `list_directory` | Found `github-pages-404-before-enable.png` referenced but not on disk |
| Scan for broken links | ✅ `LINK_RE` + existence check | Found `file.md` in eval setup (deliberate test case) |
| Pressure-test claim/audience/action | ✅ Deterministic regex | Report §3 flags eval-case bad text and generic language |
| Repo hygiene (git status, git log) | ✅ `git_hygiene()` | Report §4 shows uncommitted files and last commit |
| Top-3 priority list | ✅ `generate_report()` auto-builds | Report §5 lists actionable priorities |
| Read-only enforcement | ✅ Script never calls `write_file` | Confirmed by code review — only `read_file` and `list_directory` |

---

## Known Limitations (Honest)

1. **Regex pressure-test is blunt.** It flags quoted examples and misses subtle voice mismatches. Eval 4 in the spec requires human judgment — the script surfaces the candidate, the human decides.
2. **Missing-asset check is shallow.** It checks whether the file exists on disk, not whether the image renders or is the correct resolution.
3. **No diff against previous run.** The report is a snapshot. It doesn't say "this file was clean last week, now it has 3 new flags." That would require storing previous reports.
4. **Windows-specific git date parsing.** The `git log --format=%ci` parsing assumes a specific date format. On non-Windows git configs it might fail silently.

---

## One-Sentence Summary

**The Build Steward is a 160-line Python script that connects to the existing local MCP filesystem server, scans 22 markdown deliverables for placeholders, course references, missing assets, and broken links, applies deterministic keyword pressure-tests, checks git hygiene, and outputs a human-readable priority report in 1 second — built as a script instead of a Claude Project for version control and reproducibility.**
