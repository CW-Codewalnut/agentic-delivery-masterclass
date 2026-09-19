#!/usr/bin/env python3
"""Render the README's agent catalogue from canonical source files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANIFEST = ROOT / "agents/manifest.json"
START = "<!-- BEGIN GENERATED AGENT CATALOGUE -->"
END = "<!-- END GENERATED AGENT CATALOGUE -->"


def frontmatter_and_body(text: str) -> tuple[str, str]:
    """Split a skill without changing either source segment."""
    if not text.startswith("---\n"):
        return "", text.rstrip()
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError("unterminated skill frontmatter")
    return text[: closing + 5].rstrip(), text[closing + 5 :].strip()


def skill_name(path: str) -> str:
    return Path(path).parent.name


def generated_section() -> str:
    manifest = json.loads(MANIFEST.read_text())
    blocks: list[str] = []
    for number, agent in enumerate(manifest["agents"], 1):
        role_path = agent["role"]
        role_text = (ROOT / role_path).read_text().strip()
        skill_links = ", ".join(
            f"[`{skill_name(path)}`]({path})" for path in agent["skills"]
        )
        diagram = [
            "```mermaid",
            "flowchart LR",
            f'  R["ROLE.md<br/>owns {agent["name"]} gates and selection"]',
        ]
        for index, path in enumerate(agent["skills"], 1):
            diagram.append(
                f'  R -->|"when trigger applies"| S{index}["{skill_name(path)}"]'
            )
        diagram.append(f'  R --> T["{Path(agent["template"]).name}<br/>handoff shape"]')
        diagram.append("```")

        block = [
            "<details>",
            f"<summary><strong>{number}. {agent['name']}</strong> — {agent['outcome']}</summary>",
            "",
            f"- **Owned folder:** [`agents/{agent['id']}/`](agents/{agent['id']}/)",
            f"- **Role:** [`ROLE.md`]({role_path})",
            f"- **Skills owned:** {skill_links}",
            f"- **Output template:** [`{Path(agent['template']).name}`]({agent['template']})",
            "",
            *diagram,
            "",
            "<details>",
            "<summary>Actual <code>ROLE.md</code> text</summary>",
            "",
            f"<!-- source-start:{role_path} -->",
            role_text,
            f"<!-- source-end:{role_path} -->",
            "",
            "</details>",
            "",
        ]
        for path in agent["skills"]:
            text = (ROOT / path).read_text()
            frontmatter, body = frontmatter_and_body(text)
            block.extend(
                [
                    "<details>",
                    f"<summary>Actual <code>{skill_name(path)}/SKILL.md</code> text</summary>",
                    "",
                    f"[`{path}`]({path})",
                    "",
                    f"<!-- source-start:{path} -->",
                    "```yaml",
                    frontmatter,
                    "```",
                    "",
                    body,
                    f"<!-- source-end:{path} -->",
                    "",
                    "</details>",
                    "",
                ]
            )
        block.extend(["</details>", ""])
        blocks.append("\n".join(block))
    return "\n".join(blocks).rstrip()


def update_readme(check: bool) -> None:
    current = README.read_text()
    if current.count(START) != 1 or current.count(END) != 1:
        raise SystemExit("README must contain one generated catalogue marker pair")
    before, remainder = current.split(START, 1)
    embedded, after = remainder.split(END, 1)
    expected = "\n\n" + generated_section() + "\n\n"
    if check:
        if embedded != expected:
            raise SystemExit(
                "README agent catalogue is stale; run python3 scripts/render_readme_agents.py"
            )
        print("README agent catalogue matches 7 roles and 25 skills")
        return
    README.write_text(before + START + expected + END + after)
    print("rendered README agent catalogue from 7 roles and 25 skills")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render or verify README agent toggles from canonical sources."
    )
    parser.add_argument(
        "--check", action="store_true", help="fail if README embedded source is stale"
    )
    args = parser.parse_args()
    update_readme(args.check)


if __name__ == "__main__":
    main()
