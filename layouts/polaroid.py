from PIL import Image, ImageDraw, ImageFilter
from core.base import StyleProcessor


class PolaroidFrame(StyleProcessor):
    """
    Fresh, just-printed Polaroid layout.
    Neutral baseline (not aged).
    """

    def process(self):
        ow, oh = self.image.size

        # --- Authentic Polaroid proportions (fresh print) ---
        side = int(ow * 0.06)
        top = int(ow * 0.06)
        bottom = int(oh * 0.19)

        fw = ow + side * 2
        fh = oh + top + bottom

        # --- Fresh Polaroid paper (clean, slightly warm) ---
        paper_color = (248, 247, 245)
        frame = Image.new("RGB", (fw, fh), paper_color)

        # Paste image
        frame.paste(self.image, (side, top))

        # --- Soft physical shadow (fresh print on surface) ---
        shadow = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
        d = ImageDraw.Draw(shadow)

        shadow_offset = 3
        d.rectangle(
            [
                side + shadow_offset,
                top + shadow_offset,
                side + ow + shadow_offset,
                top + oh + shadow_offset,
            ],
            fill=(0, 0, 0, 40),
        )

        shadow = shadow.filter(ImageFilter.GaussianBlur(5))

        # Composite: shadow under paper
        result = Image.alpha_composite(
            shadow,
            frame.convert("RGBA"),
        )

        return result.convert("RGB")

