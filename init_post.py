import requests
import json 


headers = {"Content-Type": "application/json"}

init_url = "http://localhost:5001/init"
init_payload = json.dumps({"model": "gpt-4o-mini"})
requests.post(init_url, headers=headers, data=init_payload)
