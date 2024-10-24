import numpy as np
import SimpleITK as sitk
from typing import Optional
from readii.negative_controls.base import NegativeControl, T
from readii.negative_controls.enums import NegativeControlType, NegativeControlRegion
from readii.negative_controls.registry import NegativeControlRegistry

@NegativeControlRegistry.register(NegativeControlType.RANDOMIZED)
class RandomizedControl(NegativeControl):
    """Randomize the image."""
    def apply(
        self,
        baseImage: T,
        roiMask: Optional[T] = None,
        randomSeed: Optional[int] = None,
    ) -> T:
        # Set the random seed for the negative control
        self.random_seed = randomSeed

        # Define how the image will be randomized
        return self.apply_to_region(
            baseImage=baseImage,
            roiMask=roiMask,
            apply_func=self.randomize_image,
        )

    def randomize_image(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """Randomize the image.

        Parameters
        ----------
        image : sitk.Image or np.ndarray
            The base image to randomize.
        randomSeed : int, optional
            Seed for random number generation to ensure reproducibility. Default
            is None.

        Returns
        -------
        sitk.Image or np.ndarray
            The randomized image.
        """
        # Convert to array
        arrImage = self.to_array(image)

        # Set the random seed for np random generator
        randNumGen = np.random.default_rng(seed=self.random_seed)

        # Generate random array with same dimensions as baseImage with values
        # ranging from the minimum to maximum inclusive of the original image
        return randNumGen.integers(
            low=np.min(arrImage), high=np.max(arrImage), endpoint=True, size=arrImage.shape
        )
