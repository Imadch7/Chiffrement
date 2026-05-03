import json

class Request:
    
    def __init__(self, target, data):
        self.RQ = {
            "target": target,
            "data": data
        }
    
    def send_request(self):
        # return the request as proper JSON bytes
        return json.dumps(self.RQ).encode()
    
    def response(self, response_data):
        # return the response as JSON bytes
        return json.dumps(response_data).encode()
    
    
        