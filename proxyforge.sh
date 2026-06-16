#!/usr/bin/env bash
set -e

CONTAINER="proxyforge-tor"

up() {
  docker compose build
  docker compose up -d
  docker logs -f $CONTAINER
}

down() {
  docker compose down --remove-orphans
}

logs() {
  docker logs -f $CONTAINER
}

case "$1" in
  up) up ;;
  down) down ;;
  logs) logs ;;
  *) echo "up | down | logs" ;;
esac