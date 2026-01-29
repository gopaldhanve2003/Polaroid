import json
from pathlib import Path
from typing import Dict, Any

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from core.base import StyleProcessor


class EffectProcessor:
    """
    Applies a JSON-defined film effect (look) to an image.

    EffectProcessor contains NO style values.
    All visual parameters must come from effect JSON.
    """

    EFFECTS_DIR = Path(__file__).parent.parent / "effects"

    def __init__(self, effect_name: str):
        if not effect_name:
            raise ValueError("effect_name is required")

        path = self.EFFECTS_DIR / f"{effect_name}.json"
        if not path.is_file():
            raise ValueError(f"Effect not found: {effect_name}")

        with open(path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self._validate_config(self.config)

    def apply(self, image: Image.Image) -> Image.Image:
        """
        Apply the effect pipeline to the given image.
        """
        for step in self.config["pipeline"]:
            image = self._apply_step(image, step)
        return image

    # ---------- validation ----------

    def _validate_config(self, config: Dict[str, Any]):
        if "pipeline" not in config or not isinstance(config["pipeline"], list):
            raise ValueError("Effect JSON must contain a 'pipeline' list")

        for i, step in enumerate(config["pipeline"]):
            if "op" not in step:
                raise ValueError(f"Pipeline step {i} is missing 'op'")

            op = step["op"]

            if op == "multiply_channel":
                self._require(step, i, "channel", "value")

            elif op in (
                "adjust_saturation",
                "adjust_contrast",
                "adjust_brightness",
            ):
                self._require(step, i, "value")

            elif op == "GaussianBlur":
                self._require(step, i, "radius")

            elif op == "grain":
                self._require(step, i, "intensity", "blend")

            elif op == "grayscale":
                pass

            else:
                raise ValueError(f"Unknown effect operation: {op}")

    def _require(self, step: Dict[str, Any], idx: int, *keys: str):
        for key in keys:
            if key not in step:
                raise ValueError(
                    f"Pipeline step {idx} ({step['op']}) requires '{key}'"
                )

    # ---------- execution ----------

    def _apply_step(self, image: Image.Image, step: Dict[str, Any]) -> Image.Image:
        op = step["op"]

        if op == "multiply_channel":
            return self._multiply_channel(
                image,
                step["channel"],
                step["value"],
            )

        if op == "adjust_saturation":
            return ImageEnhance.Color(image).enhance(step["value"])

        if op == "adjust_contrast":
            return ImageEnhance.Contrast(image).enhance(step["value"])

        if op == "adjust_brightness":
            return ImageEnhance.Brightness(image).enhance(step["value"])

        if op == "grayscale":
            return image.convert("L").convert("RGB")

        if op == "GaussianBlur":
            return image.filter(
                ImageFilter.GaussianBlur(step["radius"])
            )

        if op == "grain":
            return StyleProcessor.apply_grain(
                image,
                step["intensity"],
                step["blend"],
            )

        # unreachable due to validation
        raise ValueError(f"Unknown effect operation: {op}")

    # ---------- helpers ----------

    def _multiply_channel(
        self,
        image: Image.Image,
        channel: str,
        value: float,
    ) -> Image.Image:
        channel = channel.upper()
        if channel not in ("R", "G", "B"):
            raise ValueError(f"Invalid channel: {channel}")

        arr = np.asarray(image).astype("float32")
        idx = {"R": 0, "G": 1, "B": 2}[channel]

        arr[:, :, idx] *= float(value)
        arr = np.clip(arr, 0, 255)

        return Image.fromarray(arr.astype("uint8"))

