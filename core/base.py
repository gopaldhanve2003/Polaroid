from abc import ABC, abstractmethod
from PIL import Image
import numpy as np


class StyleProcessor(ABC):
    """
    Abstract base class for image style processors.

    Used for layout transforms (e.g. Polaroid)
    and shared style utilities.
    """

    def __init__(self, image: Image.Image):
        if not isinstance(image, Image.Image):
            raise TypeError("image must be a PIL.Image instance")

        # Keep reference explicit and predictable
        self.image = image

    @abstractmethod
    def process(self) -> Image.Image:
        """
        Apply processing and return the resulting image.
        """
        raise NotImplementedError

    @staticmethod
    def apply_grain(
        image: Image.Image,
        intensity: float = 5,
        blend: float = 0.03,
    ) -> Image.Image:
        """
        Apply film grain using Gaussian noise.

        Args:
            image: Input RGB image
            intensity: Noise strength
            blend: Blend ratio between image and grain

        Returns:
            PIL.Image with grain applied
        """
        width, height = image.size
        noise = np.random.normal(0, intensity, (height, width, 3))
        noise = np.clip(128 + noise, 0, 255).astype("uint8")
        grain = Image.fromarray(noise)
        return Image.blend(image, grain, blend)

