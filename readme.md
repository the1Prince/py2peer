# Py2Peer – Peer-to-Peer File Sharing App

![Logo](downloads/logo-t.png)  
*A lightweight, CLI peer-to-peer (P2P) file sharing app.*

---

## 📖 Overview
**Py2Peer** is a Python-based peer-to-peer file sharing tool that allows devices on the same local network to **discover each other automatically** and share files without the need for a central server.  

It runs in the **system tray**, providing easy access to:
- Start file sharing
- Discover peers
- Download files
- Exit the app

---

## ✨ Features
- 🔍 **Peer Discovery** – Uses UDP broadcast to find peers on the LAN.
- 📤 **File Sharing** – Share files from a `shared_files` directory.
- 📥 **File Downloading** – Download files from discovered peers into a `downloads` folder.
- 🖥️ **CLI Commands** – [1] Start sharing (Server); [2] Download files (Client); [q] Quit.


---

## 📂 Project Structure
```
py2peer/
├── client_node.py
├── file_discovery.py
├── py2peer.py
├── readme.py
└── requirements.txt
└── server_node.py
```