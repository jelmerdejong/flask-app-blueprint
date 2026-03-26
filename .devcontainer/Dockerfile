FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssh-server \
    && mkdir -p /var/run/sshd \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir uv
