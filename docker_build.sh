#!/bin/bash
DOCKER_BUILDKIT=1 docker build --progress=plain -t myapp:1 .  --no-cache

