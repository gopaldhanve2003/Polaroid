import os
import random

from polaroid_pipeline import PolaroidPipeline
from registry import EFFECTS

SUPPORTED_EXTS = (".jpg", ".jpeg", ".png")


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def _output_path(input_image, output_dir, effect=None):
    name = os.path.splitext(os.path.basename(input_image))[0]
    suffix = effect if effect else "polaroid_classic"
    return os.path.join(output_dir, f"{name}_{suffix}.jpg")


def generate_styles(
    effects=None,
    input_image=None,
    output_dir="images/output",
    dry_run=False,
    paper_size="half_4r",
):
    if not input_image:
        raise ValueError("input_image is required")

    if effects:
        bad = [e for e in effects if e not in EFFECTS]
        if bad:
            raise ValueError(f"Unknown effects: {', '.join(bad)}")

    _ensure_dir(output_dir)
    pipeline = None if dry_run else PolaroidPipeline(input_image, paper_size=paper_size)

    # No effect = Polaroid Classic
    if not effects:
        out = _output_path(input_image, output_dir)
        print(
            f"[DRY-RUN] {input_image} -> {out}"
            if dry_run
            else f"Generating {out}"
        )
        if not dry_run:
            pipeline.apply_style(None, out)
        return

    for effect in effects:
        out = _output_path(input_image, output_dir, effect)
        print(
            f"[DRY-RUN] {input_image} -> {out}"
            if dry_run
            else f"Generating {out}"
        )
        if not dry_run:
            pipeline.apply_style(effect, out)


def generate_all_combinations(input_image, output_dir, dry_run=False, paper_size="half_4r"):

    generate_styles(
        effects=EFFECTS,
        input_image=input_image,
        output_dir=output_dir,
        dry_run=dry_run,
        paper_size=paper_size,
    )


def generate_random_combinations(
    n,
    input_image,
    output_dir,
    dry_run=False,
    paper_size="half_4r",
):
    if n > len(EFFECTS):
        n = len(EFFECTS)

    effects = random.sample(EFFECTS, n)

    generate_styles(
        effects=effects,
        input_image=input_image,
        output_dir=output_dir,
        dry_run=dry_run,
        paper_size=paper_size,
    )


def batch_process(
    input_dir,
    effects,
    output_dir,
    dry_run=False,
    paper_size="half_4r",
):
    if not os.path.isdir(input_dir):
        raise ValueError(f"Invalid input directory: {input_dir}")

    images = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(SUPPORTED_EXTS)
    ]

    if not images:
        raise ValueError("No supported images found in input directory")

    for img in images:
        generate_styles(
            effects=effects,
            input_image=img,
            output_dir=output_dir,
            dry_run=dry_run,
            paper_size=paper_size,
        )

