FROM debian:bookworm-slim

EXPOSE 5000

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
apt-get -y upgrade && \
apt-get -y install python3-flask --no-install-recommends && \
rm -rf /var/lib/apt/lists/*

COPY mock.py /

ENTRYPOINT ["/usr/bin/python3", "-m", "flask", "--app", "mock", "run", "--host", "0.0.0.0"]
