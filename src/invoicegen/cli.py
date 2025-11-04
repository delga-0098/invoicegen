from __future__ import annotations
import argparse
from importlib.metadata import version, PackageNotFoundError

PKG = "invoicegen"

def get_version() -> str:
    try:
        return version(PKG)
    except PackageNotFoundError:
        return "0.0.1+dev"

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="invoicegen",
        description="Generate invoices from job data.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {get_version()}")

    subparsers = parser.add_subparsers(dest="command", required=False)

    validate_p = subparsers.add_parser("validate", help="Validate input data files.")
    validate_p.add_argument("--in", dest="in_file", required=False, help="Path to input file")

    preview_p = subparsers.add_parser("preview", help="Render HTML preview (no PDF).")
    preview_p.add_argument("--in", dest="in_file", required=False, help="Path to input file")

    render_p = subparsers.add_parser("render", help="Render PDFs per unit.")
    render_p.add_argument("--in", dest="in_file", required=False, help="Path to input file")
    render_p.add_argument("--out", dest="out_dir", required=False, help="Output directory")

    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    print(f"[invoicegen] command={args.command} (skeleton)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())