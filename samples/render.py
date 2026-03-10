#!/usr/bin/env python3
"""
This sample show how to render the tilemap into a png file.
"""
import io
import os
import sys
import numpy as np

from panda3d import core as p3d
from PIL import Image

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_PATH)

from ptiled.tilemap.tilemap import TileMap
from ptiled.texture_manager import PNMTextureCacheManager


def rotate_image(image, angle):
    width = image.get_x_size()
    height = image.get_y_size()

    texture = p3d.Texture()
    texture.set_format(p3d.Texture.F_srgb_alpha)
    texture.load(image)

    data = texture.get_ram_image()

    bgra = np.frombuffer(data, dtype=np.uint8).reshape(height, width, 4)
    bgra = np.flipud(bgra)  # Flip vertically (Panda3D origin is bottom-left, PIL is top-left)
    rgba = bgra[:, :, [2, 1, 0, 3]]  # R->B, G->G, B->R, A->A

    pil_image = Image.fromarray(rgba, 'RGBA')
    pil_image = pil_image.rotate(angle, expand=True)

    # data = pil_image.tobytes()
    stream = p3d.StringStream()
    pil_image.save(stream, format='PNG')

    result = p3d.PNMImage(*pil_image.size, 4)

    ft_reg = p3d.PNMFileTypeRegistry.get_global_ptr()
    ft = ft_reg.get_type_from_extension('pil.png')
    result.read(stream, 'pil.png', ft, False)

    return result


def main():
    # The map is based on Free CC0 Top Down Tileset Template Pixel Art by rgsdev
    # https://rgsdev.itch.io/free-cc0-top-down-tileset-template-pixel-art
    # tilemap = TileMap(os.path.join(os.path.dirname(__file__), 'map.json'))
    tilemap = TileMap(
        os.path.join(os.path.dirname(__file__), 'map.json'),
        texture_cache_manager=PNMTextureCacheManager())

    output = p3d.PNMImage(
        tilemap.width * tilemap.tile_width,
        tilemap.height * tilemap.tile_height,
        4)

    def process_layers(tilemap, layers):
        for layer in layers:
            if layer.name in tilemap.sprite_lists:
                for sprite in tilemap.sprite_lists[layer.name].sprite_list:
                    texture = sprite._texture
                    width = sprite.width
                    height = sprite.height

                    if sprite.angle:
                        texture = rotate_image(texture, -sprite.angle)
                        # update the size, because it could be increased due to image rotation
                        width = texture.get_x_size()
                        height = texture.get_y_size()

                    xto = int(sprite.position[0]) - int(width / 2)
                    yto = output.get_y_size() - int(sprite.position[1]) - int(height / 2)

                    output.blend_sub_image(
                        texture,  # from image
                        xto, yto,  # (x,y) to
                        0, 0,  # (x,y) from
                        int(width), int(height))  # (width,height) from

            # get layer's height from "z" property
            z = (layer.properties or {}).get('z', 0) 

            # process child layers
            if hasattr(layer, 'layers'):
                process_layers(tilemap, layer.layers)

    process_layers(tilemap, tilemap.tiled_map.layers)

    output.write('output.png')


if __name__ == '__main__':
    main()
