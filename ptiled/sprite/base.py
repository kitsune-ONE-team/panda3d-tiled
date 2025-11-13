from typing import Any

from panda3d import core as p3d


class BasicSprite:
    """
    The absolute minimum needed for a sprite.

    Args:
        texture:
            The texture data to use for this sprite.
        scale:
            The scaling factor for drawing the texture.
        center_x:
            Location of the sprite along the X axis in pixels.
        center_y:
            Location of the sprite along the Y axis in pixels.
    """

    def __init__(
        self,
        texture: p3d.Texture,
        scale: float | p3d.Point2 = 1.0,
        center_x: float = 0,
        center_y: float = 0,
        visible: bool = True,
        **kwargs: Any,
    ) -> None:
        self._position = (center_x, center_y)
        self._depth = 0.0
        self._texture = texture
        width = texture.get_x_size()
        height = texture.get_y_size()
        self._scale = (scale, scale) if isinstance(scale, float | int) else (scale[0], scale[1])  # noqa: UP038
        self._width = width * self._scale[0]
        self._height = height * self._scale[1]
        self._visible = bool(visible)
        self._color: p3d.LColor = p3d.LColor(1, 1, 1, 1)

        cm = p3d.CardMaker(texture.get_name())
        cm.set_frame(-width / 2, width / 2, -height / 2, height / 2)
        self.nodepath = p3d.NodePath(cm.generate())
        self.nodepath.set_pos(self._position[0], 0, self._position[1])
        self.nodepath.set_texture(texture)
        self.nodepath.set_transparency(p3d.TransparencyAttrib.M_alpha, 1)

        self._angle = 0.0

    # --- Core Properties ---

    @property
    def position(self) -> p3d.Point2:
        """Get or set the center x and y position of the sprite."""
        return self._position

    @position.setter
    def position(self, new_value: p3d.Point2):
        if new_value == self._position:
            return

        self._position = new_value
        self.nodepath.set_pos(self._position[0], 0, self._position[1])

    @property
    def center_x(self) -> float:
        """Get or set the center x position of the sprite."""
        return self._position[0]

    @center_x.setter
    def center_x(self, new_value: float):
        if new_value == self._position[0]:
            return

        self.position = (new_value, self._position[1])

    @property
    def center_y(self) -> float:
        """Get or set the center y position of the sprite."""
        return self._position[1]

    @center_y.setter
    def center_y(self, new_value: float):
        if new_value == self._position[1]:
            return

        self.position = (self._position[0], new_value)

    @property
    def width(self) -> float:
        """Get or set width or the sprite in pixels"""
        return self._width

    @width.setter
    def width(self, new_value: float):
        if new_value != self._width:
            self._scale = new_value / self._texture.get_x_size(), self._scale[1]
            self._width = new_value

    @property
    def height(self) -> float:
        """Get or set the height of the sprite in pixels."""
        return self._height

    @height.setter
    def height(self, new_value: float):
        if new_value != self._height:
            self._scale = self._scale[0], new_value / self._texture.get_y_size()
            self._height = new_value
            self.nodepath.set_scale(self._scale[0], 1, self._scale[1])
