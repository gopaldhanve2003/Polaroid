from PIL import Image
import os


def compress_images(input_dir: str, quality: int = 70, output_dir: str = None):
    """
    Compress all JPG/PNG images in a directory.

    Args:
        input_dir: Directory containing images
        quality: JPEG quality (1–100)
        output_dir: Directory to save compressed images.
                    If not provided, a `compressed` subdir is created.
    """
    if not input_dir or not os.path.isdir(input_dir):
        raise ValueError(f"Invalid directory: {input_dir}")

    if not (1 <= quality <= 100):
        raise ValueError("quality must be between 1 and 100")

    if not output_dir:
        output_dir = os.path.join(input_dir, "compressed")

    os.makedirs(output_dir, exist_ok=True)

    for name in os.listdir(input_dir):
        path = os.path.join(input_dir, name)

        if not os.path.isfile(path):
            continue

        if not name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        with Image.open(path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")

            output_path = os.path.join(output_dir, os.path.splitext(name)[0] + ".jpg")
            img.save(
                output_path,
                format="JPEG",
                quality=quality,
                optimize=True,
                progressive=True,
            )

