__version__ = "0.0.1-beta"

import subprocess
import sys
import re
import socket
import os

CONTAINER = "proxyforge-tor"

# -------------------------
# Colors
# -------------------------

RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# -------------------------
# Docker Utils
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
        print(f"{RED}[✗] Docker not available{RESET}")
        sys.exit(1)

def is_running():
    result = subprocess.getoutput("docker ps --format '{{.Names}}'")
    return CONTAINER in result

# -------------------------
# LAN IP
# -------------------------

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
# UI Helpers
# -------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def render_header():
    status = "RUNNING" if is_running() else "STOPPED"
    color = GREEN if status == "RUNNING" else RED

    print(f"""
{BOLD}{CYAN}
====================================
        🚀 ProxyForge
           {__version__}
====================================
{RESET}
Status   : {color}{status}{RESET}
Container: {YELLOW}{CONTAINER}{RESET}

""")

def render_menu():
    print(f"""
{CYAN}[1]{RESET} Start ProxyForge
{CYAN}[2]{RESET} Stop
{CYAN}[3]{RESET} Restart
{CYAN}[4]{RESET} Logs
{CYAN}[5]{RESET} Exit

Press a key (NO ENTER REQUIRED)
""")

# -------------------------
# Progress
# -------------------------

def render_bar(percent, size=25):
    filled = int(size * percent / 100)
    return "█" * filled + "-" * (size - filled)

def print_progress(percent):
    bar = render_bar(percent)
    sys.stdout.write(
        f"\r{CYAN}Tor:{RESET} [{GREEN}{bar}{RESET}] {YELLOW}{percent:3d}%{RESET}"
    )
    sys.stdout.flush()
    if percent == 100:
        print()

# -------------------------
# Tor watcher
# -------------------------

def wait_for_tor():
    print(f"\n{CYAN}[+] Bootstrapping Tor...{RESET}\n")

    last = -1

    process = subprocess.Popen(
        ["docker", "logs", "-f", "--tail", "0", CONTAINER],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        m = re.search(r"Bootstrapped (\d+)%", line)
        if not m:
            continue

        percent = int(m.group(1))

        if percent <= last:
            continue

        last = percent
        print_progress(percent)

        if percent >= 100:
            process.terminate()
            break

    print(f"\n{GREEN}[✓] Tor READY{RESET}\n")

# -------------------------
# Actions
# -------------------------

def start():
    if is_running():
        print(f"{YELLOW}Already running{RESET}")
        return

    check_docker()

    print(f"{CYAN}Building...{RESET}")
    run(["docker", "compose", "build"])

    print(f"{CYAN}Starting...{RESET}")
    run(["docker", "compose", "up", "-d"])

    wait_for_tor()

    ip = get_lan_ip()

    print(f"""
{GREEN}
========================
        READY
========================
{RESET}
SOCKS5 : {ip}:1080
HTTP   : {ip}:8080
""")

def stop():
    run(["docker", "compose", "down"])
    print(f"{RED}Stopped{RESET}")

def logs():
    run(["docker", "logs", "-f", CONTAINER])

def restart():
    stop()
    start()

# -------------------------
# RAW KEY INPUT (NO ENTER)
# -------------------------

def get_key():
    try:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        return key

    except:
        import msvcrt
        return msvcrt.getch().decode()

# -------------------------
# MENU LOOP (NO ENTER)
# -------------------------

def menu():
    while True:
        clear()
        render_header()
        render_menu()

        key = get_key()

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
            print("Invalid key")

        input("\nPress Enter to continue...")

# -------------------------
# ENTRY
# -------------------------

if __name__ == "__main__":
    menu()
