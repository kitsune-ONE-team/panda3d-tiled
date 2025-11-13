from typing import NamedTuple

from pytiled_parser import Properties


class TiledObject(NamedTuple):
    """Object in a tilemaps"""

    shape: tuple[int, int, int, int]
    """Shape of the object"""
    properties: Properties | None = None
    """Properties of the object"""
    name: str | None = None
    """Name of the object"""
    type: str | None = None
    """Type of the object"""
