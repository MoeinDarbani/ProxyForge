#!/usr/bin/env bash

set -e

CONTAINER="proxyforge-tor"

function build() {
    echo "[+] Building ProxyForge..."
    docker compose build
}

function wait_for_tor() {
    echo "[+] Waiting for Tor to be ready..."

    docker logs -f $CONTAINER 2>&1 | while read line; do
        echo "$line"

        if echo "$line" | grep -q "Bootstrapped 100%"; then
            echo ""
            echo "[✓] Tor is fully bootstrapped"
            pkill -P $$ docker 2>/dev/null || true
            break
        fi
    done
}

function up() {
    echo "[+] Starting ProxyForge..."
    docker compose up -d

    wait_for_tor &

    echo ""
    echo "[✓] ProxyForge is running"
    echo "---------------------------"
    echo "SOCKS5 : 127.0.0.1:${SOCKS_PORT:-9050}"
    echo "HTTP   : 127.0.0.1:${HTTP_PORT:-8118}"
    echo "---------------------------"
}

function down() {
    docker compose down
}

function logs() {
    docker logs -f $CONTAINER
}

function restart() {
    down
    up
}

case "$1" in
    up) build && up ;;
    down) down ;;
    logs) logs ;;
    restart) restart ;;
    *) echo "Usage: $0 {up|down|logs|restart}" ;;
esac
