#!/usr/bin/env bash
source ~/.bash_profile

# zip randomiser, launch blender and install+enable
zip randomiser.zip -FS -r randomiser/
blender random_all.blend --python install_and_enable_addons.py -- ./randomiser.zip --seed 32 --input ./input_parameters.json --output ./transform_geom_mat_test.json
