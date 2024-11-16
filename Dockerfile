# syntax=docker/dockerfile:labs
FROM python:3.13.0-slim-bookworm AS pip
ENV PYTHONUNBUFFERED=1
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
COPY requirements.txt /tmp/requirements.txt
ARG DEBIAN_FRONTEND=noninteractive
RUN echo 'APT::Install-Recommends "0";' | tee -a /etc/apt/apt.conf.d/01norecommend && \
    echo 'APT::Install-Suggests "0";' | tee -a /etc/apt/apt.conf.d/01norecommend && \
    apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m venv /usr/local && \
    pip install --no-cache-dir -r /tmp/requirements.txt

FROM python:3.13.0-slim-bookworm
ENV PYTHONUNBUFFERED=1
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
COPY --from=pip /usr/local /usr/local
ARG DEBIAN_FRONTEND=noninteractive
RUN echo 'APT::Install-Recommends "0";' | tee -a /etc/apt/apt.conf.d/01norecommend && \
    echo 'APT::Install-Suggests "0";' | tee -a /etc/apt/apt.conf.d/01norecommend && \
    apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y ca-certificates tzdata tini && \
    playwright install --with-deps chromium && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY app.py /usr/local/bin/app.py
ENTRYPOINT ["tini", "--", "app.py"]
