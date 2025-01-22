from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point3D:
    """Represent a point in 3D space."""
    x: int
    y: int
    z: int

    @property
    def as_tuple(self) -> tuple[int, int, int]:
        """Return the point as a tuple."""
        return self.x, self.y, self.z

    def __add__(self, other: Point3D) -> Point3D:
        """Add two points."""
        return Point3D(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other: Point3D) -> Point3D:
        """Subtract two points."""
        return Point3D(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)


@dataclass
class Size3D(Point3D):
    """Represent the size of a 3D object using its width, height, and depth."""

    pass


@dataclass
class Coordinate(Point3D):
    """Represent a coordinate in 3D space."""
    
    def __add__(self, other: Size3D) -> Coordinate:
        """Add a size to a coordinate to get a second coordinate."""
        return Coordinate(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)
    
    def __sub__(self, other: Size3D) -> Coordinate:
        """Subtract a size from a coordinate to get a second coordinate."""
        return Coordinate(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)
    


@dataclass
class Centroid(Coordinate):
    """Represent the centroid of a region in 3D space.

    A centroid is simply a coordinate in 3D space that represents
    the center of mass of a region in an image. It is represented
    by its x, y, and z coordinates.

    Attributes
    ----------
    x : int
    y : int
    z : int
    """

    pass