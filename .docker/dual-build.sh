#!/bin/bash

file="./.docker/dual-container-compose.yml"

docker compose -f $file --project-directory . --remove-orphans down -t 0

docker compose -f $file --project-directory . up -d --build
