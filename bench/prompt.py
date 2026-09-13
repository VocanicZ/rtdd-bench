#!/usr/bin/env python3
"""Print the exact prompt to paste for one project.

  bench/prompt.py ledger/python

The task text lives once per example and the stack constraint once per project, so
every stack of an example is driven by provably identical task wording.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def prompt(project, root=ROOT):
    example, _, stack = project.strip("/").partition("/")
    if not stack:
        raise SystemExit(f"expected <example>/<project>, got {project!r}")
    parts = [root / "examples" / example / "PROMPT.md",
             root / "examples" / example / stack / "STACK.md"]
    missing = [p for p in parts if not p.is_file()]
    if missing:
        raise SystemExit("missing " + ", ".join(str(p.relative_to(root)) for p in missing))
    return "\n\n".join(p.read_text().strip() for p in parts) + "\n"


def demo():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        (root / "examples/ex/proj").mkdir(parents=True)
        (root / "examples/ex/PROMPT.md").write_text("task line\n\n")
        (root / "examples/ex/proj/STACK.md").write_text("  stack line  \n")
        assert prompt("ex/proj", root) == "task line\n\nstack line\n"
        assert prompt("ex/proj/", root) == "task line\n\nstack line\n"
        try:
            prompt("ex", root)
        except SystemExit as e:
            assert "expected <example>/<project>" in str(e)
        else:
            raise AssertionError("bare example should be rejected")
        try:
            prompt("ex/absent", root)
        except SystemExit as e:
            assert "STACK.md" in str(e)
        else:
            raise AssertionError("missing stack should be rejected")
    print("prompt.py ok")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        demo()
    elif len(sys.argv) == 2:
        sys.stdout.write(prompt(sys.argv[1]))
    else:
        sys.exit(__doc__)
