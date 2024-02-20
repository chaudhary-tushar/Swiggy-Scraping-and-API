#!/bin/bash

# Function to run a command and wait for its successful completion
run_command() {
    "$@"
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "Error: Command '$@' failed with exit code $exit_code."
        exit $exit_code
    fi
}

# Loop to run commands with a 1-minute interval
while true; do
    # Run command 1
    run_command python getall.py

    

    # Run command 2
    run_command python downmenu.py

    

    # Run command 3
    run_command rm menus/*

    # Wait for 1 minute
    sleep 60
done
