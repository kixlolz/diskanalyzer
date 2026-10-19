"""Entrypoint — plain table mode or TUI."""
import argparse
import sys
from .scanner import scan, human
from .tui import run_tui


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="diskanalyzer")
    p.add_argument("path", nargs="?", default=".", help="Directory to scan")
    p.add_argument("--depth", type=int, default=32)
    p.add_argument("--plain", action="store_true", help="Skip TUI, print table")
    p.add_argument("--top", type=int, default=10, help="Rows in plain mode")
    args = p.parse_args(argv)

    if not sys.stdout.isatty():
        args.plain = True

    if args.plain:
        node = scan(args.path, max_depth=args.depth)
        node.sort_recursive()
        print(f"{human(node.size):>10}  {node.path}")
        for child in node.children[: args.top]:
            print(f"{human(child.size):>10}  {child.path}")
        return 0

    run_tui(args.path)
    return 0


if __name__ == "__main__":
    sys.exit(main())