import sys
import threading
import json
import socket
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from request import Request

app = Flask(__name__)
CORS(app)

class IntruderState:
    def __init__(self):
        self.server_ip = '127.0.0.1'
        self.port = 4000
        self.client_socket = None
        self.connected = False
        self.intercepts = []
        
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
            
            # Send registration
            rq = Request("INTRUDER_REGISTRATION", "I am the intruder")
            self.client_socket.sendall(rq.send_request())
            
            self.intercepts.append({"from": "SYSTEM", "text": f"Connected to {host}:{port}. Awaiting intercepts..."})
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
                
                responses = response.replace('}{', '}|||{').split('|||')
                for res in responses:
                    try:
                        msg = json.loads(res)
                        if msg.get("type") == "intercept":
                            sender = msg.get("from")
                            target = msg.get("to")
                            data_hex = msg.get("data")
                            
                            self.intercepts.append({
                                "from": sender,
                                "target": target,
                                "data": data_hex
                            })
                        elif msg.get("status") == "success":
                            self.intercepts.append({"from": "SYSTEM", "text": msg.get("message")})
                    except json.JSONDecodeError:
                        pass
            except Exception as e:
                print(f"Receive error: {e}")
                self.connected = False

intruder_state = IntruderState()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intruder Sniffer</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #050505;
            --text: #00ff00;
            --border: #004400;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Share Tech Mono', monospace; }
        
        body {
            background-color: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .container {
            width: 100%;
            max-width: 900px;
            height: 80vh;
            border: 1px solid var(--text);
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
            display: flex;
            flex-direction: column;
        }

        .header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            background: rgba(0, 50, 0, 0.3);
            text-transform: uppercase;
        }

        .connection-panel {
            padding: 15px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            gap: 15px;
        }

        input {
            background: #000;
            border: 1px solid var(--text);
            color: var(--text);
            padding: 8px 12px;
            outline: none;
        }

        button {
            background: transparent;
            color: var(--text);
            border: 1px solid var(--text);
            padding: 8px 15px;
            cursor: pointer;
            text-transform: uppercase;
        }
        button:hover { background: var(--text); color: #000; }

        .sniff-area {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .intercept {
            border: 1px dashed var(--border);
            padding: 10px;
            background: rgba(0, 20, 0, 0.5);
        }
        .intercept.system { border: none; color: #00aa00; font-size: 0.9em; }
        
        .intercept-header { font-size: 0.85rem; opacity: 0.8; margin-bottom: 5px; }
        .intercept-data { word-break: break-all; color: #ff0055; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>[ INTRUDER :: NETWORK SNIFFER ]</h1>
        <div id="status" style="color: #aa0000;">[ OFFLINE ]</div>
    </div>

    <div class="connection-panel" id="conn-panel">
        <input type="text" id="host" value="127.0.0.1">
        <input type="number" id="port" value="4000" style="width:80px;">
        <button onclick="connect()">[ INJECT ]</button>
    </div>

    <div class="sniff-area" id="sniff-area">
        <div class="intercept system">Waiting for injection...</div>
    </div>
</div>

<script>
    let lastCount = 0;

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
            document.getElementById('status').style.color = '#00ff00';
            document.getElementById('status').innerText = '[ ONLINE ]';
        }
    }

    async function poll() {
        const res = await fetch('/api/intercepts');
        const data = await res.json();
        
        if (data.intercepts.length > lastCount) {
            const area = document.getElementById('sniff-area');
            for (let i = lastCount; i < data.intercepts.length; i++) {
                const m = data.intercepts[i];
                const el = document.createElement('div');
                
                if (m.from === 'SYSTEM') {
                    el.className = 'intercept system';
                    el.innerText = '> ' + m.text;
                } else {
                    el.className = 'intercept';
                    el.innerHTML = `
                        <div class="intercept-header">INTERCEPT: ${m.from} -> ${m.target}</div>
                        <div class="intercept-data">${m.data}</div>
                    `;
                }
                area.appendChild(el);
            }
            area.scrollTop = area.scrollHeight;
            lastCount = data.intercepts.length;
        }
    }

    setInterval(poll, 1000);
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
    success = intruder_state.connect(data.get('host'), data.get('port'))
    return jsonify({"success": success})

@app.route('/api/intercepts', methods=['GET'])
def api_intercepts():
    return jsonify({"intercepts": intruder_state.intercepts})

if __name__ == '__main__':
    port = 5003
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    print(f"Starting Intruder Dashboard on http://127.0.0.1:{port}")
    app.run(port=port, debug=False)
