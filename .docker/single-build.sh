#!/bin/bash

file="./.docker/single-container-compose.yml"

docker compose -f $file down -t 0

docker compose -f $file --project-directory . up -d --build
