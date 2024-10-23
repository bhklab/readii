"""Factory for creating instances of registered Negative Controls."""

from typing import List, Union

from readii.negative_controls.base import NegativeControl
from readii.negative_controls.enums import NegativeControlRegion, NegativeControlType
from readii.negative_controls.registry import NegativeControlRegistry

class NegativeControlFactory:
    """Factory for creating instances of Negative Controls.

    The factory uses the NegativeControlRegistry to dynamically instantiate
    NegativeControl objects based on the provided type and region.

    Methods
    -------
    create(
      control_type: Union[NegativeControlType, str],
      control_region: NegativeControlRegion,
    ) -> NegativeControl
        Create an instance of the appropriate NegativeControl subclass.
    """

    @staticmethod
    def create(
        control_type: Union[NegativeControlType, str], control_region: NegativeControlRegion
    ) -> NegativeControl:
        """Create an instance of the appropriate NegativeControl subclass.

        Parameters
        ----------
        control_type : Union[NegativeControlType, str]
            The type of negative control to instantiate (e.g., SHUFFLED, "custom_noise").
        control_region : NegativeControlRegion
            The region where the control will be applied (e.g., FULL, ROI, NON_ROI).

        Returns
        -------
        NegativeControl
            An instance of the corresponding NegativeControl subclass.

        Raises
        ------
        ValueError
            If the specified control type is not registered.
        """
        # Retrieve the control class from the registry.
        control_class = NegativeControlRegistry.get_control(control_type)

        if not control_class:
            raise ValueError(f"Control type '{control_type}' is not registered.")

        # Instantiate and return the control.
        return control_class(control_type, control_region)

    @staticmethod
    def create_all(
        nc_types: List[str],
    ) -> List[NegativeControl]:
        """Create multiple registered NegativeControl instances.

        Given a list of control types defined by concatenating the NegativeControlType enum
        with a string, this function will dynamically create instances of the appropriate
        `NegativeControl` subclasses.

        i.e ["randomized.full", "randomized.non_roi", "shuffled.full", "randomized_sampled.full"]
        will create instances of
          RandomizedControl with region FULL,
          RandomizedControl with region NON_ROI,
          ShuffledControl with region FULL,
          RandomizedSampledControl with region FULL

        Parameters
        ----------
        nc_types : List[str]
            A list of control types to instantiate.
            Each type should be defined by concatenating the NegativeControlType enum with
            a string OR a custom string that is not defined in the enum.

        Returns
        -------
        List[NegativeControl]
            A list of instantiated NegativeControl objects.

        """
        # Create an empty list to store the instantiated controls.
        controls = []

        # Iterate over the list of control types.
        for nc in nc_types:
            # Split the type into the control type and region.
            control_type, region = nc.split(".")

            if NegativeControlRegion(region) is None:
                raise ValueError(
                    f"Invalid region '{region}'. "
                    f"Must be one of {[e.name for e in NegativeControlRegion]}"
                )

            # Create the control instance.
            control: NegativeControl = NegativeControlFactory.create(
                control_type=control_type,
                control_region=NegativeControlRegion(region),
            )

            # Add the control to the list.
            controls.append(control)

        return controls
