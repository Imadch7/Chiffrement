# Cryptography & End-to-End Encryption Sandbox

This project is a comprehensive educational toolkit and demonstration platform for cryptography. It contains custom Python implementations of various historical, symmetric, and asymmetric cryptographic algorithms, along with two powerful Web Applications to visualize and test them.

##  Project Features

This project is divided into two main interactive modules:

### 1. The Cryptography Pipeline (Web UI)
A "CyberChef-style" web application that allows you to chain multiple cryptographic operations together on a piece of text. 
- **Hashing:** SHA-256, MD5
- **Symmetric Ciphers:** AES, DES, RC4, Bluetooth E0
- **Historical Ciphers:** Caesar, Vigenère, Affine, Hill
- **Asymmetric Ciphers:** RSA-PSS Signatures, Diffie-Hellman Key Exchange

### 2. End-to-End Encrypted Chat (Sockets)
A full client-server chat architecture designed to demonstrate how E2EE works in the real world.
- **Central Routing Server:** Acts as a network router, assigning Virtual IPs (VLANs) to connected clients.
- **Secure Chat Client:** A beautiful web UI where users can message each other. It uses **Diffie-Hellman** for secure key exchange over the network and **RC4** to encrypt all messages locally before they leave the browser.
- **Intruder Sniffer (God Mode):** A "Matrix-themed" Man-In-The-Middle dashboard that secretly intercepts all traffic passing through the server. It proves that even if a network is fully compromised, an attacker can only see useless hexadecimal ciphertext without the shared encryption keys.

---

##  Directory Structure

```text
Chiffrement/
├── Asymmetric_Encryption/
│   ├── diffie_hellman.py      # DH Key Exchange implementation
│   ├── rsa_pss.py             # RSA implementation
│   └── sockets/               # E2EE Chat Application
│       ├── chat_app.py        # Chat Client Web UI
│       ├── intruder_app.py    # MITM Sniffer Web UI
│       ├── server.py          # Central TCP Relay Server
│       ├── dhci.py            # Custom DHCP IP assigner
│       └── .env               # Server configuration (PORT=4000)
│
├── Symmetric_Encryption/      # Custom cipher implementations
│   ├── aes.py
│   ├── rc4.py
│   ├── des.py
│   └── ...
│
└── web_ui/                    # Cryptography Pipeline App
    ├── app.py                 # Flask Backend
    ├── requirements.txt
    └── templates/             # HTML Interface
```

---

##  Prerequisites & Installation

Ensure you have Python 3 installed. Then install the required web frameworks:

```bash
pip install Flask Flask-CORS
```

*(Note: The cryptography algorithms are all custom-built from scratch in pure Python, so they do not require external crypto libraries!)*

---

##  How to Run

### Part 1: The Cryptography Pipeline
To test the various algorithms and chain them together:
1. Open a terminal and navigate to the `web_ui` folder.
2. Run the application:
   ```bash
   python app.py
   ```
3. Open your browser and go to `http://127.0.0.1:5000`.

### Part 2: Secure E2E Chat & Intruder Sniffer
To simulate a network and test the End-to-End Encryption:

**1. Start the Network Server**
Open a terminal in `Asymmetric_Encryption/sockets/` and start the central relay server:
```bash
python server.py
```
*(The server runs on Port 4000 as defined in the `.env` file).*

**2. Start Chat Client 1 (Alice)**
Open a second terminal in the same folder and run:
```bash
python chat_app.py 5001
```
Open `http://127.0.0.1:5001` in your browser. Click **Connect** to get assigned your Virtual IP (e.g., `1.1`).

**3. Start Chat Client 2 (Bob)**
Open a third terminal in the same folder and run:
```bash
python chat_app.py 5002
```
Open `http://127.0.0.1:5002` in your browser. Click **Connect** to get your Virtual IP (e.g., `1.2`).

**4. Start the Intruder Sniffer (Optional)**
Open a fourth terminal in the same folder and run:
```bash
python intruder_app.py 5003
```
Open `http://127.0.0.1:5003` in your browser and click **[ INJECT ]**.

**5. Test the Encryption!**
Go to Alice's chat window (`1.1`), type Bob's IP (`1.2`) into the target box, and send a message. 
- You will see the Diffie-Hellman key exchange trigger automatically.
- Bob will receive the decrypted message.
- If you look at the Intruder Sniffer window, you will see the intercepted traffic—but because of the RC4 encryption, the intruder only sees scrambled hexadecimal garbage!
