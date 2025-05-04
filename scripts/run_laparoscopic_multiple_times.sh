#!/bin/bash

usage() {
  echo "Usage: $0 <number_of_examples> <json_in> <blender_file_path> <blender_file_path_label> <basename_prefix> [initial_seed]"
  exit 1
}

# Ensure we have at least 5 args now
if [ "$#" -lt 5 ]; then
  usage
fi

NUM_EXAMPLES=$1
JSON_IN=$2
BLENDER_FILE_PATH=$3
BLENDER_FILE_PATH_LABEL=$4
BASENAME_PREFIX=$5

# Optional parameter: initial seed (default: 0)
INITIAL_SEED="${6:-0}"

# Calculate the final seed value to run until (inclusive)
END_SEED=$(( INITIAL_SEED + NUM_EXAMPLES - 1 ))

# Loop over each seed value from 1 to the given number
for ((seed=INITIAL_SEED; seed<=END_SEED; seed++)); do
    echo "Running commands for seed $seed..."

    # Run the first command with the current seed (rendered image)
    sh run_laparoscopic_RandomiserBlender.sh -blend "$BLENDER_FILE_PATH" \
       -seed "$seed" \
       -json_in "$JSON_IN" \
       -frame 1 \
       -basename "${BASENAME_PREFIX}_seed_${seed}"

    # Run the second command with the current seed (associated label)
    sh run_laparoscopic_RandomiserBlender.sh -blend "$BLENDER_FILE_PATH_LABEL" \
       -seed "$seed" \
       -json_in "$JSON_IN" \
       -frame 1 \
       -basename "${BASENAME_PREFIX}_seed_${seed}_label"
done