from pathlib import Path

from panda3d import core as p3d


class TextureCacheManager:
    """
    A simple manager wrapping texture and image data
    with convenient methods for loading textures and sprite sheets.

    Args:
        texture_cache:
            Optional texture cache to use. If not specified, a new cache will be created
    """

    def __init__(
        self,
        hit_box_cache = None,
        image_data_cache = None,
        texture_cache = None,
    ):
        self._texture_cache = texture_cache or {}

    def _image_open(
        self,
        file_path: str | Path,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
    ) -> p3d.PNMImage:
        uri = p3d.Filename.from_os_specific(str(file_path))
        vfs = p3d.VirtualFileSystem.getGlobalPtr()

        image = p3d.PNMImage(uri)
        image.read(vfs.open_read_file(uri, True))
        x_size = image.get_read_x_size()
        y_size = image.get_read_y_size()

        # asked to crop an image
        if x or y or (width and height):
            image.expand_border(
                -x,  # left
                -(x_size - x - width),  # right
                -(y_size - y - height),  # bottom
                -y,  # top
                p3d.LColor(0, 0, 0, 0))

        return image

    def load_or_get_texture(
        self,
        file_path: str | Path,
        *,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        **kwargs
    ) -> p3d.Texture:
        """
        Load an image from disk and create a texture. If the image is already
        loaded, return the cached version.

        The ``x``, ``y``, ``width``, and ``height`` parameters are used to
        specify a sub-rectangle of the image to load. If not specified, the
        entire image is loaded.

        Args:
            file_path:
                Path to the image file.
            x:
                X coordinate of the texture in the image.
            y:
                Y coordinate of the texture in the image.
            width:
                Width of the texture in the image.
            height:
                Height of the texture in the image.
        """
        cache_key = f'{file_path}:{x}:{y}:{width}:{height}'
        if cache_key in self._texture_cache:
            return self._texture_cache[cache_key]

        uri = p3d.Filename.from_os_specific(str(file_path))
        texture = p3d.Texture(uri.get_basename())
        texture.set_format(p3d.Texture.F_srgb_alpha)
        texture.load(self._image_open(file_path, x, y, width, height))

        self._texture_cache[cache_key] = texture
        return texture


class PNMTextureCacheManager(TextureCacheManager):
    """
    A simple manager wrapping texture and image data
    with convenient methods for loading textures and sprite sheets.

    Args:
        texture_cache:
            Optional texture cache to use. If not specified, a new cache will be created
    """

    def load_or_get_texture(
        self,
        file_path: str | Path,
        *,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        **kwargs
    ) -> p3d.PNMImage:
        cache_key = f'{file_path}:{x}:{y}:{width}:{height}'
        if cache_key in self._texture_cache:
            return self._texture_cache[cache_key]

        image = self._image_open(file_path, x, y, width, height)

        self._texture_cache[cache_key] = image
        return image
