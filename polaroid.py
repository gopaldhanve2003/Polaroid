import argparse
import sys

from engine import (
    generate_styles,
    generate_all_combinations,
    generate_random_combinations,
    batch_process,
)
from tools.compress import compress_images
from registry import list_effects
from layouts.polaroid import PAPER_SIZES_MM


def build_parser():
    parser = argparse.ArgumentParser(
        prog="polaroid",
        description="Polaroid image generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # input / output
    parser.add_argument("--input", help="Input image path")
    parser.add_argument("--input-dir", help="Input directory (batch mode)")
    parser.add_argument(
        "--output",
        default="images/output",
        help="Output directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing files",
    )

    # listing
    parser.add_argument("--list-effects", action="store_true")
    parser.add_argument("--list-paper-sizes", action="store_true")

    # generation options
    gen = parser.add_argument_group("generation options")
    gen.add_argument(
        "-e",
        "--effects",
        nargs="*",
        help="Film effects to apply (default: polaroid_classic)",
    )
    gen.add_argument("-a", "--all", action="store_true")
    gen.add_argument("-r", "--random", type=int)
    gen.add_argument(
        "--paper-size",
        choices=tuple(PAPER_SIZES_MM.keys()),
        default="half_4r",
        help="Paper size for the Polaroid frame",
    )

    # tools
    tools = parser.add_argument_group("tools")
    tools.add_argument("-c", "--compress", help="Directory to compress images")
    tools.add_argument("-q", "--quality", type=int, default=70)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        available_effects = set(list_effects())

        # ---- listing ----
        if args.list_effects:
            print("Available effects:")
            for e in available_effects:
                print(f"  - {e}")
            return

        if args.list_paper_sizes:
            print("Available paper sizes:")
            for name, (w, h) in PAPER_SIZES_MM.items():
                print(f"  - {name}: {w}mm x {h}mm")
            return

        # ---- tools ----
        if args.compress:
            compress_images(args.compress, args.quality, args.output)
            return

        # ---- validation ----
        if args.input and args.input_dir:
            raise ValueError("Use either --input or --input-dir, not both")

        if not args.input and not args.input_dir:
            raise ValueError("Either --input or --input-dir is required")

        if args.effects:
            bad = [e for e in args.effects if e not in available_effects]
            if bad:
                raise ValueError(
                    f"Unknown effects: {', '.join(bad)}. "
                    f"Use --list-effects to see available options."
                )

        # ---- batch mode ----
        if args.input_dir:
            batch_process(
                input_dir=args.input_dir,
                effects=args.effects,
                output_dir=args.output,
                dry_run=args.dry_run,
                paper_size=args.paper_size,
            )
            return

        # ---- single image ----
        if args.all:
            generate_all_combinations(
                args.input,
                args.output,
                args.dry_run,
                args.paper_size,
            )
            return

        if args.random:
            generate_random_combinations(
                args.random,
                args.input,
                args.output,
                args.dry_run,
                args.paper_size,
            )
            return

        generate_styles(
            effects=args.effects,
            input_image=args.input,
            output_dir=args.output,
            dry_run=args.dry_run,
            paper_size=args.paper_size,
        )

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

