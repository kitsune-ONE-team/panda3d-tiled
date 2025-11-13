from pathlib import Path
from typing import Any

from panda3d import core as p3d

from .base import BasicSprite


class Sprite(BasicSprite):
    """
    Sprites are used to render image data to the screen.

    Most games center around sprites.

    Args:
        path_or_texture:
            Path to an image file, or a texture object.
        center_x:
            Location of the sprite in pixels.
        center_y:
            Location of the sprite in pixels.
        scale:
            Show the image at this many times its original size.
        angle:
            The initial rotation of the sprite in degrees
    """

    def __init__(
        self,
        path_or_texture: str | Path | p3d.Texture = None,
        scale: float | tuple = 1.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        angle: float = 0.0,
        **kwargs,
    ) -> None:
        if isinstance(path_or_texture, p3d.Texture):
            _texture = path_or_texture
        elif isinstance(path_or_texture, str | Path):
            _texture = TextureCacheManager().load_or_get_texture(path_or_texture)
        super().__init__(
            _texture,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
            **kwargs,
        )

        self._angle = angle
        self.nodepath.set_r(angle)

        # Custom sprite properties
        self._properties: dict[str, Any] | None = None

    # --- Properties ---

    @property
    def angle(self) -> float:
        """
        Get or set the rotation or the sprite.

        The value is in degrees and is clockwise.
        """
        return self._angle

    @angle.setter
    def angle(self, new_value: float) -> None:
        if new_value == self._angle:
            return

        self._angle = new_value
        self.nodepath.set_r(new_value)

    @property
    def properties(self) -> dict[str, Any]:
        """Get or set custom sprite properties."""
        if self._properties is None:
            self._properties = {}
        return self._properties

    @properties.setter
    def properties(self, value: dict[str, Any]) -> None:
        self._properties = value
