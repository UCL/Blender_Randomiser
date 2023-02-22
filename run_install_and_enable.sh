#!/usr/bin/env bash
cd blender_randomiser
zip -r randomiser.zip randomiser/
blender ../sample.blend --python ./install_and_enable_addons.py -- ./randomiser.zip
