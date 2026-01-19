# Offline-XOR-Chat
A decentralized, offline chat server that turns an old Android phone into a secure communication node using Python/Flask and XOR encryption

 Overview
ZeroTrace is designed for high-stakes privacy. By utilizing Termux on Android and Python/Flask, it creates a local communication hub where data is stored exclusively in Volatile RAM. If the server loses power or is restarted, every single message vanishes instantly.

Key Features

XOR Symmetric Encryption: Messages are encrypted/decrypted locally in the browser. The server only sees ciphertext.

RAM-Only Storage: Zero data is written to the physical disk.

Auto-Destruct Logic: Unique session IDs and their message history are purged automatically after 7 days.

Universal Compatibility: Works on any device with a web browser (iPhone, Android, PC, Mac).

The Architecture
The project follows a Client-Server Architecture operating over HTTP/TCP.

The Node (Old Phone): Runs a Flask server via Termux. It acts as the "Source of Truth" but never sees the "Secret Key."

The Network: A local Wi-Fi Hotspot creates the "Medium" for data transfer.

The Client: The browser handles the XOR operation, ensuring the "Secret Key" never leaves the user's device.

Quick Start
1. Requirements
Android Phone with Termux installed.

Python 3 and Flask.

2. Installation
Bash

pkg update && pkg upgrade
pkg install python
pip install flask
3. Running the Server
Bash

# Run the node
nano server.py
python server.py
4. Connection
Connect your devices to the same Wi-Fi/Hotspot and navigate to: http://<SERVER_IP>:8080/chat/<UNIQUE_ROOM_ID>
