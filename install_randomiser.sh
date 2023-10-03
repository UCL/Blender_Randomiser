#!/usr/bin/env bash

source ~/.bash_profile

# zip randomiser, launch blender and install+enable
zip randomiser.zip -FS -r randomiser/
blender define_prop.blend --python install_and_enable_addons.py -- ./randomiser.zip
