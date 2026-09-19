FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/acecoin

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       librocksdb-dev \
       pkg-config \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/electrumx

# Pin the upstream project by tag in production. The default can be
# overridden at build time without changing the application repository.
ARG ELECTRUMX_REF=master
RUN git clone --depth 1 --branch "$ELECTRUMX_REF" https://github.com/spesmilo/electrumx.git /opt/electrumx

RUN python -m pip install --no-cache-dir ".[rocksdb,orjson]"

COPY electrumx/coin /opt/acecoin/electrumx/coin
COPY electrumx/python/sitecustomize.py /opt/acecoin/sitecustomize.py
COPY electrumx/docker/entrypoint.sh /entrypoint.sh

RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin electrumx \
    && mkdir -p /data/electrumx /certs \
    && chown -R electrumx:electrumx /data/electrumx /certs /opt/acecoin

USER electrumx
WORKDIR /opt/electrumx

ENTRYPOINT ["/entrypoint.sh"]
