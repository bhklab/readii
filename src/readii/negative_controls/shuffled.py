import numpy as np
import SimpleITK as sitk
from typing import Optional
from readii.negative_controls.base import NegativeControl, T
from readii.negative_controls.enums import NegativeControlType, NegativeControlRegion
from readii.negative_controls.registry import NegativeControlRegistry

###############################################################################
# EXAMPLES


# This is how it would be defined in the library, using the enums
@NegativeControlRegistry.register(NegativeControlType.SHUFFLED)
class ShuffledControl(NegativeControl):
    """Shuffle the image."""

    def apply(
        self, baseImage: T, roiMask: Optional[T] = None, randomSeed: Optional[int] = None
    ) -> T:
        # Set the random seed for the negative control
        self.random_seed = randomSeed

        # Define how the image will be shuffled
        return self.apply_to_region(
            baseImage=baseImage,
            roiMask=roiMask,
            apply_func=self.shuffle_image,
        )

    def shuffle_image(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """Shuffle the image.

        Parameters
        ----------
        image : sitk.Image or np.ndarray
            The base image to shuffle.
        randomSeed : int, optional
            Seed for random number generation to ensure reproducibility. Default
            is None.

        Returns
        -------
        sitk.Image or np.ndarray
            The shuffled image.
        """
        # Convert to array

        # # Check if baseImage is a sitk.Image or np.ndarray
        arrImage = self.to_array(image)

        # Get array dimensions to reshape back to
        imgDimensions = arrImage.shape

        # Flatten the 3D array to 1D so values can be shuffled
        flatArrImage = arrImage.flatten()

        # Set the random seed for np random generator
        randNumGen = np.random.default_rng(seed=self.random_seed)

        # Shuffle the flat array
        randNumGen.shuffle(flatArrImage)

        # Reshape the array back into the original image dimensions
        shuffled3DArrImage = np.reshape(flatArrImage, imgDimensions)

        return shuffled3DArrImage
