#!/bin/bash
set -e

# Get IDs of all running containers
running_containers=$(sudo docker ps -q)

# Check if there are running containers before attempting to stop
if [ -n "$running_containers" ]; then
    # Loop through each container ID and stop it
    for container_id in $running_containers; do
        sudo docker stop "$container_id"
    done
else
    echo "No running containers found."
fi
