from panda3d import core as p3d


class SpriteList:
    def __init__(
        self,
        visible: bool = True,
        **kwargs
    ) -> None:
        # List of sprites in the sprite list
        self.sprite_list = []
        self.nodepath = p3d.NodePath('SpriteList')
        self.visible = visible

    @property
    def visible(self) -> bool:
        """
        Get or set the visible flag for this spritelist.

        If visible is ``False`` the ``draw()`` has no effect.
        """
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value
        if value:
            self.nodepath.show()
        else:
            self.nodepath.hide()

    def append(self, sprite) -> None:
        """
        Add a new sprite to the list.

        Args:
            sprite: Sprite to add to the list.
        """
        self.sprite_list.append(sprite)
        sprite.nodepath.reparent_to(self.nodepath)
