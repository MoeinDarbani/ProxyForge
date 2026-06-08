FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y tor && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -r -s /usr/sbin/nologin toruser

RUN mkdir -p /var/lib/tor && chown -R toruser:toruser /var/lib/tor

RUN printf "SocksPort 0.0.0.0:9050\nLog notice stdout\nDataDirectory /var/lib/tor\n" > /etc/tor/torrc

USER toruser

EXPOSE 9050

CMD ["tor", "-f", "/etc/tor/torrc"]
