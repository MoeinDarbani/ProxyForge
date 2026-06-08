__version__ = "0.0.2"

import subprocess
import sys
import re
import socket
import os

TOR_CONTAINER = "proxyforge-tor"

RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"


# -------------------------
# Core Utils
# -------------------------

def run(cmd):
    subprocess.run(cmd)


def check_docker():
    try:
        subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except:
        print(f"{RED}Docker is not available{RESET}")
        sys.exit(1)


def is_running():
    result = subprocess.getoutput("docker ps --format '{{.Names}}'")
    return TOR_CONTAINER in result


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


# -------------------------
# UI
# -------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    status = "RUNNING" if is_running() else "STOPPED"
    color = GREEN if status == "RUNNING" else RED

    print(f"""
{BOLD}{CYAN}
========================
     🚀 ProxyForge
     v{__version__}
========================
{RESET}
Tor Status : {color}{status}{RESET}
Container  : {YELLOW}{TOR_CONTAINER}{RESET}
""")


def menu():
    print(f"""
{CYAN}[1]{RESET} Start ProxyForge
{CYAN}[2]{RESET} Stop
{CYAN}[3]{RESET} Restart
{CYAN}[4]{RESET} Logs
{CYAN}[5]{RESET} Exit
""")


# -------------------------
# Tor bootstrap monitor
# -------------------------

def print_progress(percent):
    size = 30
    filled = int(size * percent / 100)
    bar = "█" * filled + "-" * (size - filled)

    print(f"\r{CYAN}Tor:{RESET} [{GREEN}{bar}{RESET}] {YELLOW}{percent}%{RESET}", end="")

    if percent == 100:
        print()


def wait_for_tor():
    print(f"\n{CYAN}Waiting for Tor bootstrap...{RESET}\n")

    process = subprocess.Popen(
        ["docker", "logs", "-f", "--tail", "0", TOR_CONTAINER],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    last = -1

    for line in process.stdout:
        match = re.search(r"Bootstrapped (\d+)%", line)
        if not match:
            continue

        percent = int(match.group(1))

        if percent <= last:
            continue

        last = percent
        print_progress(percent)

        if percent >= 100:
            process.terminate()
            break

    print(f"\n{GREEN}Tor is READY{RESET}\n")


# -------------------------
# Actions
# -------------------------

def start():
    if is_running():
        print(f"{YELLOW}Already running{RESET}")
        return

    check_docker()

    print(f"{CYAN}Building containers...{RESET}")
    run(["docker", "compose", "build"])

    print(f"{CYAN}Starting containers...{RESET}")
    run(["docker", "compose", "up", "-d"])

    wait_for_tor()

    ip = get_lan_ip()

    print(f"""
{GREEN}
========================
        READY
========================
{RESET}
SOCKS5 Proxy : {ip}:1080
HTTP Proxy   : {ip}:8080
""")


def stop():
    run(["docker", "compose", "down"])
    print(f"{RED}Stopped{RESET}")


def logs():
    run(["docker", "logs", "-f", TOR_CONTAINER])


def restart():
    stop()
    start()


# -------------------------
# Menu loop
# -------------------------

def menu_loop():
    while True:
        clear()
        header()
        menu()

        key = input("Select option: ").strip()

        if key == "1":
            start()
        elif key == "2":
            stop()
        elif key == "3":
            restart()
        elif key == "4":
            logs()
        elif key == "5":
            print("Bye 👋")
            break
        else:
            print("Invalid option")

        input("\nPress Enter to continue...")


# -------------------------
# Entry
# -------------------------

if __name__ == "__main__":
    menu_loop()