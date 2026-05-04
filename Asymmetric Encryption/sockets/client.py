import socket
import threading
import json
import request

class Client:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            self.client_socket.connect((self.server_ip, self.port))
            self.connected = True
            print(f"Connected to server at {self.server_ip}:{self.port}")
            
            # Start two threads: one for receiving, one for sending
            receive_thread = threading.Thread(target=self.receive_loop, daemon=True)
            send_thread = threading.Thread(target=self.send_loop)
            
            receive_thread.start()
            send_thread.start()
            
            send_thread.join()  # Wait for send thread to complete
        except Exception as e:
            print(f"Failed to connect to server: {e}")
        finally:
            self.close()
    
    def receive_loop(self):
        """Continuously receive messages from server or other clients"""
        while self.connected:
            try:
                response = self.client_socket.recv(1024).decode()
                if response:
                    try:
                        msg = json.loads(response)
                        if msg.get("type") == "message":
                            # Message from another client
                            print(f"\n[Message from {msg.get('from')}]: {msg.get('data')}")
                        else:
                            # Response from server
                            print(f"\n[Server]: {response}")
                    except:
                        print(f"\n[Server]: {response}")
                else:
                    self.connected = False
            except Exception as e:
                if self.connected:
                    print(f"Failed to receive: {e}")
                self.connected = False
    
    def send_loop(self):
        """Handle user input and send messages"""
        while self.connected:
            try:
                target = input("\nEnter target host (or 'exit' to quit): ")
                if target.lower() == 'exit':
                    self.connected = False
                    break
                data = input("Enter message/data to send: ")
                self.send_request(target, data)
            except Exception as e:
                print(f"Error: {e}")
                self.connected = False
    
    def send_request(self, target, data):
        try:
            rq = request.Request(target, data)
            self.client_socket.sendall(rq.send_request())
        except Exception as e:
            print(f"Failed to send request: {e}")
            self.connected = False

    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    client = Client('127.0.0.1', 54321)
    client.connect()
    client.close()