__version__ = "0.0.2-beta"

import subprocess
import json
import socket
import os
import time

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

TOR_CONTAINER = "proxyforge-tor"
console = Console()


# -------------------------
# DOCKER SINGLE SOURCE OF TRUTH
# -------------------------

def inspect_container():
    try:
        out = subprocess.check_output(
            ["docker", "inspect", TOR_CONTAINER],
            text=True
        )
        return json.loads(out)[0]
    except:
        return None


def get_state():
    data = inspect_container()
    if not data:
        return "STOPPED"

    state = data["State"]

    if state.get("Running"):
        health = state.get("Health", {}).get("Status")

        if health == "healthy":
            return "RUNNING"
        return "STARTING"

    return "STOPPED"


# -------------------------
# SAFETY CHECKS
# -------------------------

def system_tor_running():
    out = subprocess.getoutput("ps aux | grep '[t]or'")
    return bool(out.strip())


def port_free(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", port))
        return True
    except:
        return False
    finally:
        s.close()


def validate_ports():
    return [p for p in (1080, 8080) if not port_free(p)]


# -------------------------
# DOCKER CONTROL
# -------------------------

def run(cmd):
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def start_container():
    run(["docker", "compose", "up", "-d"])


def stop_container():
    run(["docker", "compose", "down", "--remove-orphans"])
    run(["docker", "rm", "-f", TOR_CONTAINER])


def build():
    run(["docker", "compose", "build"])


# -------------------------
# UI (NO FLICKER, NO PROGRESS FAKE)
# -------------------------

def render():
    state = get_state()

    color = (
        "green" if state == "RUNNING"
        else "yellow" if state == "STARTING"
        else "red"
    )

    table = Table(title="ProxyForge")

    table.add_column("Component")
    table.add_column("Status")

    table.add_row("Tor Container", f"[{color}]{state}[/{color}]")

    return Panel(table)


# -------------------------
# UI LOOP (NON-BLOCKING SAFE)
# -------------------------

def ui_loop():
    with Live(render(), refresh_per_second=2, console=console) as live:
        while True:
            live.update(render())
            time.sleep(1)


# -------------------------
# START FLOW (SAFE)
# -------------------------

def start():
    if system_tor_running():
        console.print("[yellow]Warning: System Tor detected[/yellow]")

    conflicts = validate_ports()
    if conflicts:
        console.print(f"[red]Port conflict: {conflicts}[/red]")
        return

    console.print("[cyan]Building...[/cyan]")
    build()

    console.print("[cyan]Starting container...[/cyan]")
    start_container()

    # wait until docker actually reports running
    for _ in range(30):
        if get_state() in ("RUNNING", "STARTING"):
            break
        time.sleep(1)

    ui_loop()


# -------------------------
# STOP FLOW (FIXED - NO GHOST STATE)
# -------------------------

def stop():
    console.print("[cyan]Stopping ProxyForge...[/cyan]")

    stop_container()

    # verification loop (critical fix)
    for _ in range(10):
        if get_state() == "STOPPED":
            console.print("[green]Stopped successfully[/green]")
            return
        time.sleep(1)

    console.print("[red]Stop failed - container still exists[/red]")


# -------------------------
# LOGS
# -------------------------

def logs():
    subprocess.run(["docker", "logs", "-f", TOR_CONTAINER])


# -------------------------
# MENU
# -------------------------

def menu():
    while True:
        os.system("clear")

        state = get_state()
        console.print(Panel(f"ProxyForge {__version__}\nState: {state}"))

        print("""
[1] Start
[2] Stop
[3] Logs
[4] Exit
""")

        c = input("> ")

        if c == "1":
            start()
        elif c == "2":
            stop()
            input("press...")
        elif c == "3":
            logs()
        elif c == "4":
            break


if __name__ == "__main__":
    menu()