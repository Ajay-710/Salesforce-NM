import requests
import json

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

with open("force-app/main/default/classes/PremiumCalculator.cls", "r") as f:
    code = f.read()

payload = {
    "Name": "PremiumCalculator",
    "Body": code
}

res = requests.post(f"{instance_url}/services/data/v60.0/tooling/sobjects/ApexClass", headers=headers, json=payload)
print("Create PremiumCalculator:", res.status_code, res.text)
