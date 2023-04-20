#!/usr/bin/env bash
source ~/.bash_profile

# zip randomiser, launch blender and install+enable
cd blender_randomiser
blender ../sample.blend --python ./install_and_enable_addons.py -- ./randomiser.zip 32
