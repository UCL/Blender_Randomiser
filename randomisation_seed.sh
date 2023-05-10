#!/usr/bin/env bash
source ~/.bash_profile

# zip randomiser, launch blender and install+enable
zip -r randomiser.zip randomiser/
blender sample.blend --python install_and_enable_addons.py -- ./randomiser.zip --seed 32
