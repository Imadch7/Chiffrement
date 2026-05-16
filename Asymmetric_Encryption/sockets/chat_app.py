import os
import sys
import threading
import json
import socket
import time
import hashlib
import importlib.util
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from request import Request

# Load custom crypto modules
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

current_dir = os.path.dirname(os.path.abspath(__file__))
grandparent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))

dh_path = os.path.join(grandparent_dir, 'Asymmetric_Encryption', 'diffie_hellman.py')
rc4_path = os.path.join(grandparent_dir, 'Symmetric_Encryption', 'rc4.py')

dh_mod = load_module_from_path('dh_mod', dh_path)
rc4_mod = load_module_from_path('rc4_mod', rc4_path)

app = Flask(__name__)
CORS(app)

# Global client state
class ChatState:
    def __init__(self):
        self.server_ip = '127.0.0.1'
        self.port = 54321
        self.client_socket = None
        self.connected = False
        self.my_ip = None
        self.messages = []
        
        # E2EE State
        self.dh_instance = dh_mod.DiffieHellman(bits=128)
        self.rc4_instance = rc4_mod.RC4()
        self.shared_secrets = {} # target_ip -> secret_key (bytes)
        
    def connect(self, host, port):
        if self.connected:
            return True
        self.server_ip = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.port))
            self.connected = True
            threading.Thread(target=self.receive_loop, daemon=True).start()
            self.messages.append({"from": "System", "text": f"Connected to {host}:{port}"})
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def receive_loop(self):
        while self.connected:
            try:
                response = self.client_socket.recv(4096).decode()
                if not response:
                    self.connected = False
                    break
                
                # Split multiple JSON objects if they are concatenated
                # This is a hacky way but works for simple sockets
                responses = response.replace('}{', '}|||{').split('|||')
                
                for res in responses:
                    try:
                        msg = json.loads(res)
                        if msg.get("type") == "welcome":
                            self.my_ip = msg.get("ip")
                            self.messages.append({"from": "System", "text": f"✅ Connected! Your Virtual IP is: {self.my_ip}"})
                        elif msg.get("type") == "message":
                            sender = msg.get("from")
                            data_hex = msg.get("data")
                            
                            # Handle Key Exchange
                            if data_hex.startswith("DH_PUB_KEY:"):
                                parts = data_hex.split(":")
                                pub_key = int(parts[1])
                                p = int(parts[2])
                                g = int(parts[3])
                                
                                # CRITICAL: We MUST use the sender's P and G to compute the identical shared secret
                                specific_dh = dh_mod.DiffieHellman(p=p, g=g)
                                shared = specific_dh.generate_shared_secret(pub_key)
                                key_bytes = hashlib.sha256(str(shared).encode()).digest()[:16]
                                self.shared_secrets[sender] = key_bytes
                                
                                # Send reply using the new public key generated for this specific P and G
                                self.send_raw(sender, f"DH_PUB_KEY_REPLY:{specific_dh.public_key}")
                                self.messages.append({"from": "System", "text": f"🔑 Secure E2E channel established with {sender}!"})
                                
                            elif data_hex.startswith("DH_PUB_KEY_REPLY:"):
                                parts = data_hex.split(":")
                                pub_key = int(parts[1])
                                shared = self.dh_instance.generate_shared_secret(pub_key)
                                key_bytes = hashlib.sha256(str(shared).encode()).digest()[:16]
                                self.shared_secrets[sender] = key_bytes
                                self.messages.append({"from": "System", "text": f"🔑 Secure E2E channel established with {sender}!"})
                                
                            else:
                                # Decrypt Chat Message
                                if sender in self.shared_secrets:
                                    key = self.shared_secrets[sender]
                                    ciphertext = bytes.fromhex(data_hex)
                                    plaintext = self.rc4_instance.rc4_decrypt(ciphertext, key).decode('utf-8', errors='ignore')
                                    self.messages.append({"from": sender, "text": plaintext})
                                else:
                                    self.messages.append({"from": "System", "text": f"⚠️ Encrypted message from {sender} but no key established!"})
                        else:
                            # Filter out noisy delivery logs
                            if msg.get("status") == "success":
                                pass # Don't show in UI
                            elif msg.get("status") == "error":
                                self.messages.append({"from": "System", "text": f"⚠️ Error: {msg.get('message')}"})
                            else:
                                self.messages.append({"from": "Server", "text": res})
                    except json.JSONDecodeError:
                        pass # Ignore random non-JSON logs
            except Exception as e:
                print(f"Receive error: {e}")
                self.connected = False

    def send_raw(self, target, data_str):
        if not self.connected: return
        rq = Request(target, data_str)
        self.client_socket.sendall(rq.send_request())

    def send_encrypted(self, target, plaintext):
        if not self.connected: return False
        
        if target not in self.shared_secrets:
            # Initiate key exchange
            msg = f"DH_PUB_KEY:{self.dh_instance.public_key}:{self.dh_instance.p}:{self.dh_instance.g}"
            self.send_raw(target, msg)
            self.messages.append({"from": "System", "text": f"Initiating secure channel with {target}... Send your message again."})
            return False
            
        key = self.shared_secrets[target]
        ciphertext = self.rc4_instance.rc4_encrypt(plaintext.encode(), key)
        self.send_raw(target, ciphertext.hex())
        self.messages.append({"from": "Me", "target": target, "text": plaintext})
        return True

chat_state = ChatState()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure E2E Chat</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0f172a;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
            --accent: #3b82f6;
            --accent-glow: rgba(59, 130, 246, 0.5);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(59, 130, 246, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(168, 85, 247, 0.15), transparent 25%);
        }

        .container {
            width: 100%;
            max-width: 900px;
            height: 80vh;
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .header {
            padding: 20px 30px;
            border-bottom: 1px solid var(--glass-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.6);
        }

        .header h1 {
            font-size: 1.5rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .header h1 span {
            font-size: 0.8rem;
            background: rgba(168, 85, 247, 0.2);
            color: #c084fc;
            padding: 4px 8px;
            border-radius: 12px;
            border: 1px solid rgba(168, 85, 247, 0.3);
        }

        .connection-panel {
            display: flex;
            gap: 15px;
            padding: 20px 30px;
            background: rgba(30, 41, 59, 0.4);
            border-bottom: 1px solid var(--glass-border);
        }

        input {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid var(--glass-border);
            color: var(--text-main);
            padding: 10px 15px;
            border-radius: 8px;
            outline: none;
            transition: all 0.3s ease;
        }

        input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        button {
            background: var(--accent);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover {
            background: #2563eb;
            box-shadow: 0 4px 12px var(--accent-glow);
            transform: translateY(-1px);
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .messages {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .msg {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            line-height: 1.4;
            animation: slideIn 0.3s ease forwards;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .msg.me {
            align-self: flex-end;
            background: var(--accent);
            border-bottom-right-radius: 4px;
        }

        .msg.other {
            align-self: flex-start;
            background: rgba(51, 65, 85, 0.8);
            border: 1px solid var(--glass-border);
            border-bottom-left-radius: 4px;
        }

        .msg.system {
            align-self: center;
            background: transparent;
            color: var(--text-muted);
            font-size: 0.9rem;
            max-width: 90%;
            text-align: center;
            border: 1px dashed var(--glass-border);
        }

        .msg-header {
            font-size: 0.8rem;
            opacity: 0.8;
            margin-bottom: 4px;
            font-weight: 600;
        }

        .input-area {
            padding: 20px 30px;
            background: rgba(15, 23, 42, 0.6);
            border-top: 1px solid var(--glass-border);
            display: flex;
            gap: 15px;
        }

        .input-area input {
            flex: 1;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>SecureChat <span>End-to-End Encrypted (RC4 + Diffie-Hellman)</span></h1>
        <div id="my-ip" style="color: var(--accent); font-weight: bold; margin-right: auto; margin-left: 20px;"></div>
        <div id="status" style="color: #ef4444; font-weight: 600; font-size: 0.9rem;">● Disconnected</div>
    </div>

    <div class="connection-panel" id="conn-panel">
        <input type="text" id="host" placeholder="Server IP" value="127.0.0.1">
        <input type="number" id="port" placeholder="Port" value="4000" style="width: 100px;">
        <button onclick="connect()">Connect</button>
    </div>

    <div class="chat-area">
        <div class="messages" id="messages">
            <!-- Messages go here -->
            <div class="msg system">Welcome! Connect to the server to begin.</div>
        </div>
        
        <div class="input-area">
            <input type="text" id="target" placeholder="Target IP (e.g. 1.2)" style="width: 150px;">
            <input type="text" id="msg-input" placeholder="Type an encrypted message..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Send Secure</button>
        </div>
    </div>
</div>

<script>
    let lastMsgCount = 0;

    async function connect() {
        const host = document.getElementById('host').value;
        const port = document.getElementById('port').value;
        
        const res = await fetch('/api/connect', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({host, port: parseInt(port)})
        });
        const data = await res.json();
        
        if (data.success) {
            document.getElementById('status').style.color = '#10b981';
            document.getElementById('status').innerText = '● Connected';
            document.getElementById('conn-panel').style.opacity = '0.5';
            document.getElementById('conn-panel').style.pointerEvents = 'none';
        } else {
            alert('Connection failed!');
        }
    }

    async function sendMessage() {
        const target = document.getElementById('target').value;
        const text = document.getElementById('msg-input').value;
        
        if(!target || !text) return;
        
        await fetch('/api/send', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({target, text})
        });
        
        document.getElementById('msg-input').value = '';
        pollMessages();
    }

    async function pollMessages() {
        const res = await fetch('/api/messages');
        const data = await res.json();
        
        if (data.my_ip) {
            document.getElementById('my-ip').innerText = 'Your IP: ' + data.my_ip;
        }
        
        if (data.messages.length > lastMsgCount) {
            const msgsDiv = document.getElementById('messages');
            
            for (let i = lastMsgCount; i < data.messages.length; i++) {
                const m = data.messages[i];
                const el = document.createElement('div');
                
                if (m.from === 'Me') {
                    el.className = 'msg me';
                    el.innerHTML = `<div class="msg-header">To: ${m.target}</div>${m.text}`;
                } else if (m.from === 'System' || m.from === 'Server') {
                    el.className = 'msg system';
                    el.innerText = m.text;
                } else {
                    el.className = 'msg other';
                    el.innerHTML = `<div class="msg-header">From: ${m.from}</div>${m.text}`;
                }
                
                msgsDiv.appendChild(el);
            }
            
            msgsDiv.scrollTop = msgsDiv.scrollHeight;
            lastMsgCount = data.messages.length;
        }
    }

    // Poll every second
    setInterval(pollMessages, 1000);
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/connect', methods=['POST'])
def api_connect():
    data = request.json
    success = chat_state.connect(data.get('host'), data.get('port'))
    return jsonify({"success": success})

@app.route('/api/send', methods=['POST'])
def api_send():
    data = request.json
    success = chat_state.send_encrypted(data.get('target'), data.get('text'))
    return jsonify({"success": success})

@app.route('/api/messages', methods=['GET'])
def api_messages():
    return jsonify({"messages": chat_state.messages, "my_ip": chat_state.my_ip})

if __name__ == '__main__':
    port = 5001
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    print(f"Starting Chat UI on http://127.0.0.1:{port}")
    app.run(port=port, debug=False)
