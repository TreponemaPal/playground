import argparse
from pathlib import Path
import sys

try:
    from pypdf import PdfMerger
except Exception:
    print("Missing dependency: pypdf. Install with: pip install pypdf")
    sys.exit(1)


def merge_pdfs(inputs: list[Path], output: Path) -> None:
    merger = PdfMerger()
    try:
        for pdf_path in inputs:
            if not pdf_path.exists():
                raise FileNotFoundError(f"Input file not found: {pdf_path}")
            if pdf_path.suffix.lower() != ".pdf":
                raise ValueError(f"Not a PDF file: {pdf_path}")
            merger.append(str(pdf_path))

        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("wb") as f:
            merger.write(f)
    finally:
        merger.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge multiple PDF files into one.")
    parser.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        help="Input PDF files in the order to merge.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output PDF file path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        merge_pdfs(args.inputs, args.output)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    print(f"Merged {len(args.inputs)} file(s) into: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
