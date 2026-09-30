import requests
import json

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

def deploy_class(name, filepath):
    with open(filepath, "r") as f:
        code = f.read()
    payload = {
        "Name": name,
        "Body": code
    }
    res = requests.post(f"{instance_url}/services/data/v60.0/tooling/sobjects/ApexClass", headers=headers, json=payload)
    print(f"Deploy {name}:", res.status_code, res.text)

deploy_class("ClaimsAdjusterController", "force-app/main/default/classes/ClaimsAdjusterController.cls")
deploy_class("ClaimsAdjusterControllerTest", "force-app/main/default/classes/ClaimsAdjusterControllerTest.cls")
