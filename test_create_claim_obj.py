import requests
import json

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

obj_data = {
    "FullName": "Claim__c",
    "Metadata": {
        "label": "Claim",
        "pluralLabel": "Claim",
        "deploymentStatus": "Deployed",
        "sharingModel": "ReadWrite",
        "nameField": {
            "type": "AutoNumber",
            "label": "Claim Number",
            "displayFormat": "C - {0000}",
            "startingNumber": 1
        },
        "enableReports": True,
        "enableActivities": True,
        "enableHistory": True,
        "enableSearch": True
    }
}

res = requests.post(f"{instance_url}/services/data/v60.0/tooling/sobjects/CustomObject", headers=headers, json=obj_data)
print("Create Claim__c:", res.status_code, res.text)
