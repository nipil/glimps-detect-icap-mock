FROM glimpsre/icap-detect:v0.2.2 AS detect

FROM debian:bookworm-slim

EXPOSE 5000

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
apt-get -y upgrade && \
apt-get -y install python3-flask curl c-icap musl && \
rm -rf /var/lib/apt/lists/*

COPY mock.py /

COPY --from=detect /srv/icap-detect /srv/icap-detect

ENTRYPOINT ["/usr/bin/python3", "-m", "flask", "--app", "mock", "run", "--host", "0.0.0.0"]
