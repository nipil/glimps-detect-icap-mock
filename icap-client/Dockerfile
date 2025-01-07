# use apache as base so that the containers is kept running
FROM httpd:bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
apt-get -y upgrade && \
apt-get -y install python3-flask curl c-icap && \
rm -rf /var/lib/apt/lists/*
