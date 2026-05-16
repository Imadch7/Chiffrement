#Dynamic Host Configuration IDentifier
#creating a vlan
import json
import time
class DHCI:
    def __init__(self, config):
        self.config = config
        
    def find_host_vlan(self, target):
        try:
            with open('server.json', 'r') as f:
                server_infos = json.load(f)
                # search for the target host in all vlans
                for vlan_code, vlan_info in server_infos['vlans'].items():
                    if target in vlan_info['hosts']:
                        return vlan_code
            return None
        except FileNotFoundError:
            print("server.json file not found. Please create a vlan first.")
            return None
    
    def create_vlan(self):
        try:
            with open('server.json', 'r') as f:
                server_infos = json.load(f)
                # check the last vlan code and increment it by 1
                # {
                #   vlan_code: code,
                #   hosts: []
                # }
            vlans = server_infos['vlans']
            if vlans:
                last_vlan_code = max(vlans.keys())
                new_vlan_code = str(int(last_vlan_code) + 1)
            else:
                new_vlan_code = '1'
            server_infos['vlans'][new_vlan_code] = {
                "hosts": []
            }
            with open('server.json', 'w') as f:
                json.dump(server_infos, f)
        except FileNotFoundError:
            with open('server.json', 'w') as f:
                server_infos = self.config.server_json()
                server_infos['vlans']['1'] = {
                    "hosts": []
                }
                json.dump(server_infos, f)
    
    def affect_to_vlan(self, vlan_code):
        try:
            with open('server.json', 'r') as f:
                server_infos = json.load(f)
                # check if the vlan code exist
                if vlan_code in server_infos['vlans']:
                    # get the hosts of the vlan
                    hosts = server_infos['vlans'][vlan_code]['hosts']
                    if len(hosts) >= 5:
                        print(f"Vlan code {vlan_code} is full.")
                        print("Affecting to the next vlan...")
                        time.sleep(1)
                        return self.affect_to_vlan(str(int(vlan_code)+1))
                    # generate a random ip address for the host
                    new_ip = f"{vlan_code}.{len(hosts) + 1}"
                    # add the new ip to the hosts of the vlan
                    hosts.append(new_ip)
                    # update the server.json file
                    with open('server.json', 'w') as f:
                        json.dump(server_infos, f)
                    return new_ip
                    
                else:
                    print(f"Vlan code {vlan_code} not found. Please create a vlan first.")
                    print("Creating a new vlan...")
                    time.sleep(1)
                    self.create_vlan()
                    return self.affect_to_vlan(vlan_code)
        except FileNotFoundError:
            print("server.json file not found. Please create a vlan first.") 
            print("Creating a new vlan...")
            time.sleep(1)
            self.create_vlan()
            return self.affect_to_vlan(vlan_code)