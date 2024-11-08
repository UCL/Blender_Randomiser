#!/usr/bin/env bash
source ~/.bash_profile

#Setup blender path
alias blender=/home/lbinding/software/blender-4.2.3-linux-x64/blender
blender=/home/lbinding/software/blender-4.2.3-linux-x64/blender

# Get script name
script_name=`basename $0`
#Get script location
script_path="$(dirname "$(realpath "$BASH_SOURCE")")"

# Setup user paths
# Loop over arguments looking for -i and -o
args=("$@")
i=0
while [ $i -lt $# ]; do
    #Set blender data
    if ( [ ${args[i]} = "-blend" ] ) ; then
      let i=$i+1
      blend_file=${args[i]}
    elif ( [ ${args[i]} = "-seed" ] ) ; then
      # Set seed value
      let i=$i+1
      seed_num=${args[i]}
    elif ( [ ${args[i]} = "-json_in" ] ) ; then
      # Set json input
      let i=$i+1
      json_input=${args[i]}
    elif ( [ ${args[i]} = "-json_out" ] ) ; then
      # Set json output
      let i=$i+1
      json_output=${args[i]}
    elif ( [ ${args[i]} = "-frame" ] ) ; then
      # Set frame number
      let i=$i+1
      frame=${args[i]}
    elif ( [ ${args[i]} = "-basename" ] ) ; then
      # Set base output
      let i=$i+1
      base_output=${args[i]}
    fi
    let i=$i+1
done

#Check to make sure all required inputs are assigned
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
  echo ""
  echo "${script_name} -blend /home/username/colon.blend -json_in /home/username/input.json -json_out  /home/username/output.json -json /home/username/synb0/dwi.json -seed 32 -frame 10 -basename /home/username/output_frame"
  echo ""
  exit
fi



# zip randomiser, launch blender and install+enable, set seed and input bounds
zip ${script_path}/randomiser.zip -FS -r ${script_path}/randomiser/
#${blender} ${blend_file} --python ${script_path}/install_and_enable_addons.py -- ${script_path}/randomiser.zip --seed 32 --input ${json_input} --output ${json_output}

${blender} -b ${blend_file} --python ${script_path}/install_and_enable_addons.py -- ${script_path}/randomiser.zip --seed 32 --input ${json_input} --frame 10 --basename ${base_output}
