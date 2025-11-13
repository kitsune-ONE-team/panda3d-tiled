#!/usr/bin/env python3
import os
import sys

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_PATH)

from direct.showbase.ShowBase import ShowBase
from panda3d import core as p3d

from ptiled.tilemap.tilemap import TileMap


class Sample(ShowBase):
    def __init__(self):
        p3d.load_prc_file_data('', '''
            win-size 1280 720
            framebuffer-srgb t
            framebuffer-alpha f
            show-frame-rate-meter t
            textures-power-2 f
        ''')
        super().__init__()

        # The map is based on Free CC0 Top Down Tileset Template Pixel Art by rgsdev
        # https://rgsdev.itch.io/free-cc0-top-down-tileset-template-pixel-art
        tilemap = TileMap(os.path.join(os.path.dirname(__file__), 'map.json'))

        # make root node to attach all the layers
        root = p3d.NodePath('root')
        root.reparent_to(self.render)
        root.set_scale(0.1)

        # make tree of layers and attach them to the root node
        self._process_layers(tilemap, tilemap.tiled_map.layers, root)

        self.cam.set_pos((20, -50, 40))
        self.camLens.set_near_far(0.01, 1000)

        # generic key bingins
        self.accept('escape', sys.exit)
        self.accept('q', sys.exit)
        self.accept('l', self.render.ls)
        self.accept('f3', self.toggleWireframe)

        # camera movement keys
        self._movement = {}
        self.accept('w', lambda: self._move('up', True))
        self.accept('w-up', lambda: self._move('up', False))
        self.accept('s', lambda: self._move('down', True))
        self.accept('s-up', lambda: self._move('down', False))
        self.accept('a', lambda: self._move('left', True))
        self.accept('a-up', lambda: self._move('left', False))
        self.accept('d', lambda: self._move('right', True))
        self.accept('d-up', lambda: self._move('right', False))
        self.accept('f', lambda: self._move('forward', True))
        self.accept('f-up', lambda: self._move('forward', False))
        self.accept('r', lambda: self._move('backward', True))
        self.accept('r-up', lambda: self._move('backward', False))

        # main game loop
        self.task_mgr.add(self.update, 'update')

    def _process_layers(self, tilemap, layers, parent):
        zoffset = 0

        for layer in layers:
            if layer.name not in tilemap.sprite_lists:
                np = p3d.NodePath(layer.name)
            else:
                np = tilemap.sprite_lists[layer.name].nodepath

            # get layer's height from "z" property
            z = (layer.properties or {}).get('z', 0) 

            # add extra offset for the layers with the same height
            z += zoffset
            zoffset += 0.5

            # attach layer to parent
            np.reparent_to(parent)
            np.set_y(-z)

            # process child layers and attach them to current layer
            if hasattr(layer, 'layers'):
                self._process_layers(tilemap, layer.layers, np)

    def _move(self, side, active):
        self._movement[side] = active

    def update(self, task):
        dt = p3d.ClockObject.get_global_clock().get_dt()
        speed = 20

        # move entity
        if self._movement.get('up') and not self._movement.get('down'):
            self.cam.set_z(self.cam, dt * speed)
        elif not self._movement.get('up') and self._movement.get('down'):
            self.cam.set_z(self.cam, dt * -speed)
        if self._movement.get('left') and not self._movement.get('right'):
            self.cam.set_x(self.cam, dt * -speed)
        elif not self._movement.get('left') and self._movement.get('right'):
            self.cam.set_x(self.cam, dt * speed)
        if self._movement.get('forward') and not self._movement.get('backward'):
            self.cam.set_y(self.cam, dt * speed)
        elif not self._movement.get('forward') and self._movement.get('backward'):
            self.cam.set_y(self.cam, dt * -speed)

        return task.again


app = Sample()
app.run()
