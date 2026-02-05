from PIL import Image, ImageDraw, ImageFilter
from core.base import StyleProcessor


class PolaroidFrame(StyleProcessor):

    def process(self):

        # ---------- Physical Aspects ----------
        DPI = 300

        # Half_4R
        PAGE_WIDTH = 76
        PAGE_HEIGHT = 102
        
        # # A6
        # PAGE_WIDTH = 105
        # PAGE_HEIGHT = 148
        
        WIDTH = int(PAGE_WIDTH * DPI / 25.4)
        HEIGHT = int(PAGE_HEIGHT * DPI / 25.4)

        fw, fh = WIDTH, HEIGHT

        ow, oh = self.image.size

        # ⭐ Border scale control (MAIN CONTROL)
        BORDER_SCALE = 0.7   # ↓ lower = bigger image

        # ⭐ Trim control
        PRINTER_BORDER_MM = 0
        trim = int(PRINTER_BORDER_MM * DPI / 25.4)

        # ---------- Base Polaroid ratios ----------
        base_side = 0.05
        base_top = 0.06
        base_bottom = 0.22

        # ---------- Apply scaling ----------
        side = int(fw * base_side * BORDER_SCALE)
        top = int(fh * base_top * BORDER_SCALE)
        min_bottom = int(fh * base_bottom * BORDER_SCALE)

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
        d = ImageDraw.Draw(shadow)

        offset = 3
        d.rectangle(
            [x + offset, y + offset, x + new_w + offset, y + new_h + offset],
            fill=(0, 0, 0, 40),
        )

        shadow = shadow.filter(ImageFilter.GaussianBlur(5))

        result = Image.alpha_composite(
            shadow,
            frame.convert("RGBA")
        ).convert("RGB")

        # ---------- Trim (NEW) ----------
        if trim > 0:
            result = result.crop(
                (trim, trim, fw - trim, fh - trim,)
            )

        return result


