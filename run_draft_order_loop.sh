#!/bin/bash
# Draft order loop restart script - restarts if killed
# Press Ctrl+C to stop

trap "echo 'Stopping draft order loop...'; exit 0" SIGINT SIGTERM

while true; do
    echo "Starting draft order loop at $(date)"
    python run_draft_order_loop.py --use-processes "$@"
    exit_code=$?

    if [ $exit_code -eq 137 ] || [ $exit_code -eq 143 ]; then
        # 137 = SIGKILL (killed), 143 = SIGTERM (terminated)
        echo "Draft order loop was killed (exit code $exit_code). Restarting in 2 seconds..."
        sleep 2
    elif [ $exit_code -eq 0 ]; then
        echo "Draft order loop completed successfully. Exiting."
        break
    else
        echo "Draft order loop exited with code $exit_code. Restarting in 2 seconds..."
        sleep 2
    fi
done
