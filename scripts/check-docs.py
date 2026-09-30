#!/usr/bin/env python3
"""Checks that what the docs tell a reader to do can be done. Every relative link,
heading anchor, image, repo path, script and flag named in a Markdown file must exist."""

import os
import re
import subprocess
import sys

ROOT = os.environ.get(
    "DOCS_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
TOP = (
    "docs",
    "data",
    "scripts",
    "agent-os",
    "references",
    "templates",
    "assets",
    ".github",
)
PATH_RE = re.compile(
    r"(?<![\w./~-])((?:%s)/[A-Za-z0-9_./-]*[A-Za-z0-9_-]\.[a-z]{2,5})(?![\w/-])"
    % "|".join(re.escape(t) for t in TOP)
)
LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_SRC_RE = re.compile(r"<img[^>]+src=\"([^\"]+)\"")
CMD_RE = re.compile(
    r"(?:python3|bash)\s+((?:~/[\w./-]*/)?(scripts/[\w.-]+\.(?:py|sh)))((?:\s+[^\s|;&<>`]+)*)"
)
FLAG_RE = re.compile(r"(?<!\S)(--[a-z][a-z0-9-]*)")


def markdown_files():
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith(".md"):
                out.append(os.path.join(base, name))
    return sorted(out)


def slug(heading):
    text = re.sub(r"[`*_]|<[^>]+>", "", heading).strip().lower()
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path, cache={}):
    if path not in cache:
        found, seen, fenced = set(), {}, False
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.lstrip().startswith("```"):
                    fenced = not fenced
                match = None if fenced else re.match(r"#{1,6}\s+(.*)", line)
                if match:
                    base = slug(match.group(1))
                    n = seen.get(base, 0)
                    seen[base] = n + 1
                    found.add(base if n == 0 else f"{base}-{n}")
        cache[path] = found
    return cache[path]


def flags_of(script, cache={}):
    if script not in cache:
        with open(os.path.join(ROOT, script), encoding="utf-8") as f:
            cache[script] = f.read()
    return cache[script]


def check_file(path):
    problems = []
    rel = os.path.relpath(path, ROOT)
    here = os.path.dirname(path)
    generated = rel.startswith("references" + os.sep)
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for number, line in enumerate(lines, 1):
        where = f"{rel}:{number}"
        targets = [m.group(2) for m in LINK_RE.finditer(line)] + HTML_SRC_RE.findall(
            line
        )
        for target in targets:
            if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("//"):
                continue
            file_part, _, anchor = target.partition("#")
            dest = (
                path
                if not file_part
                else os.path.normpath(os.path.join(here, file_part))
            )
            if not os.path.exists(dest):
                problems.append(f"{where} links to {target}, which does not exist")
            elif (
                anchor and dest.endswith(".md") and anchor.lower() not in anchors(dest)
            ):
                problems.append(
                    f"{where} links to #{anchor}, no such heading in {os.path.relpath(dest, ROOT)}"
                )
        if generated:
            continue
        for match in PATH_RE.finditer(line):
            named = match.group(1)
            if "*" in named or "<" in named:
                continue
            if not os.path.exists(os.path.join(ROOT, named)):
                problems.append(f"{where} names {named}, which does not exist")
        for match in CMD_RE.finditer(line):
            script = match.group(2)
            if not os.path.exists(os.path.join(ROOT, script)):
                continue
            source = flags_of(script)
            for flag in FLAG_RE.findall(match.group(3)):
                if flag not in source:
                    problems.append(
                        f"{where} runs {script} with {flag}, which the script does not accept"
                    )
    return problems


def main():
    problems = []
    files = markdown_files()
    for path in files:
        problems.extend(check_file(path))
    syntax = subprocess.run(
        ["bash", "-n", os.path.join(ROOT, "scripts", "install.sh")], capture_output=True
    )
    if (
        os.path.exists(os.path.join(ROOT, "scripts", "install.sh"))
        and syntax.returncode != 0
    ):
        problems.append("scripts/install.sh does not parse")
    for problem in problems:
        print(problem)
    print(f"check-docs. {len(files)} files, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
