#!/bin/bash --login
set -e

# Activate the conda environment (replace with your env name if different)
conda activate flagellar_motor_detection_project

# Execute the CMD from the Dockerfile
exec "$@"
