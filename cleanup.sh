#!/bin/bash

# Remove cache files
find . -type f -name '*.cache' -exec rm -f {} +

# Remove .dist-info directories
find . -type d -name '*.dist-info' -exec rm -rf {} +

# Remove .egg-info directories
find . -type d -name '*.egg-info' -exec rm -rf {} +

echo "Cleanup complete."
