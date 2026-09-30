import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

res = requests.get(f"{instance_url}/services/data/v60.0/tooling/query/?q=SELECT+Id,DeveloperName+FROM+CustomObject+WHERE+DeveloperName='Claim'+OR+DeveloperName='Policy'", headers=headers)
print("CustomObject query:", res.status_code, res.text)
