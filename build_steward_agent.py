"""Build Steward Agent — FL-07

A read-only weekly repo auditor that connects to the local MCP filesystem server,
cross-checks the README status table against actual files, scans for issues,
reports repo hygiene, and outputs a structured markdown report.

Run with:  python build_steward_agent.py
Requires: mcp_server.py in the same directory, git in PATH.
"""

import asyncio
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from mcp import stdio_client
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters
from mcp.types import TextContent

REPO_ROOT = Path(__file__).parent.resolve()
SERVER_PATH = REPO_ROOT / "mcp_server.py"

# ---------------------------------------------------------------------------
#  Regex scanners
# ---------------------------------------------------------------------------

# Placeholder brackets that look incomplete  (e.g.  [relevant background — add ...])
PLACEHOLDER_RE = re.compile(
    r"\[[^\]]*(?:add|TODO|placeholder|relevant|if you have|insert|fill in)[^\]]*\]",
    re.IGNORECASE,
)

# Course-internal language
COURSE_RE = re.compile(
    r"\b(FL-\d+|Week\s+\d+|assignment|deliverable)\b",
    re.IGNORECASE,
)

# Markdown image references  ![alt](path)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

# Markdown internal links  [text](path.md)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+\.md)\)")

# Claim keywords that suggest generic language (weak signals)
GENERIC_CLAIM_RE = re.compile(
    r"\b(leverage|synergy|cutting-edge|state-of-the-art|holistic|results-driven|optimize|streamline|empower)\b",
    re.IGNORECASE,
)

# Buzzwords that state skill rather than audience problem
BUZZWORD_RE = re.compile(
    r"\b(skilled developer|AI-powered solutions|expert in|master of|passionate about)\b",
    re.IGNORECASE,
)


def _text(content_result) -> str:
    """Extract text from an MCP tool result."""
    for c in content_result.content:
        if isinstance(c, TextContent):
            return c.text
    return ""


# ---------------------------------------------------------------------------
#  MCP helpers
# ---------------------------------------------------------------------------

async def mcp_read_file(session, path: str) -> str:
    result = await session.call_tool("read_file", {"path": path})
    return _text(result)


async def mcp_list_dir(session, path: str) -> list[str]:
    result = await session.call_tool("list_directory", {"path": path})
    txt = _text(result)
    if txt.startswith("Error"):
        return []
    return [line.strip() for line in txt.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
#  Step 1 — Read README status table
# ---------------------------------------------------------------------------

def extract_status_table(readme_text: str) -> list[dict]:
    """Parse the markdown table under ## Repo Status."""
    # Find the status table section
    match = re.search(
        r"##\s+Repo\s+Status\s*\n\n?(\|.*?\n[\s\S]*?)(?=\n##|\n\*\*|$)",
        readme_text,
        re.IGNORECASE,
    )
    if not match:
        return []
    table = match.group(1).strip()
    lines = [ln for ln in table.splitlines() if ln.strip().startswith("|")]
    # Drop header separator line (contains only |, -, :, spaces)
    data_lines = [
        ln for ln in lines
        if not re.fullmatch(r"[\|\-\s:]+", ln.strip().replace(" ", ""))
    ]
    # Drop the first real header line too (it has text, not just dashes)
    # Actually let's parse properly: first line is header, second is separator, rest are data
    if len(data_lines) < 2:
        return []
    header = data_lines[0]
    data_lines = data_lines[1:]
    # Skip separator-looking lines in data too
    data_lines = [ln for ln in data_lines if not set(ln.strip()).issubset({"|", "-", ":", " "})]

    items = []
    for ln in data_lines:
        cells = [c.strip() for c in ln.split("|")]
        cells = [c for c in cells if c]  # drop empty edge cells
        if len(cells) >= 2:
            items.append({"item": cells[0], "status": cells[1]})
    return items


# ---------------------------------------------------------------------------
#  Step 2 — Cross-check files
# ---------------------------------------------------------------------------

async def scan_file(session, filepath: Path, repo_root: Path) -> dict:
    """Read a markdown file and scan for known failure modes."""
    text = await mcp_read_file(session, str(filepath))
    flags = []

    # 2a — Placeholder brackets
    for m in PLACEHOLDER_RE.finditer(text):
        line_num = text[:m.start()].count("\n") + 1
        flags.append({
            "type": "placeholder",
            "line": line_num,
            "snippet": m.group(0)[:80],
        })

    # 2b — Course-internal language (skip lines that are clearly table-of-contents / index)
    lines = text.splitlines()
    for m in COURSE_RE.finditer(text):
        line_num = text[:m.start()].count("\n")
        line = lines[line_num] if line_num < len(lines) else ""
        # Skip if the line is a deliverables/week index entry (starts with | **Week or | Week)
        if re.search(r"^\|\s*\*+Week\s+\d+", line.strip()):
            continue
        flags.append({
            "type": "course-internal",
            "line": line_num + 1,
            "snippet": m.group(0),
        })

    # 2c — Missing assets
    for m in IMAGE_RE.finditer(text):
        img_path = m.group(1)
        # Resolve relative to repo root or file's directory
        if img_path.startswith(("http://", "https://")):
            continue  # external images, skip
        candidate = repo_root / filepath.parent / img_path
        candidate2 = repo_root / img_path
        if not candidate.exists() and not candidate2.exists():
            line_num = text[:m.start()].count("\n") + 1
            flags.append({
                "type": "missing-asset",
                "line": line_num,
                "snippet": img_path,
            })

    # 2d — Broken internal links
    for m in LINK_RE.finditer(text):
        link_path = m.group(1)
        candidate = repo_root / filepath.parent / link_path
        candidate2 = repo_root / link_path
        if not candidate.exists() and not candidate2.exists():
            line_num = text[:m.start()].count("\n") + 1
            flags.append({
                "type": "broken-link",
                "line": line_num,
                "snippet": link_path,
            })

    return {"path": str(filepath.relative_to(repo_root)), "flags": flags}


# ---------------------------------------------------------------------------
#  Step 3 — Pressure-test (deterministic keyword scan)
# ---------------------------------------------------------------------------

def pressure_test(text: str, filename: str) -> list[dict]:
    """Run deterministic claim/audience/action checks."""
    flags = []
    lines = text.splitlines()

    # CLAIM check: generic buzzwords that weaken specificity
    # Skip lines where the word appears in a "forbidden words" list or inside explicit quotes
    # (those lines are teaching what NOT to do, not using the word as copy)
    for i, line in enumerate(lines, 1):
        for m in GENERIC_CLAIM_RE.finditer(line):
            # Skip if preceded by a quote mark or inside a parenthetical forbidden list
            start = m.start()
            prefix = line[max(0, start - 30):start]
            if '"' in prefix or "'" in prefix or "buzzwords" in prefix.lower() or "forbidden" in prefix.lower():
                continue
            flags.append({
                "criterion": "CLAIM",
                "line": i,
                "snippet": line.strip()[:120],
                "why": f"Contains generic buzzword '{m.group(0)}' — does not support the specific claim.",
            })

    # AUDIENCE check: language that states skill instead of diagnosing problem
    for i, line in enumerate(lines, 1):
        for m in BUZZWORD_RE.finditer(line):
            # Skip eval-case setup lines (they contain deliberately bad text as examples)
            start = m.start()
            prefix = line[max(0, start - 40):start]
            if "setup" in prefix.lower() or "append" in prefix.lower() or "bad text" in line.lower():
                continue
            flags.append({
                "criterion": "AUDIENCE",
                "line": i,
                "snippet": line.strip()[:120],
                "why": f"States builder skill ('{m.group(0)}') instead of naming the Head of AI's problem.",
            })

    # ACTION check: look for vague CTAs like "get in touch"
    vague_cta_re = re.compile(r"\b(get in touch|contact me|reach out)\b", re.IGNORECASE)
    for i, line in enumerate(lines, 1):
        for m in vague_cta_re.finditer(line):
            # Skip meta-descriptions (e.g. "One action: Reach out to me to build...")
            # Those are proof-statement descriptions, not actual page CTAs
            if re.search(r"(proof statement|one action|desired action|audience is)", line, re.IGNORECASE):
                continue
            flags.append({
                "criterion": "ACTION",
                "line": i,
                "snippet": line.strip()[:120],
                "why": f"Vague CTA ('{m.group(0)}') — does not bridge to a concrete next step.",
            })

    return flags


# ---------------------------------------------------------------------------
#  Step 4 — Repo hygiene (subprocess git)
# ---------------------------------------------------------------------------

def git_hygiene(repo_root: Path) -> dict:
    """Run git status and git log, return parsed hygiene info."""
    result = {"uncommitted": [], "last_commit": None, "recent_commits": []}

    try:
        status = subprocess.run(
            ["git", "status", "--short"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if status.returncode == 0:
            result["uncommitted"] = [ln.strip() for ln in status.stdout.splitlines() if ln.strip()]
    except Exception as e:
        result["uncommitted_error"] = str(e)

    try:
        log = subprocess.run(
            ["git", "log", "--oneline", "-5", "--format=%h %s (%ci)"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if log.returncode == 0:
            lines = [ln.strip() for ln in log.stdout.splitlines() if ln.strip()]
            result["recent_commits"] = lines
            if lines:
                # Parse the date from the first line: hash msg (YYYY-MM-DD HH:MM:SS +ZZZZ)
                m = re.search(r"\((\d{4}-\d{2}-\d{2})", lines[0])
                if m:
                    result["last_commit"] = m.group(1)
    except Exception as e:
        result["log_error"] = str(e)

    return result


# ---------------------------------------------------------------------------
#  Step 5 — Generate report
# ---------------------------------------------------------------------------

def generate_report(
    status_items: list[dict],
    file_checks: list[dict],
    pressure_flags: list[dict],
    hygiene: dict,
    runtime_sec: float,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Build Steward — Weekly Review Report",
        "",
        f"*Generated: {now}*",
        f"*Runtime: {runtime_sec:.1f}s*",
        "",
        "---",
        "",
        "## 1. Status Table Summary",
        "",
        f"| Item | Claimed Status |",
        f"|------|----------------|",
    ]
    for item in status_items:
        lines.append(f"| {item['item']} | {item['status']} |")

    lines.extend(["", "---", "", "## 2. File Cross-Check", ""])

    total_flags = 0
    for fc in file_checks:
        fname = fc["path"]
        flags = fc["flags"]
        if flags:
            total_flags += len(flags)
            lines.append(f"### {fname}")
            for f in flags:
                lines.append(f"- **{f['type']}** (line {f['line']}): `{f['snippet']}`")
            lines.append("")
        else:
            lines.append(f"- **{fname}** — Passes. No flags.")

    if total_flags == 0:
        lines.append("No flags found across all checked files.")

    lines.extend(["", "---", "", "## 3. Pressure-Test Flags", ""])
    if pressure_flags:
        for pf in pressure_flags:
            fname = pf["file"]
            lines.append(f"### {fname}")
            for fl in pf["flags"]:
                lines.append(
                    f"- **{fl['criterion']}** (line {fl['line']}): {fl['why']}"
                )
                lines.append(f"  > `{fl['snippet']}`")
            lines.append("")
    else:
        lines.append("No pressure-test flags found.")

    lines.extend(["", "---", "", "## 4. Repo Hygiene", ""])
    if hygiene.get("uncommitted"):
        lines.append(f"- **Uncommitted files:** {len(hygiene['uncommitted'])}")
        for u in hygiene["uncommitted"]:
            lines.append(f"  - `{u}`")
    else:
        lines.append("- **Uncommitted files:** None. Working tree clean.")

    if hygiene.get("last_commit"):
        lines.append(f"- **Last commit:** {hygiene['last_commit']}")
    else:
        lines.append("- **Last commit:** (could not determine)")

    if hygiene.get("recent_commits"):
        lines.append("- **Recent commits:**")
        for c in hygiene["recent_commits"]:
            lines.append(f"  - `{c}`")

    # Calculate staleness
    if hygiene.get("last_commit"):
        try:
            last = datetime.strptime(hygiene["last_commit"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            today = datetime.now(timezone.utc)
            days = (today - last).days
            if days > 7:
                lines.append(f"- ⚠️ **Repo stale:** Last commit was {days} days ago.")
            else:
                lines.append(f"- **Repo freshness:** {days} days since last commit.")
        except ValueError:
            pass

    lines.extend(["", "---", "", "## 5. Priority Order for This Weekend", ""])

    # Build top-3 priorities automatically
    priorities = []
    if hygiene.get("uncommitted"):
        priorities.append("Commit uncommitted deliverables before they drift.")
    stale_count = sum(1 for fc in file_checks if fc["flags"])
    if stale_count:
        priorities.append(f"Fix {stale_count} flagged file issue(s) (placeholders, missing assets, course-internal language).")
    if pressure_flags:
        priorities.append("Review pressure-test flags — at least one file has weak claim/audience/action language.")
    if not priorities:
        priorities.append("Repo is clean. Work on the next deliverable or capture the missing screenshots.")
    if len(priorities) < 3:
        priorities.append("Check the ⏳ items in the status table — move one to ⚠️ or ✅.")
    if len(priorities) < 3:
        priorities.append("Update the build steward prompt if any false positives were flagged.")

    for i, p in enumerate(priorities[:3], 1):
        lines.append(f"{i}. {p}")

    lines.extend(["", "---", "", "*End of report.*"])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------

async def main():
    import time
    start = time.time()

    if not SERVER_PATH.exists():
        print(f"ERROR: MCP server not found at {SERVER_PATH}")
        sys.exit(1)

    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            print(f"=== Build Steward connected to {init.serverInfo.name} ===\n")

            # STEP 1 — Read README
            readme_path = REPO_ROOT / "README.md"
            readme_text = await mcp_read_file(session, str(readme_path))
            status_items = extract_status_table(readme_text)
            print(f"STEP 1: Found {len(status_items)} items in status table.")

            # STEP 2 — Cross-check every ✅ and ⚠️ item
            # Collect ALL markdown deliverables in the repo root.
            # We exclude build logs and generated artifacts to avoid noise.
            EXCLUDED = {"build-steward-run.txt", "mcp_test_output.txt", "mcp_test_evidence.txt"}
            md_files_to_check = sorted(
                [f for f in REPO_ROOT.glob("*.md") if f.name not in EXCLUDED]
            )
            file_checks = []
            print(f"STEP 2: Checking {len(md_files_to_check)} markdown files...")
            for fp in md_files_to_check:
                check = await scan_file(session, fp, REPO_ROOT)
                file_checks.append(check)
                if check["flags"]:
                    print(f"  ⚠️  {check['path']}: {len(check['flags'])} flag(s)")
                else:
                    print(f"  ✅  {check['path']}: clean")

            # Also check index.html for placeholder / missing asset references
            index_path = REPO_ROOT / "index.html"
            if index_path.exists():
                idx_check = await scan_file(session, index_path, REPO_ROOT)
                file_checks.append(idx_check)
                if idx_check["flags"]:
                    print(f"  ⚠️  {idx_check['path']}: {len(idx_check['flags'])} flag(s)")
                else:
                    print(f"  ✅  {idx_check['path']}: clean")

            # STEP 3 — Pressure-test all checked files
            print("\nSTEP 3: Running pressure-test on checked files...")
            pressure_flags = []
            for fp in md_files_to_check:
                text = await mcp_read_file(session, str(fp))
                flags = pressure_test(text, fp.name)
                if flags:
                    pressure_flags.append({"file": fp.name, "flags": flags})
                    print(f"  ⚠️  {fp.name}: {len(flags)} pressure flag(s)")
                else:
                    print(f"  ✅  {fp.name}: passes pressure-test")

            # STEP 4 — Repo hygiene
            print("\nSTEP 4: Checking repo hygiene...")
            hygiene = git_hygiene(REPO_ROOT)
            if hygiene.get("uncommitted"):
                print(f"  ⚠️  {len(hygiene['uncommitted'])} uncommitted file(s)")
            else:
                print("  ✅  Working tree clean")
            if hygiene.get("last_commit"):
                print(f"  📅  Last commit: {hygiene['last_commit']}")

            # STEP 5 — Generate and write report
            elapsed = time.time() - start
            report = generate_report(status_items, file_checks, pressure_flags, hygiene, elapsed)

            report_path = REPO_ROOT / "build-steward-run.txt"
            report_path.write_text(report, encoding="utf-8")
            print(f"\n=== Report saved to {report_path} ({len(report)} chars) ===")
            print(f"=== Total runtime: {elapsed:.1f}s ===")

            # Also print a preview
            print("\n--- Report Preview (first 40 lines) ---\n")
            for ln in report.splitlines()[:40]:
                print(ln)
            print("\n... (see build-steward-run.txt for full report) ...")


if __name__ == "__main__":
    asyncio.run(main())
