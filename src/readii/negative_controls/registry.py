"""Registry for managing and instantiating Negative Control types."""

from typing import Callable, ClassVar, Dict, List, Type, Union

from readii.negative_controls.base import NegativeControl
from readii.negative_controls.enums import NegativeControlType

class NegativeControlRegistry:
    """Singleton registry to keep track of all available NegativeControl types.

    The registry allows for easy integration and extension by using the
    `register_control` decorator to add new negative controls.

    Methods
    -------
    register(control_type: Union[NegativeControlType, str]) -> Callable:
        Decorator to register a NegativeControl subclass.
    get_control(control_type: Union[NegativeControlType, str]) -> Type[NegativeControl]:
        Retrieve a registered NegativeControl subclass.
    """

    _registry: ClassVar[Dict[str, Type[NegativeControl]]] = {}

    @classmethod
    def register(
        cls: Type["NegativeControlRegistry"],
        control_type: Union[NegativeControlType, str],
    ) -> Callable[..., Type[NegativeControl]]:
        """Register a NegativeControl subclass.

        This is a decorator function that takes a subclass of NegativeControl
        and registers it with the specified control type.

        Parameters
        ----------
        control_type : Union[NegativeControlType, str]
            The unique identifier for the negative control type.
            This allows to define the main library NC types but also custom ones
            (e.g., NegativeControlType.SHUFFLED or "custom_noise").

        Returns
        -------
        Callable
            A decorator function that registers the class.

        Raises
        ------
        ValueError
            If the control type is already registered.

        Example
        -------
        >>> @NegativeControlRegistry.register_control(
        ...     NegativeControlType.SHUFFLED
        ... )
        ... class Shuffled(NegativeControl):
        ...     pass

        """
        # Convert enums to their name for registration consistency
        control_type_key: str = (
            control_type.name if isinstance(control_type, NegativeControlType) else control_type
        ).upper()

        if control_type_key in cls._registry:
            raise ValueError(f"Negative control type '{control_type_key}' is already registered.")
        elif (
            not control_type_key.replace("-", "").replace("_", "").replace(".", "").isalnum()
        ):  # ensure the key is alphanumeric
            # if not alphanumeric, raise an error
            raise KeyError(
                f"Control type '{control_type_key}' is not alphanumeric. "
                "Only hyphens, underscores, and periods are allowed."
            )

        def decorator(control_cls: Type[NegativeControl]) -> Type[NegativeControl]:
            cls._registry[control_type_key] = control_cls
            return control_cls

        return decorator

    @classmethod
    def get_control(
        cls: Type["NegativeControlRegistry"],
        control_type: Union[NegativeControlType, str],
    ) -> Type[NegativeControl]:
        """Retrieve the registered NegativeControl class.

        Parameters
        ----------
        control_type : NegativeControlType
            The type of the negative control to retrieve.

        Returns
        -------
        Type[NegativeControl]
            The registered NegativeControl class.

        Raises
        ------
        ValueError
            If the control type is not registered.
        """
        control_type_key = (
            control_type.name if isinstance(control_type, NegativeControlType) else control_type
        ).upper()

        negative_control_class = cls._registry.get(control_type_key)

        if negative_control_class is None:
            raise ValueError(f"Control type {control_type_key} is not registered.")

        return negative_control_class

    @classmethod
    def get_control_types(cls: Type["NegativeControlRegistry"]) -> List[str]:
        """Return a list of all registered control types.

        Returns
        -------
        List[str]
            A list of all registered control types.

        """
        return list(cls._registry.keys())
