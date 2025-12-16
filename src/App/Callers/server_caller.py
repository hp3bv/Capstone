import os
import requests

SERVER_LINK = os.environ.get("SERVER_LINK")
if not SERVER_LINK:
    raise ValueError("SERVER_LINK not set")

class ServerCaller:
    def __init__(self):
        self.ext = None
        
    def postRequest(self, body, callback=None):
        url = SERVER_LINK + self.ext
        response = requests.post(url, json=body)
        
        if not response.ok:
            print(f"Request failed with {response.status_code}: {response.text}")
        
        return response
        
    def getRequest(self, body, extAddition="", callback=None):
        url = SERVER_LINK + self.ext + extAddition
        response = requests.get(url, json=body)
        
        if not response.ok:
            print(f"Request failed with {response.status_code}: {response.text}")
            
        return response