#config of the server
#the server will listen to this port 54321
# my ip structure is vlan_code:address
import hashlib
import os


class Config:
    def __init__(self):
        # Load .env file manually if it exists
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, val = line.split('=', 1)
                        os.environ[key] = val

        self.PORT = int(os.getenv('PORT', '54321'))
        self.BUFFER_SIZE = int(os.getenv('BUFFER_SIZE', '1024'))
        self.USERNAME = os.getenv('USERNAME', 'admin')
        self.__PASSWORD = os.getenv('PASSWORD', 'admin123')
        self.SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')

    def server_json(self):
        return {
            "server_info": {
                "ip": self.SERVER_IP,
                "port": self.PORT,
                "username": self.USERNAME,
                "password": hashlib.sha256(self.__PASSWORD.encode()).hexdigest()
            },
            "vlans": {
                
            }
        }
        