#!/usr/bin/env bash
zip -r blender_randomiser/randomiser.zip blender_randomiser/randomiser
blender --python blender_randomiser/install_and_enable_addons.py -- blender_randomiser/randomiser.zip
