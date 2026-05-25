#!/usr/bin/env python3
import argparse
import html
import logging
import re
import subprocess
import tempfile
from pathlib import Path

from common import add_common_args, project_root, setup_logging


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def table_to_html(lines):
    rows = []
    for line in lines:
        cells = [inline_md(c.strip()) for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) >= 2 and all(set(c.replace(":", "").replace("-", "").strip()) == set() for c in rows[1]):
        header = rows[0]
        body = rows[2:]
    else:
        header = []
        body = rows
    out = ["<table>"]
    if header:
        out.append("<thead><tr>" + "".join(f"<th>{c}</th>" for c in header) + "</tr></thead>")
    out.append("<tbody>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def markdown_to_html(markdown: str) -> str:
    out = []
    paragraph = []
    bullets = []
    table = []

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            out.append("<p>" + "<br>".join(inline_md(x.rstrip("  ")) for x in paragraph) + "</p>")
            paragraph = []

    def flush_bullets():
        nonlocal bullets
        if bullets:
            out.append("<ul>" + "".join(f"<li>{inline_md(x)}</li>" for x in bullets) + "</ul>")
            bullets = []

    def flush_table():
        nonlocal table
        if table:
            out.append(table_to_html(table))
            table = []

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("|") and line.endswith("|"):
            flush_paragraph()
            flush_bullets()
            table.append(line)
            continue
        flush_table()
        if not line.strip():
            flush_paragraph()
            flush_bullets()
            continue
        if line.startswith("#"):
            flush_paragraph()
            flush_bullets()
            level = min(len(line) - len(line.lstrip("#")), 3)
            title = line[level:].strip()
            out.append(f"<h{level}>{inline_md(title)}</h{level}>")
            continue
        if line.startswith("- "):
            flush_paragraph()
            bullets.append(line[2:].strip())
            continue
        paragraph.append(line)
    flush_table()
    flush_paragraph()
    flush_bullets()
    return "\n".join(out)


def wrap_html(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
@page {{ size: A4; margin: 18mm 16mm; }}
body {{
  font-family: "Noto Sans CJK SC", "Noto Sans CJK", "SimSun", sans-serif;
  color: #17202a;
  font-size: 10.5pt;
  line-height: 1.62;
}}
h1 {{
  font-size: 23pt;
  margin: 0 0 14pt;
  padding-bottom: 8pt;
  border-bottom: 2px solid #2f5d8c;
  color: #12385f;
}}
h2 {{
  font-size: 15.5pt;
  margin: 20pt 0 7pt;
  color: #174d7c;
  break-after: avoid;
}}
h3 {{
  font-size: 12.5pt;
  margin: 12pt 0 5pt;
  color: #263f56;
}}
p {{ margin: 0 0 7pt; }}
ul {{ margin: 0 0 8pt 18pt; padding: 0; }}
li {{ margin: 0 0 3pt; }}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 8pt 0 12pt;
  font-size: 8.8pt;
  break-inside: avoid;
}}
th, td {{
  border: 0.6pt solid #b7c2cc;
  padding: 4pt 5pt;
  vertical-align: top;
}}
th {{
  background: #edf3f8;
  color: #12385f;
  font-weight: 700;
}}
code {{
  font-family: "Noto Sans Mono CJK SC", "Noto Sans Mono", monospace;
  background: #f3f5f7;
  padding: 0 2pt;
  border-radius: 2pt;
}}
a {{ color: #174d7c; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Markdown report to PDF using headless Google Chrome.")
    add_common_args(parser)
    parser.add_argument("--input", type=Path, default=project_root() / "docs" / "dataset_survey_zh.md")
    parser.add_argument("--output", type=Path, default=project_root() / "docs" / "dataset_survey_zh.pdf")
    parser.add_argument("--chrome", default="google-chrome")
    args = parser.parse_args()
    setup_logging(args.verbose)

    if not args.input.exists():
        logging.error("Input report does not exist: %s", args.input)
        return 2
    markdown = args.input.read_text(encoding="utf-8")
    title = markdown.splitlines()[0].lstrip("# ").strip() if markdown.splitlines() else "Dataset Report"
    body = markdown_to_html(markdown)
    rendered = wrap_html(title, body)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        html_path = Path(td) / "report.html"
        html_path.write_text(rendered, encoding="utf-8")
        cmd = [
            args.chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--print-to-pdf={args.output.resolve()}",
            str(html_path.resolve()),
        ]
        logging.info("Rendering PDF: %s", args.output)
        subprocess.run(cmd, check=True)
    logging.info("Wrote %s", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
