#!/usr/bin/env python3
"""
Bulk materialize BMM implementation story files from planning story docs.

This is a "yolo" helper to run the spirit of the BMM `create-story` workflow for
ALL backlog stories in:
  project_management/implementation-artifacts/sprint-status.yaml

Inputs:
  - planning story docs: project_management/planning-artifacts/stories/epic-XX/story-XX-YY-*.md
  - sprint status:       project_management/implementation-artifacts/sprint-status.yaml

Outputs:
  - implementation story files: project_management/implementation-artifacts/<story_key>.md
  - sprint-status.yaml updated: story statuses backlog -> ready-for-dev
                              epic statuses backlog/contexted -> in-progress (when any story created)

Design goal:
  Preserve sprint-status comments/formatting by doing a targeted textual rewrite.
"""

from __future__ import annotations

import datetime as _dt
import glob
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


RE_STORY_KEY_LINE = re.compile(r"^(?P<indent>\s{2})(?P<key>\d+-\d+-[a-z0-9-]+):\s*(?P<status>[a-z-]+)\s*$")
RE_EPIC_KEY_LINE = re.compile(r"^(?P<indent>\s{2})(?P<key>epic-(?P<epic_num>\d+)):\s*(?P<status>[a-z-]+)\s*$")
RE_RETRO_KEY_LINE = re.compile(r"^\s{2}epic-\d+-retrospective:\s*[a-z-]+\s*$")


@dataclass(frozen=True)
class PlanningStory:
    epic_num: int
    story_num: int
    story_title: str
    role: str
    action: str
    benefit: str
    acceptance_blocks: List[str]  # each block is markdown text (Given/When/Then...)
    source_path: Path


def _die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        _die(f"Missing file: {path}")


def _find_planning_story_file(repo_root: Path, epic_num: int, story_num: int) -> Path:
    pat = repo_root / "project_management" / "planning-artifacts" / "stories" / f"epic-{epic_num:02d}" / f"story-{epic_num:02d}-{story_num:02d}-*.md"
    matches = sorted(glob.glob(str(pat)))
    if not matches:
        _die(f"No planning story file found for epic {epic_num} story {story_num} at pattern: {pat}")
    if len(matches) > 1:
        # deterministic: choose lexicographically first
        pass
    return Path(matches[0])


def _strip_front_matter(md: str) -> str:
    # planning story docs include YAML front matter bounded by --- lines
    if md.startswith("---"):
        parts = md.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return md


def _extract_story_statement(body: str) -> Tuple[str, str, str]:
    # Look for the canonical 3-line form:
    # As a X,
    # I want Y,
    # So that Z.
    lines = [ln.rstrip() for ln in body.splitlines()]
    for i in range(len(lines) - 2):
        a, b, c = lines[i : i + 3]
        if re.match(r"^\s*As a\s+.+", a) and re.match(r"^\s*I want\s+.+", b) and re.match(r"^\s*So that\s+.+", c, re.IGNORECASE):
            role = re.sub(r"^\s*As a\s+", "", a, flags=re.IGNORECASE).strip()
            role = role.rstrip(",").rstrip(".").strip()
            action = re.sub(r"^\s*I want\s+", "", b, flags=re.IGNORECASE).strip()
            action = action.rstrip(",").rstrip(".").strip()
            benefit = re.sub(r"^\s*So that\s+", "", c, flags=re.IGNORECASE).strip()
            benefit = benefit.rstrip(",").rstrip(".").strip()
            return role, action, benefit

    # Fallback: accept "As the system," etc, and missing punctuation
    for i in range(len(lines) - 2):
        a, b, c = lines[i : i + 3]
        if re.match(r"^\s*As\s+.+", a, re.IGNORECASE) and re.match(r"^\s*I want\s+.+", b, re.IGNORECASE) and re.match(r"^\s*So that\s+.+", c, re.IGNORECASE):
            role = re.sub(r"^\s*As\s+", "", a, flags=re.IGNORECASE).strip().rstrip(",").rstrip(".")
            action = re.sub(r"^\s*I want\s+", "", b, flags=re.IGNORECASE).strip().rstrip(",").rstrip(".")
            benefit = re.sub(r"^\s*So that\s+", "", c, flags=re.IGNORECASE).strip().rstrip(",").rstrip(".")
            return role.strip(), action.strip(), benefit.strip()

    _die("Could not find a 3-line story statement (As ... / I want ... / So that ...) in planning story doc.")


def _extract_title(body: str, epic_num: int, story_num: int) -> str:
    # Prefer heading: "# Story X.Y: Title"
    m = re.search(rf"^#\s*Story\s+{epic_num}\.{story_num}\s*:\s*(.+?)\s*$", body, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Fallback: first H1
    m2 = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    if m2:
        return m2.group(1).strip()
    return f"Epic {epic_num} Story {story_num}"


def _extract_acceptance_blocks(body: str) -> List[str]:
    # Find the "**Acceptance Criteria:**" marker then split into paragraph blocks.
    m = re.search(r"^\*\*Acceptance Criteria:\*\*\s*$", body, flags=re.MULTILINE)
    if not m:
        _die("Could not find '**Acceptance Criteria:**' section in planning story doc.")

    tail = body[m.end() :].strip()
    if not tail:
        _die("Acceptance Criteria section is empty.")

    # Blocks separated by 1+ blank lines
    raw_blocks = re.split(r"\n\s*\n", tail)
    blocks: List[str] = []
    for blk in raw_blocks:
        blk = blk.strip()
        if not blk:
            continue
        # Ensure each block is a compact markdown snippet
        blocks.append(blk)
    return blocks


def _parse_planning_story(repo_root: Path, epic_num: int, story_num: int) -> PlanningStory:
    src = _find_planning_story_file(repo_root, epic_num, story_num)
    md = _read_text(src)
    body = _strip_front_matter(md)
    title = _extract_title(body, epic_num, story_num)
    role, action, benefit = _extract_story_statement(body)
    ac_blocks = _extract_acceptance_blocks(body)
    return PlanningStory(
        epic_num=epic_num,
        story_num=story_num,
        story_title=title,
        role=role,
        action=action,
        benefit=benefit,
        acceptance_blocks=ac_blocks,
        source_path=src,
    )


def _render_acceptance_criteria(blocks: List[str]) -> str:
    out: List[str] = []
    for idx, blk in enumerate(blocks, start=1):
        # Keep the rich markdown (Given/When/Then/And) as-is under numbered item.
        indented = "\n".join([f"   {ln}" if ln.strip() else "" for ln in blk.splitlines()])
        out.append(f"{idx}.")
        out.append(indented)
        out.append("")  # blank line between ACs
    return "\n".join(out).rstrip() + "\n"


def _summarize_ac(block: str) -> str:
    # Try to pick a meaningful short summary from the first Then line.
    for ln in block.splitlines():
        ln = ln.strip()
        if ln.startswith("**Then**"):
            return re.sub(r"^\*\*Then\*\*\s*", "", ln).strip()
    # fallback: first non-empty line without bold markers
    for ln in block.splitlines():
        ln = ln.strip()
        if ln:
            return re.sub(r"\*\*(Given|When|Then|And)\*\*\s*", "", ln).strip()
    return "Implement acceptance criteria"


def _render_tasks(blocks: List[str]) -> str:
    tasks: List[str] = []
    for idx, blk in enumerate(blocks, start=1):
        summary = _summarize_ac(blk)
        tasks.append(f"- [ ] Implement AC {idx}: {summary} (AC: {idx})")
        # crude subtasks based on common cues
        subtasks: List[str] = []
        if "structured log" in blk.lower() or "structured logging" in blk.lower():
            subtasks.append("Add structured logs with correlation/request id")
        if "audit" in blk.lower() or "audit_events" in blk:
            subtasks.append("Persist audit event with minimum required fields")
        if "escape" in blk.lower() or "markdown" in blk.lower():
            subtasks.append("Ensure Telegram MarkdownV2 escaping for dynamic text")
        if "idempot" in blk.lower():
            subtasks.append("Make operation idempotent and safe to retry")
        if "utc" in blk.lower() or "ist" in blk.lower():
            subtasks.append("Confirm UTC storage + IST presentation rules are followed")
        if not subtasks:
            subtasks.append("Implement core behavior and error handling for this AC")
        subtasks.append("Add/adjust tests covering this AC")
        for s in subtasks:
            tasks.append(f"  - [ ] {s}")

    tasks.append("- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)")
    tasks.append("  - [ ] Run the full test suite locally")
    tasks.append("  - [ ] Confirm no secrets leak into logs")
    return "\n".join(tasks).rstrip() + "\n"


def _render_story_file(ps: PlanningStory, story_key: str) -> str:
    today = _dt.date.today().isoformat()
    return "\n".join(
        [
            f"# Story {ps.epic_num}.{ps.story_num}: {ps.story_title}",
            "",
            "Status: ready-for-dev",
            "",
            "<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->",
            "",
            "## Story",
            "",
            f"As a {ps.role},",
            f"I want {ps.action},",
            f"so that {ps.benefit}.",
            "",
            "## Acceptance Criteria",
            "",
            _render_acceptance_criteria(ps.acceptance_blocks).rstrip(),
            "",
            "## Tasks / Subtasks",
            "",
            _render_tasks(ps.acceptance_blocks).rstrip(),
            "",
            "## Dev Notes",
            "",
            "- **Sources**:",
            f"  - Planning story: `{ps.source_path.as_posix()}`",
            "  - Epics: `project_management/planning-artifacts/epics.md`",
            "  - Architecture: `project_management/planning-artifacts/architecture.md`",
            "- **Cross-cutting guardrails (from architecture/epics)**:",
            "  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.",
            "  - Store timestamps in UTC; render IST only at presentation time.",
            "  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.",
            "  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.",
            "  - Emit structured logs and audit events with correlation/request IDs where applicable.",
            "",
            "### References",
            "",
            f"- Story key: `{story_key}`",
            "- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)",
            "",
            "## Dev Agent Record",
            "",
            "### Agent Model Used",
            "",
            "{{agent_model_name_version}}",
            "",
            "### Debug Log References",
            "",
            "### Completion Notes List",
            "",
            "### File List",
            "",
            "## Change Log",
            "",
            f"- {today}: Created implementation story file from planning artifacts (bulk yolo create-story).",
            "",
            "## Status",
            "",
            "ready-for-dev",
            "",
        ]
    )


def _iter_development_status_lines(lines: Iterable[str]) -> Iterable[Tuple[int, str]]:
    in_section = False
    for i, ln in enumerate(lines):
        if ln.strip() == "development_status:":
            in_section = True
            yield i, ln
            continue
        if in_section:
            # section ends when indentation drops back to 0 and non-empty
            if ln and not ln.startswith(" "):
                in_section = False
            if in_section:
                yield i, ln


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    sprint_status_path = repo_root / "project_management" / "implementation-artifacts" / "sprint-status.yaml"
    impl_dir = repo_root / "project_management" / "implementation-artifacts"

    sprint_text = _read_text(sprint_status_path)
    sprint_lines = sprint_text.splitlines(keepends=False)

    # Collect keys in order and map line indexes for status updates.
    backlog_story_keys: List[Tuple[str, int, int]] = []  # (story_key, epic_num, story_num)
    story_line_idx_by_key: dict[str, int] = {}
    epic_line_idx_by_num: dict[int, int] = {}
    epic_status_by_num: dict[int, str] = {}

    for idx, ln in _iter_development_status_lines(sprint_lines):
        m_epic = RE_EPIC_KEY_LINE.match(ln)
        if m_epic:
            epic_num = int(m_epic.group("epic_num"))
            epic_line_idx_by_num[epic_num] = idx
            epic_status_by_num[epic_num] = m_epic.group("status")
            continue
        if RE_RETRO_KEY_LINE.match(ln):
            continue
        m_story = RE_STORY_KEY_LINE.match(ln)
        if not m_story:
            continue
        key = m_story.group("key")
        status = m_story.group("status")
        story_line_idx_by_key[key] = idx
        m = re.match(r"^(?P<epic>\d+)-(?P<num>\d+)-", key)
        if not m:
            continue
        epic_num = int(m.group("epic"))
        story_num = int(m.group("num"))
        if status == "backlog":
            backlog_story_keys.append((key, epic_num, story_num))

    if not backlog_story_keys:
        print("No backlog stories found. Nothing to do.")
        return 0

    created: List[str] = []
    updated_story_statuses: List[str] = []
    epic_touched: set[int] = set()

    for story_key, epic_num, story_num in backlog_story_keys:
        ps = _parse_planning_story(repo_root, epic_num, story_num)
        out_path = impl_dir / f"{story_key}.md"
        if not out_path.exists():
            out_path.write_text(_render_story_file(ps, story_key), encoding="utf-8")
            created.append(str(out_path.relative_to(repo_root)))
        else:
            # do not overwrite; still move sprint status so dev-story can pick it up
            pass

        # update sprint status line from backlog -> ready-for-dev
        line_idx = story_line_idx_by_key.get(story_key)
        if line_idx is not None:
            ln = sprint_lines[line_idx]
            sprint_lines[line_idx] = re.sub(r":\s*backlog\s*$", ": ready-for-dev", ln)
            updated_story_statuses.append(story_key)
            epic_touched.add(epic_num)

    # Update epic statuses to in-progress when we created any story in them
    for epic_num in sorted(epic_touched):
        idx = epic_line_idx_by_num.get(epic_num)
        if idx is None:
            continue
        current = epic_status_by_num.get(epic_num, "")
        if current in ("backlog", "contexted"):
            sprint_lines[idx] = re.sub(r":\s*(backlog|contexted)\s*$", ": in-progress", sprint_lines[idx])

    sprint_status_path.write_text("\n".join(sprint_lines) + "\n", encoding="utf-8")

    print(f"Created {len(created)} story file(s).")
    print(f"Updated {len(updated_story_statuses)} story status line(s) to ready-for-dev.")
    print(f"Updated {len(epic_touched)} epic status line(s) to in-progress (when applicable).")
    if created:
        print("\nCreated files:")
        for p in created:
            print(f" - {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

