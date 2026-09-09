# Personal Agent Spec: The Build Steward

## FL-06 — Design Your Personal Agent

---

## 1. Job to Be Done

**One sentence:** Every Friday, review my FlyRank portfolio repo, detect drift between the README status table and actual files, flag blockers older than one week, and run the pressure-test pipeline on any new or updated markdown deliverables — then report back with a prioritized action list for the weekend.

**Why this job:** My portfolio has 15+ deliverables across 5 weeks, a status table that I update manually, and a pressure-test criteria (claim / audience / action) that I sometimes skip when I'm tired. The risk is not a missing file — it's a *dishonest* status table that claims "Final" when the file still has placeholder brackets, or a new deliverable that ships without running the voice-check. The agent's job is to be the honest mirror I can't be for myself on a Friday evening.

**Scope boundary:** The agent does NOT write commits, does NOT post to course forums, and does NOT rewrite files without my explicit approval per-item. It reads, flags, suggests, and reports. I remain the human in the loop for every action.

---

## 2. User and Usage Frequency

| Field | Detail |
|-------|--------|
| **User** | Me (the builder). I know the repo structure, the course timeline, and which blockers are real vs. aspirational. |
| **Frequency** | Weekly, every Friday at 18:00, plus on-demand when I type "steward check" before a major commit. |
| **Duration** | The report takes ~3 minutes to read. Reviewing flagged items and deciding what to fix takes 15–30 minutes. |
| **Trigger** | Scheduled (weekly) + manual (pre-commit). No ambient monitoring. |

**Why Friday evening:** I typically do FlyRank coursework on weekends. A Friday report lets me decide Saturday's priority before I start, rather than wasting Saturday morning figuring out where I left off.

---

## 3. Tools and Data Needed

### 3.1 Data Sources

| Data | Location | Access Method |
|------|----------|---------------|
| README status table | `C:\Users\velan\FlyRank\README.md` | File read via MCP filesystem server |
| Deliverable markdown files | `C:\Users\velan\FlyRank\*.md` | File read via MCP filesystem server |
| Asset directories | `C:\Users\velan\FlyRank\assets\**` | Directory listing via MCP filesystem server |
| Git status | Local git repo | Shell command execution (`git status`, `git log --oneline -5`) |
| Course timeline | External URL (bookmark) | I provide the link manually; the agent does NOT scrape external sites |

### 3.2 Tools

| Tool | Purpose | Why It Exists |
|------|---------|---------------|
| `read_file` | Read any markdown file to check content | From existing MCP filesystem server (`mcp_server.py`) |
| `list_directory` | Check if referenced assets (images, screenshots) actually exist | From existing MCP filesystem server |
| `git_status` | Check for uncommitted changes before a "steward check" | Shell command wrapper; agent calls it, I approve output |
| `run_pressure_test` | Apply the claim/audience/action criteria to a markdown file's text | This is a prompt tool — the agent runs the 3-criteria check internally and outputs a flag table |
| `generate_report` | Compile findings into a structured markdown report | Agent's internal compilation step; no external tool needed |

### 3.3 Access Plan

- **MCP filesystem server**: Already built (`mcp_server.py` from FL-04). Runs locally via stdio transport. The agent connects to it through a Claude Project or local script.
- **Git commands**: Executed in the local shell where the repo lives. The agent does not need GitHub API access — it only reads local state.
- **No external APIs**: The agent does not call CoffeeDB.pro, Claude API, or any web service. All data is local filesystem + my manual inputs.

---

## 4. Draft Instructions

### System Prompt (What the Agent Is)

```
You are the Build Steward. You work for one person: the builder of the FlyRank portfolio.
Your job is honest weekly review, not cheerleading. If something is wrong, say so clearly.
If something is fine, say so briefly and move on.

You have access to:
- The FlyRank repo at C:\Users\velan\FlyRank
- A filesystem MCP server (read_file, list_directory)
- Local git shell commands (git status, git log)

You do NOT have access to:
- The internet (no web scraping)
- Write access to files (read-only)
- GitHub API (no PRs, no issues)
```

### Weekly Review Workflow (What the Agent Does)

```
STEP 1: Read README.md
- Extract the status table (the markdown table under "## Repo Status")
- List every item, its status emoji, and its claimed state

STEP 2: Cross-check each "Final" or "Documented" item
- For each markdown deliverable marked ✅ or ⚠️, read the actual file
- Check for:
  a) Placeholder brackets: [ ... ] or "add if you have it" or "TODO"
  b) Course-internal language: "FL-03", "Week 4", "assignment"
  c) Missing referenced assets: images linked in markdown that don't exist on disk
  d) Broken internal links: `[file](file.md)` where file.md does not exist
- For each file marked ⏳, check if it has been created at all

STEP 3: Run pressure-test on new or modified files
- Compare file modification time against last review date
- For any file modified since last review, run the 3-criteria check:
  1. CLAIM: Does it support "I ship domain-specific AI products from API to UI"?
  2. AUDIENCE: Does it name the Head of AI's problem, not the builder's skill?
  3. ACTION: Does it have one explicit CTA or next-step bridge?
- Output a flag table: line quoted, criterion failed, brief why

STEP 4: Check repo hygiene
- Run `git status` for uncommitted changes
- Run `git log --oneline -5` for recent commit messages
- Flag if there are uncommitted deliverables (risk of loss)
- Flag if the last commit is >7 days old (stale repo signal)

STEP 5: Generate report
- Format: markdown, 5 sections matching the steps above
- Tone: direct, warm, precise (match the builder's voice)
- Length: 1–2 pages max. Bullet points, not paragraphs.
- End with: "Priority order for this weekend" — top 3 actions only.
```

### On-Demand Trigger ("steward check")

```
When the user says "steward check" before a commit:
- Run ONLY Step 3 (pressure-test) on the files in `git status --short`
- Run ONLY Step 4 (repo hygiene) — check for uncommitted files
- Output a 5-bullet pre-flight checklist, not a full report
```

---

## 5. Five Eval Cases

Eval cases define what "done well" looks like before I build. I will run these manually after the agent is built to verify it behaves correctly.

### Eval 1: Placeholder Detection

**Setup:** Create a fake markdown file `test-eval.md` containing: `Before this, I [relevant background — add if you have it].`

**Expected:** Agent flags this as "Placeholder found: bracketed incomplete text in line X."

**Pass if:** The flag is specific (quotes the exact line) and correctly identifies it as a placeholder, not a link.

### Eval 2: Status Table Drift

**Setup:** Change README.md status table to mark `through-line.md` as ✅ Final, but do not edit `through-line.md` (it still contains "Deadline: FL-03").

**Expected:** Agent flags: "README claims through-line.md is Final, but file still contains course-internal reference 'FL-03'. Status table may be dishonest."

**Pass if:** Agent cross-references the status claim against the file content, not just parrots the table.

### Eval 3: Missing Asset Reference

**Setup:** Add `![missing](assets/screenshots/does-not-exist.png)` to `sitemap.md`. Do not create the image.

**Expected:** Agent flags: "sitemap.md references assets/screenshots/does-not-exist.png — file not found on disk."

**Pass if:** Agent uses `list_directory` or equivalent to verify the asset exists, not just assumes.

### Eval 4: Pressure-Test on New Content

**Setup:** Append a new paragraph to `case-study-achilles.md`: `I am a skilled developer who leverages cutting-edge AI to deliver holistic solutions.`

**Expected:** Agent flags under criterion AUDIENCE (buzzwords, states skill instead of diagnosing problem) and CLAIM (generic, not specific to domain API → UI).

**Pass if:** Agent correctly identifies both criteria violated, quotes the exact line, and explains why "leverages" and "holistic" fail the voice constraint.

### Eval 5: Repo Hygiene — Stale Check

**Setup:** Do not commit anything for 8 days. Run the scheduled Friday review.

**Expected:** Agent flags: "Last commit was 8 days ago. Repo is stale. Uncommitted changes: [list if any]."

**Pass if:** Agent reads git log, calculates date difference, and warns without panicking.

---

## 6. Risks and Guardrails

### What the Agent Must Confirm (Always Ask)

| Action | Why It Needs Confirmation |
|--------|---------------------------|
| Flagging a file as "not actually Final" | I may have intentionally left a course reference for my own tracking. The agent flags; I decide. |
| Suggesting a specific rewrite | The agent outputs the suggested rewrite in the report, but does NOT write it to disk. I copy-paste if I agree. |
| Declaring a blocker "must be fixed this weekend" | My real-life calendar may override the repo's urgency. The agent suggests priority; I decide. |

### What the Agent Must Never Do

| Forbidden Action | Why |
|-----------------|-----|
| Write to any file in the repo | Read-only by design. The agent is a mirror, not an editor. |
| Execute `git commit`, `git push`, or any write git command | I own the commit history and messages. The agent only reads. |
| Scrape external URLs (course site, CoffeeDB.pro, etc.) | Scope boundary. The agent works with local data only. |
| Share repo contents outside the local session | Privacy guardrail. No cloud logging of file contents. |
| Run more than once per day without explicit trigger | Prevent notification fatigue. Scheduled weekly + manual on-demand only. |
| Flag stylistic preferences as errors | "I prefer shorter paragraphs" is not a criterion. Only claim/audience/action violations count. |

### Failure Modes I've Already Anticipated

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Agent flags too many minor issues → report becomes noise | High | Limit to 3 priority actions per report. Everything else goes in an appendix. |
| Agent misses a subtle placeholder (e.g., "see FL-03" without brackets) | Medium | Add regex for course-code patterns (FL-\d+, Week \d+) to the placeholder scan. |
| Agent hallucinates a file status (claims file is missing when it's just in a subdirectory) | Medium | Use `list_directory` recursively, not hardcoded paths. |
| Agent pressure-test is too lenient on my own writing (confirmation bias) | Medium | The eval cases include deliberately bad text (Eval 4) to test strictness. |
| MCP server crashes or path changes | Low | Include a startup check: "MCP server responding? If not, report error and stop." |

---

## 7. Platform Choice and Justification

### Chosen Platform: Claude Project + Local MCP Filesystem Server

**Setup:** I will extend the existing Achilles Claude Project (configured in `claude-project-setup.md`) with the Build Steward instructions above. The MCP filesystem server from FL-04 (`mcp_server.py`) runs locally and connects via stdio transport. I trigger the agent manually by pasting the workflow prompt into the Claude Project chat, or I run it on a schedule by opening the project every Friday.

### Why Claude Project + MCP

| Factor | How This Platform Serves It |
|--------|----------------------------|
| **Free** | Claude Projects are free. The MCP server is a local Python script I already built. No paid tiers needed. |
| **Uses existing infrastructure** | I already have the MCP filesystem server (`mcp_server.py`) and the Claude Project with Achilles context. Adding a new instruction set is 10 minutes, not a new tool. |
| **No code to maintain** | The "agent logic" is the prompt (instructions + workflow). I don't need to write a Python orchestration layer. The LLM handles the reasoning. |
| **Human in the loop by default** | Claude Project is chat-based. Every output waits for my review. I must explicitly act on suggestions — no accidental auto-commits. |
| **Easy to iterate** | If the pressure-test criteria need tuning, I edit the prompt and rerun. No deployment, no restart, no CI/CD. |

### Alternative Considered: n8n Agent Workflow

**Why I rejected it:** n8n is powerful for multi-step automation, but it requires:
1. A cloud or self-hosted n8n instance (setup time: 2–3 hours)
2. Configuring the MCP server as an n8n node (non-trivial; n8n's stdio node support is limited)
3. Building a visual workflow for something that is essentially "read files → apply prompt → output report"

The n8n path would take 6–8 hours of tooling work before the agent does anything useful. For a weekly 3-minute report, that's over-engineering. Claude Project gives me the same result in the time it takes to write the prompt.

### Alternative Considered: Custom GPT

**Why I rejected it:** Custom GPTs cannot connect to local filesystems. I would need to paste the entire repo contents into the chat window every time, which breaks for files >100KB and misses the cross-reference checking (README vs. actual files). A Custom GPT is good for a chatbot; it's the wrong tool for a repo auditor.

### Alternative Considered: Python Scripted Agent (Anthropic SDK)

**Why I rejected it:** I could write a Python script that calls the Claude API, passes file contents, and outputs a report. This would be fully automated and schedulable. But:
1. It requires API keys and rate-limit management
2. It requires coding the orchestration logic (which files to read, in what order, how to handle MCP connection failures)
3. It requires a scheduler (cron, Windows Task Scheduler)

The scripted path is valid and I may move to it later if the Claude Project manual trigger becomes annoying. For the 10-hour build scope, Claude Project + MCP is the right trade-off: zero new infrastructure, leverages what I already built, and gives me the exact output I need.

---

## 8. Honest Assessment: Will I Actually Use This?

**Yes, but with friction.** The Friday schedule requires me to remember to open the Claude Project and paste the workflow prompt. I will likely forget some Fridays. The on-demand "steward check" before major commits is more realistic — I already ask Claude to review my work informally; this just formalizes the criteria.

**The real value:** Even if I only use it 50% of the time, the act of writing the spec forced me to define what "done" means for every deliverable. The README status table is now under explicit scrutiny, not just vibes. That's the guardrail I needed.

---

## 9. One-Line Summary

**The Build Steward is a read-only weekly repo auditor that cross-checks the README status table against actual file contents, runs the claim/audience/action pressure-test on new deliverables, and reports the top 3 weekend priorities — built as a Claude Project prompt using my existing local MCP filesystem server, because the 10-hour scope doesn't justify n8n infrastructure or API scripting for a 3-minute report.**
