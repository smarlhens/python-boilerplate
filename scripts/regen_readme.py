"""
Regenerate README.md from templates/README.md.j2.

Versions are read from the files that pin them, and command outputs come from
real runs, so the README cannot drift from the project. Run with --check to
fail (and print a diff) instead of writing when the README is out of date.
"""

import argparse
import difflib
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

from jinja2 import Environment, StrictUndefined, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
TEMPLATE = ROOT / "templates" / "README.md.j2"
# width of the redrawn coverage header (pytest's fallback when COLUMNS is unset
# and output is not a tty), so the README does not depend on the terminal
WIDTH = 80


def constraint(specifier: str) -> str:
    """Render a PEP 440 specifier set the way the README shows it: '>=1 <2'."""
    return " ".join(part.strip() for part in specifier.split(","))


def dev_dependency(pyproject: dict[str, Any], name: str) -> str:
    for requirement in pyproject["dependency-groups"]["dev"]:
        if match := re.fullmatch(rf"{re.escape(name)}\s*(.+)", requirement):
            return str(match[1])
    msg = f"no {name} in the dev dependency group"
    raise ValueError(msg)


def locked_version(name: str) -> str:
    with (ROOT / "uv.lock").open("rb") as f:
        lock = tomllib.load(f)
    for package in lock["package"]:
        if package["name"] == name:
            return str(package["version"])
    msg = f"no {name} in uv.lock"
    raise ValueError(msg)


def uv_version() -> str:
    dockerfile = (ROOT / "Dockerfile").read_text()
    match = re.search(r"ghcr\.io/astral-sh/uv:(\S+)", dockerfile)
    if match is None:
        msg = "no ghcr.io/astral-sh/uv image in Dockerfile"
        raise ValueError(msg)
    return str(match[1])


def run(*args: str) -> str:
    result = subprocess.run(  # noqa: S603 fixed argv, no shell
        [sys.executable, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        sys.exit(f"python {' '.join(args)} failed:\n{result.stdout}{result.stderr}")
    return result.stdout


def find(lines: list[str], pattern: str, start: int = 0) -> tuple[int, re.Match[str]]:
    for i in range(start, len(lines)):
        if match := re.search(pattern, lines[i]):
            return i, match
    msg = f"pytest output has no line matching {pattern!r}"
    raise ValueError(msg)


def pytest_outputs(output: str) -> tuple[str, str]:
    """
    Keep the compact parts of a `pytest tests --cov=src` run shown in the README.

    Returns the plain run output and the coverage run output: the plain run prints
    the same lines minus the coverage section. The platform is pinned to linux
    (where CI and the Docker image run) so the output does not depend on the
    machine that regenerates it.
    """
    lines = output.splitlines()
    _, collected = find(lines, r"collected \d+ items?")
    tests = [m[0] for line in lines if (m := re.match(r"\S+::\S+ [A-Z]+", line))]
    plain = [collected[0], "", *tests]

    start, coverage = find(lines, r"coverage: platform \S+, python (\S+)")
    end, _ = find(lines, r"^TOTAL", start)
    header = f" coverage: platform linux, python {coverage[1]} ".center(WIDTH, "_")
    table = [row for row in lines[start + 1 : end + 1] if row]
    return "\n".join(plain), "\n".join([*plain, "", header, *table])


def render(pytest_output: str) -> str:
    with (ROOT / "pyproject.toml").open("rb") as f:
        pyproject = tomllib.load(f)
    plain_output, cov_output = pytest_outputs(pytest_output)
    env = Environment(
        keep_trailing_newline=True,
        undefined=StrictUndefined,
        # markdown, not HTML: only escape .html/.xml templates, never string ones
        autoescape=select_autoescape(default_for_string=False),
    )
    template = env.from_string(TEMPLATE.read_text())
    return template.render(
        python_constraint=constraint(pyproject["project"]["requires-python"]),
        python_version=(ROOT / ".python-version").read_text().strip(),
        pre_commit_constraint=constraint(dev_dependency(pyproject, "pre-commit")),
        pre_commit_version=locked_version("pre-commit"),
        uv_constraint=constraint(pyproject["tool"]["uv"]["required-version"]),
        uv_version=uv_version(),
        pytest_output=plain_output,
        pytest_cov_output=cov_output,
        app_output=run("-m", "python_boilerplate.main").strip(),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail with a diff instead of writing when README.md is out of date",
    )
    parser.add_argument(
        "--pytest-output",
        type=Path,
        help="read the output of `pytest tests --cov=src` from this file "
        "instead of running the test suite again",
    )
    args = parser.parse_args()

    if args.pytest_output:
        pytest_output = args.pytest_output.read_text()
    else:
        pytest_output = run("-m", "pytest", "tests", "--cov=src")
    current = README.read_text()
    rendered = render(pytest_output)
    if current == rendered:
        return 0
    if args.check:
        sys.stdout.writelines(
            difflib.unified_diff(
                current.splitlines(keepends=True),
                rendered.splitlines(keepends=True),
                "README.md",
                "README.md (regenerated)",
            )
        )
        sys.stdout.flush()
        sys.stderr.write(
            "README.md is out of date: edit templates/README.md.j2, then run "
            "`uv run scripts/regen_readme.py` to update it.\n"
        )
        return 1
    README.write_text(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
