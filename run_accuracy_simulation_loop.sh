#!/bin/bash
# Accuracy simulation restart loop - restarts simulation if killed
# Press Ctrl+C to stop

trap "echo 'Stopping simulation loop...'; exit 0" SIGINT SIGTERM

while true; do
    echo "Starting accuracy simulation at $(date)"
    python run_accuracy_simulation.py
    exit_code=$?

    if [ $exit_code -eq 137 ] || [ $exit_code -eq 143 ]; then
        # 137 = SIGKILL (killed), 143 = SIGTERM (terminated)
        echo "Simulation was killed (exit code $exit_code). Restarting in 2 seconds..."
        sleep 2
    elif [ $exit_code -eq 0 ]; then
        echo "Simulation completed successfully. Exiting."
        break
    else
        echo "Simulation exited with code $exit_code. Restarting in 2 seconds..."
        sleep 2
    fi
done
