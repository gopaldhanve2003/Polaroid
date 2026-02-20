from PIL import Image, ImageDraw, ImageFilter
from core.base import StyleProcessor


PAPER_SIZES_MM = {
    "half_4r": (76, 102),
    "a6": (105, 148),
}

DEFAULT_PAPER_SIZE = "half_4r"

# Keep frame feel consistent across supported print sizes.
# Values are ratios of frame width/height.
FRAME_RATIOS = {
    "half_4r": {
        "border_scale": 0.74,
        "side": 0.053,
        "top": 0.065,
        "bottom": 0.225,
    },
    "a6": {
        "border_scale": 0.70,
        "side": 0.050,
        "top": 0.062,
        "bottom": 0.215,
    },
}


def get_supported_paper_sizes():
    return tuple(PAPER_SIZES_MM.keys())


class PolaroidFrame(StyleProcessor):
    def __init__(self, image, paper_size: str = DEFAULT_PAPER_SIZE):
        super().__init__(image)

        if paper_size not in PAPER_SIZES_MM:
            supported = ", ".join(get_supported_paper_sizes())
            raise ValueError(
                f"Unsupported paper_size '{paper_size}'. "
                f"Supported paper sizes: {supported}"
            )

        if paper_size not in FRAME_RATIOS:
            supported = ", ".join(FRAME_RATIOS.keys())
            raise ValueError(
                f"Missing FRAME_RATIOS profile for '{paper_size}'. "
                f"Configured profiles: {supported}"
            )

        self.paper_size = paper_size

    def process(self):

        # ---------- Physical Aspects ----------
        DPI = 300

        page_width_mm, page_height_mm = PAPER_SIZES_MM[self.paper_size]

        fw = int(page_width_mm * DPI / 25.4)
        fh = int(page_height_mm * DPI / 25.4)

        ow, oh = self.image.size

        # ---------- Frame profile by paper size ----------
        profile = FRAME_RATIOS[self.paper_size]
        border_scale = profile["border_scale"]

        side = int(fw * profile["side"] * border_scale)
        top = int(fh * profile["top"] * border_scale)
        min_bottom = int(fh * profile["bottom"] * border_scale)

        # ---------- Trim control ----------
        printer_border_mm = 0
        trim = int(printer_border_mm * DPI / 25.4)

        # ---------- Fit image ----------
        max_w = fw - side * 2
        max_h = fh - top - min_bottom

        scale = min(max_w / ow, max_h / oh)

        new_w = int(ow * scale)
        new_h = int(oh * scale)

        resized = self.image.resize((new_w, new_h), Image.LANCZOS)

        # ---------- Center image ----------
        x = (fw - new_w) // 2
        y = top

        frame = Image.new("RGB", (fw, fh), (255, 255, 255))
        frame.paste(resized, (x, y))

        # ---------- Shadow ----------
        shadow = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
        draw = ImageDraw.Draw(shadow)

        shadow_offset = 3
        draw.rectangle(
            [
                x + shadow_offset,
                y + shadow_offset,
                x + new_w + shadow_offset,
                y + new_h + shadow_offset,
            ],
            fill=(0, 0, 0, 40),
        )

        shadow = shadow.filter(ImageFilter.GaussianBlur(5))

        result = Image.alpha_composite(
            shadow,
            frame.convert("RGBA")
        ).convert("RGB")

        if trim > 0:
            result = result.crop((trim, trim, fw - trim, fh - trim))

        return result
