# 📘 ProxyForge

> 🚀 A lightweight Docker-based Tor SOCKS5 & HTTP proxy toolkit for secure networking, testing, and privacy routing.

---

## ⚠️ Disclaimer

This project is intended for:
- Educational purposes
- Network security testing in controlled environments
- Research and DevOps learning

You are responsible for how you use this tool. Misuse of proxy technologies may violate local laws or network policies.

---

## 🚀 Overview

**ProxyForge** is a DevOps-style proxy orchestration tool that runs a fully containerized **Tor network gateway** with optional HTTP proxy support.

It provides a simple CLI (Python + Bash) to manage:
- Tor SOCKS5 proxy
- HTTP proxy layer
- Docker lifecycle
- LAN-accessible proxy endpoints
- Real-time Tor bootstrap monitoring

---

## 🧱 Architecture

```
+----------------------+
|   ProxyForge CLI     |
|   (Python / Bash)    |
+----------+-----------+
           |
           v
+----------------------+
|    Docker Compose    |
|   Tor Container      |
|   Privoxy (optional) |
+----------------------+
           |
           v
     Tor Network
```

---

## ⚙️ Requirements

Before running ProxyForge:

- Docker
- Docker Compose
- Python 3.8+
- Linux / WSL2 (Windows supported via Docker Desktop)

---

## 📦 Installation

### 1. Clone repository

```bash
git clone https://github.com/MoeinDarbani/ProxyForge.git
cd ProxyForge
```

## 🐍 Python (Recommended)

Run interactive CLI:

```bash
python3 proxyforge.py
```

**Features:**
- Interactive menu
- Real-time Tor bootstrap progress bar
- LAN IP detection
- No need to remember commands

### 🧭 Python Menu

```
[1] Start ProxyForge
[2] Stop
[3] Restart
[4] Logs
[5] Exit
```

**Usage:** Just enter the number and press Enter.

---

## 🐚 Bash Script (Alternative)

Make executable:

```bash
chmod +x proxyforge.sh
```

Run:

```bash
./proxyforge.sh
```

Or:

```bash
./proxyforge.sh start
./proxyforge.sh stop
./proxyforge.sh restart
```

---

## 🌐 Default Proxy Ports

| Service  | Address              |
|----------|----------------------|
| SOCKS5   | `127.0.0.1:1080`     |
| HTTP     | `127.0.0.1:8080`     |

If running on LAN:
- SOCKS5 → `<LAN_IP>:1080`
- HTTP   → `<LAN_IP>:8080`

---

## 📊 Features

- ✔ Tor bootstrap progress monitoring
- ✔ Real-time CLI status UI
- ✔ Docker-based isolated environment
- ✔ LAN IP auto-detection
- ✔ Cross-platform support (Linux / Windows via WSL)
- ✔ Dual interface (Python + Bash)
- ✔ Beginner-friendly + DevOps-oriented design

---

## 🧠 Use Cases

- Network security testing
- Proxy routing experiments
- Privacy routing via Tor
- Secure traffic tunneling
- Educational DevOps projects
- Safe and controlled internet censorship circumvention using Tor network routing

---

## 🧪 Example Workflow

```bash
# Start tool
python3 proxyforge.py

# Select:
1 → Start ProxyForge

# Wait until:
Tor: [█████████████████████████] 100%

# Output:
SOCKS5 : 192.168.x.x:1080
HTTP   : 192.168.x.x:8080
```

## 🛑 Stop Service

From CLI: Select `2`

Or manually:

```bash
docker compose down
```

---

## 📜 License

MIT License

---

## 👤 Author

Built by **Moein**  
DevOps / Networking / Security Engineering Project

---

## ⭐ Project Status

**Beta Release:** v0.0.1-beta  
Core functionality stable for testing and development use.