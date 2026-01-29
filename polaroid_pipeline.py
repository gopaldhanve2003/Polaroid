import os
from PIL import Image

from core.effect_processor import EffectProcessor
from layouts.polaroid import PolaroidFrame


class PolaroidPipeline:
    def __init__(self, input_path: str):
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input image not found: {input_path}")

        image = Image.open(input_path)
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        self.image = image

    def apply_style(self, effect: str | None, output_path: str):
        """
        Apply a Polaroid-style transformation.

        - effect: optional film effect (JSON-defined)
        - output_path: destination file path

        Polaroid layout is always applied.
        """
        # work on a copy to avoid accidental reuse side-effects
        img = self.image.copy()

        # apply film effect (optional)
        if effect:
            img = EffectProcessor(effect).apply(img)

        # always apply Polaroid layout
        img = PolaroidFrame(img).process()

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        img.save(
            output_path,
            format="JPEG",
            quality=95,
            optimize=True,
            progressive=True,
        )

