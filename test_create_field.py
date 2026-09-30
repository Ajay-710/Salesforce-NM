import requests
import json

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

# Let's test creating Beneficiary_Name__c on Policy__c
field_data = {
    "FullName": "Policy__c.Beneficiary_Name__c",
    "Metadata": {
        "label": "Beneficiary Name",
        "type": "Text",
        "length": 50,
        "required": False,
        "externalId": False
    }
}

res = requests.post(f"{instance_url}/services/data/v60.0/tooling/sobjects/CustomField", headers=headers, json=field_data)
print("Create Beneficiary_Name__c:", res.status_code, res.text)
