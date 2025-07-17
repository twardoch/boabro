# this_file: src/boabro/__main__.py
"""CLI entry point for boabro."""

import sys
import argparse
import json
from pathlib import Path

from .boabro import analyze_font_data
from . import __version__


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Boabro - Browser-based font analysis tools"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"boabro {__version__}"
    )
    parser.add_argument(
        "font_file",
        help="Font file to analyze (TTF, OTF, WOFF, WOFF2)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    # Check if font file exists
    font_path = Path(args.font_file)
    if not font_path.exists():
        print(f"Error: Font file '{font_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Analyze font
    try:
        if args.verbose:
            print(f"Analyzing font: {font_path}", file=sys.stderr)

        with open(font_path, "rb") as f:
            font_bytes = f.read()

        result = analyze_font_data(font_bytes, font_path.name)

        # Format output
        if args.format == "json":
            output = json.dumps(result, indent=2)
        else:
            output = format_text_output(result, args.verbose)

        # Write output
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            if args.verbose:
                print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(output)

    except Exception as e:
        print(f"Error analyzing font: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def format_text_output(result: dict, verbose: bool = False) -> str:
    """Format analysis result as human-readable text."""
    lines = []

    # Basic info
    lines.append(f"Font Analysis: {result['fileName']}")
    lines.append("=" * 50)
    lines.append(f"Family Name: {result['familyName']}")
    lines.append(f"Subfamily: {result['subfamily']}")
    lines.append(f"Full Name: {result['fullName']}")
    lines.append(f"PostScript Name: {result['psName']}")
    lines.append(f"Version: {result['version']}")
    lines.append("")

    # Metrics
    lines.append("Metrics:")
    lines.append(f"  Units per EM: {result['upm']}")
    lines.append(f"  Number of glyphs: {result['numGlyphs']}")
    lines.append("")

    # Tables
    lines.append(f"OpenType tables ({len(result['tables'])}):")
    for i, table in enumerate(result["tables"]):
        lines.append(f"  {i+1:2d}. {table}")
    lines.append("")

    # Additional info if verbose
    if verbose:
        lines.append("Additional Information:")
        lines.append(f"  Manufacturer: {result.get('manufacturer', 'N/A')}")
        lines.append(f"  Designer: {result.get('designer', 'N/A')}")
        lines.append(f"  License: {result.get('license', 'N/A')}")
        lines.append(f"  Trademark: {result.get('trademark', 'N/A')}")
        lines.append("")

        # Name records count
        name_records = result.get("nameTableRecords", [])
        lines.append(f"Name table records: {len(name_records)}")

        # Show some name records
        if name_records:
            lines.append("Sample name records:")
            for i, record in enumerate(name_records[:10]):  # Show first 10
                lines.append(f"  {record['nameID']:2d}: {record['string']}")
            if len(name_records) > 10:
                lines.append(f"  ... and {len(name_records) - 10} more")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
