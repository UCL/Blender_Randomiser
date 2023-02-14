#!/usr/bin/env bash
cd blender_randomiser/randomiser
zip -r ../randomiser.zip *
blender --python ../install_and_enable_addons.py -- ../randomiser.zip
