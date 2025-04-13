#!/bin/bash

# Check if the mandatory arguments are provided
if [ "$#" -lt 4 ]; then
    echo "Usage: $0 <number_of_examples> <json_in> <blender_file_path> <blender_file_path_label>"
    exit 1
fi

NUM_EXAMPLES=$1
JSON_IN=$2
BLENDER_FILE_PATH=$3
BLENDER_FILE_PATH_LABEL=$4
BASENAME_PREFIX=$5

# Optional parameter: initial seed (default: 0)
if [ -n "$6" ]; then
    INITIAL_SEED=$6
else
    INITIAL_SEED=0
fi

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