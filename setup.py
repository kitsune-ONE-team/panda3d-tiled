#!/usr/bin/env python3
import os
import setuptools
import subprocess


if __name__ == "__main__":
    setuptools.setup(
        name='panda3d-tiled',
        version='0.0.1',
        description='Tiled importer for Panda3D',
        long_description='Python library for loading Tiled maps into Panda3D',
        url='https://github.com/kitsune-ONE-team/panda3d-tiled',
        download_url='https://github.com/kitsune-ONE-team/panda3d-tiled',
        author='Yonnji',
        license='MIT',
        packages=[
            'ptiled',
            'ptiled.sprite',
            'ptiled.tilemap',
        ],
        install_requires=['panda3d', 'pytiled_parser'],
    )
