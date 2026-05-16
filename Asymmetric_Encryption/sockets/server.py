# create a server socket with a list of ports
# use the asymetric encryption (public and private key)
#

import socket
import threading
import random
import json
import config
import dhci
import request
import hashlib


class Server:
    def __init__(self):
        self.config = config.Config()
        self.dhci = dhci.DHCI(self.config)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.config.PORT))
        self.server_socket.listen(5)
        self.server_socket.settimeout(1.0)  # 1 second timeout to allow keyboard interrupt
        self.clients = {}  # Dictionary to store connected clients: {ip_address: socket}
        self.intruders = [] # List of intruder sockets
        self.clients_lock = threading.Lock()  # Thread lock for safe access
        self.running = True
        print(f"Server is listening on {self.config.PORT}")

    def handle_client(self, client_socket, addr):
        # Assign client to VLAN and keep connection alive for messaging
        ip_address = None
        try:
            vlan_code = '1'  # Default VLAN, can be dynamic
            ip_address = self.dhci.affect_to_vlan(vlan_code)
            print(f"Client {addr} assigned IP: {ip_address}\n")
            
            # Register this client
            with self.clients_lock:
                self.clients[ip_address] = client_socket
            print(f"Registered client {ip_address}. Total clients: {len(self.clients)}\n")
            
            # Tell the client its newly assigned IP
            welcome_msg = json.dumps({"type": "welcome", "ip": ip_address}).encode()
            client_socket.sendall(welcome_msg)
            
            # Keep listening for requests from this client
            while True:
                request_data = client_socket.recv(1024)
                if not request_data:
                    break
                
                response = self.handle_request(request_data, ip_address)
                client_socket.sendall(response)
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            # Unregister this client
            if ip_address:
                with self.clients_lock:
                    if ip_address in self.clients:
                        del self.clients[ip_address]
                    if client_socket in self.intruders:
                        self.intruders.remove(client_socket)
                print(f"Unregistered client {ip_address}. Total clients: {len(self.clients)}")
            client_socket.close()
            print(f"Client {addr} disconnected")
        
    def handle_request(self, request, sender_ip):
        # Handle the request and route to target host
        try:
            RQ = json.loads(request.decode())
            target = RQ.get('target')  # Target host to receive the message
            data = RQ.get('data')      # Message/data to send to target
            
            if not target or not data:
                return json.dumps({"status": "error", "message": "Missing target or data"}).encode()
                
            # Handle Intruder Registration
            if target == "INTRUDER_REGISTRATION":
                with self.clients_lock:
                    if self.clients[sender_ip] not in self.intruders:
                        self.intruders.append(self.clients[sender_ip])
                return json.dumps({"status": "success", "message": "Registered as an intruder! Intercepting traffic..."}).encode()
            
            # Try to find and forward message to target host
            with self.clients_lock:
                if target in self.clients:
                    # Target is connected - forward the message
                    target_socket = self.clients[target]
                    message_to_target = json.dumps({
                        "type": "message",
                        "from": sender_ip,
                        "data": data
                    }).encode()
                    try:
                        target_socket.sendall(message_to_target)
                        
                        # --- BROADCAST TO INTRUDERS ---
                        intercept_msg = json.dumps({
                            "type": "intercept",
                            "from": sender_ip,
                            "to": target,
                            "data": data
                        }).encode()
                        for intruder in self.intruders:
                            try:
                                intruder.sendall(intercept_msg)
                            except Exception:
                                pass
                        # ------------------------------
                        
                        return json.dumps({
                            "status": "success",
                            "message": f"Message delivered to {target}"
                        }).encode()
                    except Exception as e:
                        return json.dumps({
                            "status": "error",
                            "message": f"Failed to deliver to {target}: {str(e)}"
                        }).encode()
                else:
                    # Target not connected
                    return json.dumps({
                        "status": "error",
                        "message": f"Target host {target} is not connected"
                    }).encode()
        
        except json.JSONDecodeError:
            return json.dumps({"status": "error", "message": "Invalid JSON format"}).encode()
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)}).encode()
    
    def authenticate(self, username, password):
        # Authenticate the client using the username and password
        if username == self.config.USERNAME and hashlib.sha256(password.encode()).hexdigest() == self.config.server_json()['server_info']['password']:
            return True
        else:
            return False

    def start(self):
        print("Starting the server...")
        
        # check the data of the server from server.json if exsist else create new one
        try:
            with open('server.json', 'r') as f:
                server_infos = json.load(f)
        except FileNotFoundError:
            with open('server.json', 'w') as f:
                json.dump(self.config.server_json(), f)

        
        
        self.running = True
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"Accepted connection from {addr}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_handler.daemon = True
                client_handler.start()
            except socket.timeout:
                # Timeout is normal, just continue
                continue
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")
    
    def stop(self):
        self.running = False
        self.server_socket.close()
        # close all client connections
        with self.clients_lock:
            for ip, client_socket in self.clients.items():
                try:
                    client_socket.close()
                except Exception as e:
                    print(f"Error closing connection for {ip}: {e}")
            self.clients.clear()
        # Clear all vlans hosts
        try:
            with open('server.json', 'r') as f:
                server_infos = json.load(f)
                for vlan_code in server_infos['vlans']:
                    server_infos['vlans'][vlan_code]['hosts'] = []
            with open('server.json', 'w') as f:
                json.dump(server_infos, f)
        except FileNotFoundError:
            pass  # If file doesn't exist, nothing to clear
        
            
if __name__ == "__main__":
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop()
        exit(0)
    
            