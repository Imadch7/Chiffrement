#config of the server
#the server will listen to this port 54321
# my ip structure is vlan_code:address
import hashlib
import os
import dotenv

dotenv.load_dotenv()

class Config:
    def __init__(self):
        self.PORT = int(os.getenv('PORT'))
        self.BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))
        self.USERNAME = os.getenv('USERNAME')
        self.__PASSWORD = os.getenv('PASSWORD')
        self.SERVER_IP = os.getenv('SERVER_IP')

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

        