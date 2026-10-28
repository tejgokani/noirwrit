"""noirwrit command line entry point."""

from __future__ import annotations

import argparse
import sys

from noirwrit import __version__


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="noirwrit", description="Offline crime and noir chapter generator.")
    p.add_argument("--version", action="version", version=f"noirwrit {__version__}")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("info", help="show config and paths")
    a = p.parse_args(argv)
    if a.cmd == "info":
        from noirwrit.config import load_requirements

        print(load_requirements())
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
