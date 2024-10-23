"""Negative controls for radiomics analysis.

This module defines the abstract base class (ABC) for all negative controls
used in radiomics analysis. The `NegativeControl` class serves as a blueprint
for creating different types of negative controls, enforcing a consistent
interface across implementations.

Each negative control must implement the `apply` method, which is responsible
for applying the specific transformation to the given image, based on the type
of negative control.

This design ensures that the system remains extensible, allowing developers to
easily add new types of negative controls by subclassing `NegativeControl` and
implementing the `apply` method.

Type Generics
-------------
The class leverages Python Type Generics to allow handling different input types,
such as `sitk.Image` or `np.ndarray`. This enables seamless operation regardless
of the specific input format, ensuring flexibility and compatibility.

Classes
-------
NegativeControl : ABC
    Abstract base class that defines the interface for all negative controls.
"""

from abc import ABC, abstractmethod
from typing import Callable, Optional, TypeVar, Union

import numpy as np
import SimpleITK as sitk

from readii.negative_controls.enums import NegativeControlRegion, NegativeControlType

T = TypeVar("T", sitk.Image, np.ndarray)


class NegativeControl(ABC):
    """Abstract base class for defining negative controls.

    Subclasses must implement the `apply` method, which applies a specific
    negative control to a given image. This design ensures that all negative
    controls conform to a consistent interface.

    Attributes
    ----------
    control_type : Union[NegativeControlType, str]
        The type of negative control (e.g., SHUFFLED, RANDOMIZED).
    control_region : NegativeControlRegion
        The region to apply the control to (e.g., FULL, ROI, NON_ROI).

    Methods
    -------
    apply(baseImage, roiMask=None, randomSeed=None)
        Apply the negative control to the image.
    """

    def __init__(
        self,
        control_type: Union[NegativeControlType, str],
        control_region: NegativeControlRegion,
    ) -> None:
        """Initialize the negative control with type and region.

        Parameters
        ----------
        control_type : NegativeControlType
            Type of negative control (e.g., SHUFFLED, RANDOMIZED).
        control_region : NegativeControlRegion
            Region to apply the control (e.g., FULL, ROI, NON_ROI).
        """
        self.control_type = control_type
        self.control_region = control_region

    @abstractmethod
    def apply(
        self,
        baseImage: T,
        roiMask: Optional[T] = None,
        randomSeed: Optional[int] = None,
    ) -> T:
        """Apply the negative control to the image.

        Parameters
        ----------
        baseImage : sitk.Image or np.ndarray
            The base image to which the negative control will be applied.
        roiMask : sitk.Image or np.ndarray, optional
            Mask for the region of interest (ROI) if the negative control should
            be applied to specific regions of the image. Default is None.
        randomSeed : int, optional
            Seed for random number generation to ensure reproducibility. Default
            is None.

        Returns
        -------
        sitk.Image or np.ndarray
            The image with the negative control applied.
        """
        pass

    def to_array(self, input_data: Union[sitk.Image, np.ndarray]) -> np.ndarray:
        """Convert a SimpleITK Image to numpy array if needed, else return the array.

        Parameters
        ----------
        input_data : sitk.Image or np.ndarray
            The input data to convert.

        Returns
        -------
        np.ndarray
            The numpy array version of the input data.
        """
        if isinstance(input_data, sitk.Image):
            return sitk.GetArrayFromImage(input_data)
        return input_data

    def _apply_to_roi_or_full(
        self,
        baseImage: T,
        roiMask: Optional[T],
        apply_func: Callable[[np.ndarray], np.ndarray],
    ) -> T:
        """Apply a function to either the full image or a specific ROI based on control_region.

        Parameters
        ----------
        baseImage : sitk.Image or np.ndarray
            The base image on which the function will be applied.
        roiMask : sitk.Image or np.ndarray, optional
            The ROI mask. If None, the function is applied to the full image.
        apply_func : callable
            The function that defines how to apply the transformation.

        Returns
        -------
        sitk.Image or np.ndarray
            The transformed image.
        """
        base_array = self.to_array(baseImage)

        if self.control_region == NegativeControlRegion.FULL or roiMask is None:
            # Apply the function to the full image.
            transformed_array = apply_func(base_array)
        else:
            # Convert ROI mask and base image to arrays
            mask_array = self.to_array(roiMask)

            # Apply transformation only within the mask or outside of the mask based on region
            transformed_array = np.copy(base_array)
            mask_indices = np.nonzero(mask_array)

            if self.control_region == NegativeControlRegion.ROI:
                transformed_array[mask_indices] = apply_func(base_array[mask_indices])
            elif self.control_region == NegativeControlRegion.NON_ROI:
                non_mask_indices = np.nonzero(~mask_array)
                transformed_array[non_mask_indices] = apply_func(base_array[non_mask_indices])
            else:
                raise ValueError("Unsupported control region specified.")

        if isinstance(baseImage, sitk.Image):
            transformed_image = sitk.GetImageFromArray(transformed_array)
            transformed_image.CopyInformation(baseImage)
            return transformed_image

        return transformed_array
