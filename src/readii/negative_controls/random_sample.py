import numpy as np
import SimpleITK as sitk
from typing import Optional
from readii.negative_controls.base import NegativeControl, T
from readii.negative_controls.enums import NegativeControlType, NegativeControlRegion
from readii.negative_controls.registry import NegativeControlRegistry

@NegativeControlRegistry.register(NegativeControlType.RANDOMIZED_SAMPLED)
class RandomizedSampledControl(NegativeControl):
    """Randomly Sample all the pixel values."""

    def apply(
        self,
        baseImage: T,
        roiMask: Optional[T] = None,
        randomSeed: Optional[int] = None,
    ) -> T:
        """Apply the negative control to the image."""
        # Set the random seed for the negative control
        self.random_seed = randomSeed

        # Define how the image will be randomized
        return self.apply_to_region(
            baseImage=baseImage,
            roiMask=roiMask,
            apply_func=self.random_sample_image,
        )

    def random_sample_image(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """Randomly sample all the pixel values.

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
        # Check if baseImage is a sitk.Image or np.ndarray
        arrImage = self.to_array(image)

        # Get array dimensions to reshape back to
        imgDimensions = arrImage.shape

        # Flatten the 3D array to 1D so values can be shuffled
        flatArrImage = arrImage.flatten()

        # Set the random seed for np random number generator
        randNumGen = np.random.default_rng(seed=self.random_seed)

        # Randomly sample values for new array from original image distribution
        sampled_array = randNumGen.choice(flatArrImage, size=len(flatArrImage), replace=True)

        # Reshape the array back into the original image dimensions
        return np.reshape(sampled_array, imgDimensions)
