#!/usr/bin/env python3
"""Assemble the prompt for a project, and plant it in its workspaces.

  bench/prompt.py ledger/python            print it
  bench/prompt.py --write ledger/python    write PROMPT.md into tdd/ and rtdd/
  bench/prompt.py --write                  ... for every project that has workspaces

The task text lives once per example and the stack constraint once per project, so
every stack of an example is driven by provably identical task wording. --write
carries that guarantee into the two workspaces: same bytes, same digest, so a session
starts by reading a file rather than by trusting a paste.
"""
import hashlib, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
VARIANTS = ("tdd", "rtdd")


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


def projects(root=ROOT):
    """Every project that has at least one checked-out workspace."""
    for stack in sorted((root / "examples").glob("*/*")):
        if any((stack / v).is_dir() for v in VARIANTS):
            yield f"{stack.parent.name}/{stack.name}"


def write(project, root=ROOT):
    """Plant the assembled prompt in each workspace. Returns (path, digest) pairs."""
    text = prompt(project, root)
    digest = hashlib.sha256(text.encode()).hexdigest()[:12]
    out = []
    for v in VARIANTS:
        ws = root / "examples" / project / v
        if not ws.is_dir():
            continue
        p = ws / "PROMPT.md"
        p.write_text(text)
        out.append((p.relative_to(root), digest))
    return out


def demo():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        (root / "examples/ex/proj").mkdir(parents=True)
        (root / "examples/ex/PROMPT.md").write_text("task line\n\n")
        (root / "examples/ex/proj/STACK.md").write_text("  stack line  \n")
        assert prompt("ex/proj", root) == "task line\n\nstack line\n"
        assert prompt("ex/proj/", root) == "task line\n\nstack line\n"
        for bad, want in (("ex", "expected <example>/<project>"), ("ex/absent", "STACK.md")):
            try:
                prompt(bad, root)
            except SystemExit as e:
                assert want in str(e), (bad, e)
            else:
                raise AssertionError(f"{bad!r} should have been rejected")

        # no workspaces yet: nothing to plant, and nothing claiming otherwise
        assert write("ex/proj", root) == []
        assert list(projects(root)) == []

        for v in VARIANTS:
            (root / "examples/ex/proj" / v).mkdir()
        planted = write("ex/proj", root)
        assert len(planted) == 2, planted
        bodies = [(root / "examples/ex/proj" / v / "PROMPT.md").read_bytes() for v in VARIANTS]
        assert bodies[0] == bodies[1], "the two variants must get identical bytes"
        assert bodies[0] == b"task line\n\nstack line\n"
        assert len({d for _, d in planted}) == 1, "one digest for the pair"
        assert list(projects(root)) == ["ex/proj"]

        # a changed stack line must reach both workspaces on the next write
        (root / "examples/ex/proj/STACK.md").write_text("other stack\n")
        write("ex/proj", root)
        assert all((root / "examples/ex/proj" / v / "PROMPT.md").read_text().endswith("other stack\n")
                   for v in VARIANTS)
    print("prompt.py ok")


def main(argv):
    if argv == ["--demo"]:
        return demo()
    if argv[:1] == ["--write"]:
        targets = argv[1:] or list(projects())
        if not targets:
            raise SystemExit("no project has a checked-out workspace")
        for t in targets:
            for path, digest in write(t) or [(None, None)]:
                print(f"{digest}  {path}" if path else f"-  {t}: no workspace checked out")
        return
    if len(argv) == 1:
        return sys.stdout.write(prompt(argv[0]))
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
