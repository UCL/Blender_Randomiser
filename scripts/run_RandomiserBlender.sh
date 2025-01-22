#!/usr/bin/env bash
#
# run_RandomiserBlender.sh
#   Takes user inputs and randomises these on a blend file and saves a frame
#
# Created by ruaridhg & lbinding
#   08/11/2024
#

# source ~/.bash_profile

# #Setup blender path
# alias blender=/Applications/Blender.app/Contents/MacOS/Blender
# blender=/Applications/Blender.app/Contents/MacOS/Blender

# Get script name
script_name=`basename $0`
#Get script location
main_dir="$(dirname "$(realpath "$BASH_SOURCE")")/.."
script_path="$(dirname "$(realpath "$BASH_SOURCE")")"

#Check if files are in the script directory
if [ ! -f ../install_and_enable_addons.py ]; then
  echo "ERROR: 'install_and_enable_addons.py' is not located in the main directory"
  echo "exiting..."
fi
if [ ! -f ../randomiser.zip ]; then
  echo "ERROR: 'randomiser.zip' is not located in the main directory"
  echo "exiting..."
fi

# Setup user paths
# Loop over arguments looking for -i and -o
args=("$@")
i=0
while [ $i -lt $# ]; do
    # Set blender data
    if [ "${args[i]}" = "-blend" ]; then
      let i=i+1
      blend_file="${args[i]}"
    elif [ "${args[i]}" = "-seed" ]; then
      # Set seed value
      let i=i+1
      seed_num="${args[i]}"
    elif [ "${args[i]}" = "-json_in" ]; then
      # Set json input
      let i=i+1
      json_input="${args[i]}"
    elif [ "${args[i]}" = "-frame" ]; then
      # Set frame number
      let i=i+1
      frame="${args[i]}"
    elif [ "${args[i]}" = "-basename" ]; then
      # Set base output
      let i=i+1
      base_output="${args[i]}"
    elif [ "${args[i]}" = "-render_main" ]; then
      # Set Render main as true or false
      let i=i+1
      render_main=True
    fi
    let i=i+1
done

# Debugging: Print each variable to check values
echo "Blend file: ${blend_file}"
echo "Seed: ${seed_num}"
echo "JSON input: ${json_input}"
echo "Frame: ${frame}"
echo "Base output: ${base_output}"

# Check to make sure all required inputs are assigned
if [ -z "${blend_file}" ] || [ -z "${seed_num}" ] || [ -z "${json_input}" ]; then
    correct_input=0
else
    correct_input=1
fi

#Check the user has provided the correct inputs
if ( [[ ${correct_input} -eq 0 ]] ) ; then
  echo ""
  echo "Incorrect input. Please see below for correct use"
  echo ""
  echo "Options:"
  echo " -blend:              Absolute path to working directory  -- REQUIRED"
  echo " -json_in:            Input dwi data (full path)  -- REQUIRED"
  echo " -json_out:           Input bvec data (full path)  -- REQUIRED"
  echo " -seed:               Input bval data (full path)  -- REQUIRED"
  echo " -frame:              Input number (full path)  -- REQUIRED"
  echo " -basename:           Input basename (full path)  -- REQUIRED"
  echo " -render_main:        Sets variable to true to run main image generation (full path)  -- OPTIONAL"
  echo ""
  echo "${script_name} -blend /home/username/colon.blend -json_in /home/username/input.json -json_out  /home/username/output.json -json /home/username/synb0/dwi.json -seed 32 -frame 10 -basename /home/username/output_frame -render_main"
  echo ""
  exit
fi

# zip randomiser
zip ../randomiser.zip -FS -r ../randomiser/

# Run blender in the background (-b) and run the python script inputting the seed,
blender -b ${blend_file} --python install_and_enable_addons_render.py -- ../randomiser.zip --seed ${seed_num} --input ${json_input} --frame ${frame} --basename ${base_output} --render_main ${render_main}
