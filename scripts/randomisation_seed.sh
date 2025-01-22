#!/usr/bin/env bash
source ~/.bash_profile

# zip randomiser, launch blender and install+enable, set seed and input bounds
zip ../randomiser.zip -FS -r ../randomiser/
blender ../blend_files/sample.blend --python ../install_and_enable_addons.py -- ../randomiser.zip --seed 32 --input ../input_files/input_bounds.json --output ../output_files/output_randomisations_per_frame1697116725.310647.json
