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
- 🖥️ **Cross-platform** - Works on any operating system with Python 3.
- 🖥️ **CLI Commands** – [1] Start sharing (Server); [2] Download files (Client); [q] Quit.


---

---

## Prerequisite
- To run this application, you need to have Python 3 installed on your system.

---

## 🪛 Installation
1. Download the `py2peer-cli.py` file from this repository.
2. Place it in a folder of your choice.


---
## 🖱️How to Use
Run the application from your terminal or command prompt.
```
python py2peer-cli.py
```

After starting, you will see a command-line menu with the following options:
1. Start sharing files (Server): This will start the file sharing server and allow other peers to connect to you. It also begins broadcasting your presence on the network so others can discover you. You can continue to use the CLI menu while the server is running.
2. List discovered peers: Shows a list of all other py2peer users who are currently running the application in server mode on your network.
3. Download a file from a peer: Prompts you to select a peer from the discovered list and enter the name of the file you wish to download. The file will be saved to a downloads folder created in the same directory as the script.
4. Quit: Exits the application.

---
### 📎Sharing Files
To share a file with other users, simply place the file you want to share inside the `shared_files` folder that is automatically created by the script.

---
### 🔖Note
- Network: Both the server and the client must be on the same local network for discovery and file transfers to work.

- Firewall: You may need to grant firewall permissions for the application to communicate over the network.

- Case-Sensitivity: The application is case-sensitive when requesting file names. Please type the name exactly as it appears.

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
