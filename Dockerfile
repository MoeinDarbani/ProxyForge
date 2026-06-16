FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y tor curl && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -r -s /usr/sbin/nologin toruser

RUN mkdir -p /var/lib/tor && chown -R toruser:toruser /var/lib/tor

RUN printf "SocksPort 0.0.0.0:9050\nLog notice stdout\nDataDirectory /var/lib/tor\n" > /etc/tor/torrc

USER toruser

EXPOSE 9050

HEALTHCHECK --interval=5s --timeout=3s --retries=20 \
  CMD curl --socks5-hostname localhost:9050 https://check.torproject.org >/dev/null 2>&1 || exit 1

CMD ["tor", "-f", "/etc/tor/torrc"]